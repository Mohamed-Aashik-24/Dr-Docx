import os
import random
from typing import Tuple, Dict, Any, Optional, List
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
import joblib

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from src.config import (
    ElementType,
    MODEL_DIR,
    PYTORCH_MODEL_PATH,
    VECTORIZER_PATH,
    LABEL_ENCODER_PATH,
    CONFIDENCE_THRESHOLD,
    LEARNING_RATE,
    BATCH_SIZE,
    EPOCHS,
    EARLY_STOPPING_PATIENCE,
    DROPOUT_RATE_1,
    DROPOUT_RATE_2,
    RANDOM_SEED,
)
from src.feature_extractor import FeatureExtractor
from src.neural_model import DocumentElementNetwork
from data.training_data import generate_training_data


def seed_everything(seed: int = RANDOM_SEED):
    """Sets random seeds across random, numpy, and PyTorch for reproducible training."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class DocumentClassifier:
    """
    Document element classifier powered by a PyTorch Multilayer Perceptron.
    Extracts text features via TF-IDF combined with structural document metadata.
    """

    def __init__(self, device: Optional[str] = None):
        seed_everything(RANDOM_SEED)
        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model: Optional[DocumentElementNetwork] = None
        self.feature_extractor = FeatureExtractor()
        self.label_encoder = LabelEncoder()
        self._is_trained = False
        self.input_size: Optional[int] = None
        self.num_classes: Optional[int] = None

    def train(
        self,
        epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        lr: Optional[float] = None,
        patience: Optional[int] = None,
        val_split: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Trains the PyTorch MLP document classifier.
        Uses Adam optimizer, CrossEntropyLoss, and early stopping.
        """
        seed_everything(RANDOM_SEED)
        max_epochs = epochs if epochs is not None else EPOCHS
        b_size = batch_size if batch_size is not None else BATCH_SIZE
        learning_rate = lr if lr is not None else LEARNING_RATE
        max_patience = patience if patience is not None else EARLY_STOPPING_PATIENCE

        data = generate_training_data()
        texts = [item[0] for item in data]
        metadata_list = [item[1] for item in data]
        labels = [item[2] for item in data]

        # 1. Fit TF-IDF vectorizer
        self.feature_extractor.fit_tfidf(texts)

        # 2. Encode string labels into integer class IDs
        y = self.label_encoder.fit_transform(labels)
        self.num_classes = len(self.label_encoder.classes_)

        # 3. Extract combined feature vectors (structural metadata + TF-IDF)
        X_list = []
        for text, meta in zip(texts, metadata_list):
            feat_vec = self.feature_extractor.get_feature_vector(
                text=text,
                is_bold=meta.get('is_bold', False),
                is_italic=meta.get('is_italic', False),
                font_size=meta.get('font_size'),
                position_ratio=meta.get('position_ratio', 0.5),
            )
            X_list.append(feat_vec)

        X = np.array(X_list, dtype=np.float32)
        self.input_size = X.shape[1]

        # 4. Stratified Train / Validation Split
        try:
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=val_split, random_state=RANDOM_SEED, stratify=y
            )
        except ValueError:
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=val_split, random_state=RANDOM_SEED
            )

        train_dataset = TensorDataset(
            torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long)
        )
        val_dataset = TensorDataset(
            torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.long)
        )

        train_loader = DataLoader(train_dataset, batch_size=b_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=b_size, shuffle=False)

        # 5. Build Model
        self.model = DocumentElementNetwork(
            input_size=self.input_size,
            num_classes=self.num_classes,
            dropout1=DROPOUT_RATE_1,
            dropout2=DROPOUT_RATE_2,
        ).to(self.device)

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)

        best_val_loss = float('inf')
        best_val_acc = 0.0
        best_macro_f1 = 0.0
        best_model_state = None
        patience_counter = 0
        epochs_completed = 0

        # 6. Training Loop with Early Stopping
        for epoch in range(1, max_epochs + 1):
            epochs_completed = epoch
            self.model.train()
            train_loss = 0.0

            for batch_x, batch_y in train_loader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)

                optimizer.zero_grad()
                logits = self.model(batch_x)
                loss = criterion(logits, batch_y)
                loss.backward()
                optimizer.step()

                train_loss += loss.item() * batch_x.size(0)

            train_loss /= len(train_dataset)

            # Validation Evaluation
            self.model.eval()
            val_loss = 0.0
            val_preds = []
            val_targets = []

            with torch.no_grad():
                for batch_x, batch_y in val_loader:
                    batch_x = batch_x.to(self.device)
                    batch_y = batch_y.to(self.device)

                    logits = self.model(batch_x)
                    loss = criterion(logits, batch_y)
                    val_loss += loss.item() * batch_x.size(0)

                    preds = torch.argmax(logits, dim=1)
                    val_preds.extend(preds.cpu().numpy())
                    val_targets.extend(batch_y.cpu().numpy())

            val_loss /= len(val_dataset)
            epoch_val_acc = float(accuracy_score(val_targets, val_preds))
            epoch_macro_f1 = float(f1_score(val_targets, val_preds, average='macro', zero_division=0))

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_val_acc = epoch_val_acc
                best_macro_f1 = epoch_macro_f1
                best_model_state = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= max_patience:
                    break

        if best_model_state is not None:
            self.model.load_state_dict(best_model_state)
            self.model.to(self.device)

        self._is_trained = True
        self.save()

        print(f"PyTorch MLP training complete ({epochs_completed} epochs, "
              f"val_acc: {best_val_acc:.4f}, macro_f1: {best_macro_f1:.4f}, device: {self.device})")

        return {
            'accuracy': best_val_acc,
            'num_samples': len(data),
            'num_features': self.input_size,
            'validation_accuracy': best_val_acc,
            'macro_f1': best_macro_f1,
            'epochs_completed': epochs_completed,
            'model_type': 'PyTorch MLP',
            'device': str(self.device),
        }

    def predict(
        self,
        text: str,
        is_bold: bool = False,
        is_italic: bool = False,
        font_size: Optional[float] = None,
        position_ratio: float = 0.5,
    ) -> Tuple[ElementType, float]:
        """Predicts ElementType and confidence score for a single element."""
        if not self.is_trained():
            raise RuntimeError('Model is not trained or loaded.')

        self.model.eval()
        with torch.no_grad():
            features = self.feature_extractor.get_feature_vector(text, is_bold, is_italic, font_size, position_ratio)
            features_tensor = torch.tensor(features, dtype=torch.float32, device=self.device).unsqueeze(0)
            logits = self.model(features_tensor)

            probas = torch.softmax(logits, dim=1)
            pred_idx = torch.argmax(probas, dim=1).item()
            confidence = float(probas[0, pred_idx].item())

        label_str = self.label_encoder.inverse_transform([pred_idx])[0]
        try:
            element_type = ElementType(label_str)
        except ValueError:
            for e in ElementType:
                if e.value == label_str:
                    element_type = e
                    break
            else:
                element_type = ElementType.BODY

        return element_type, confidence

    def predict_batch(self, items: List[dict]) -> List[Tuple[ElementType, float]]:
        """Performs batched inference for a list of element metadata dictionaries."""
        if not self.is_trained():
            raise RuntimeError('Model is not trained or loaded.')
        if not items:
            return []

        self.model.eval()
        with torch.no_grad():
            X = self.feature_extractor.get_feature_vectors_batch(items)
            X_tensor = torch.tensor(X, dtype=torch.float32, device=self.device)
            logits = self.model(X_tensor)

            probas = torch.softmax(logits, dim=1)
            preds = torch.argmax(probas, dim=1).cpu().numpy()
            probas_np = probas.cpu().numpy()

        results = []
        label_strs = self.label_encoder.inverse_transform(preds)
        for i, label_str in enumerate(label_strs):
            pred_idx = preds[i]
            confidence = float(probas_np[i, pred_idx])
            try:
                elem_type = ElementType(label_str)
            except ValueError:
                elem_type = ElementType.BODY
            results.append((elem_type, confidence))

        return results

    def load(
        self,
        model_path: Optional[str] = None,
        vectorizer_path: Optional[str] = None,
        encoder_path: Optional[str] = None,
    ) -> bool:
        """Loads model weights, vectorizer, and label encoder."""
        import src.config as cfg
        pt_path = model_path or str(cfg.PYTORCH_MODEL_PATH)
        vec_path = vectorizer_path or str(cfg.VECTORIZER_PATH)
        enc_path = encoder_path or str(cfg.LABEL_ENCODER_PATH)

        if not os.path.exists(pt_path) or not os.path.exists(vec_path) or not os.path.exists(enc_path):
            return False

        try:
            checkpoint = torch.load(pt_path, map_location=self.device, weights_only=False)
            self.input_size = checkpoint['input_size']
            self.num_classes = checkpoint['num_classes']

            self.model = DocumentElementNetwork(
                input_size=self.input_size,
                num_classes=self.num_classes,
                dropout1=DROPOUT_RATE_1,
                dropout2=DROPOUT_RATE_2,
            ).to(self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.eval()

            self.feature_extractor.load_vectorizer(vec_path)
            self.label_encoder = joblib.load(enc_path)
            self._is_trained = True
            return True
        except Exception:
            self._is_trained = False
            self.model = None
            return False

    def save(
        self,
        model_path: Optional[str] = None,
        vectorizer_path: Optional[str] = None,
        encoder_path: Optional[str] = None,
    ) -> None:
        """Saves model state_dict, vectorizer, and label encoder."""
        import src.config as cfg
        pt_path = model_path or str(cfg.PYTORCH_MODEL_PATH)
        vec_path = vectorizer_path or str(cfg.VECTORIZER_PATH)
        enc_path = encoder_path or str(cfg.LABEL_ENCODER_PATH)

        os.makedirs(str(cfg.MODEL_DIR), exist_ok=True)

        if self.model is not None:
            label_classes_list = None
            if hasattr(self.label_encoder, 'classes_') and self.label_encoder.classes_ is not None:
                label_classes_list = list(self.label_encoder.classes_)

            checkpoint = {
                'model_state_dict': self.model.state_dict(),
                'input_size': self.input_size,
                'num_classes': self.num_classes,
                'label_classes': label_classes_list,
                'model_type': 'PyTorch MLP',
            }
            torch.save(checkpoint, pt_path)

        self.feature_extractor.save_vectorizer(vec_path)
        joblib.dump(self.label_encoder, enc_path)

    def is_trained(self) -> bool:
        return self._is_trained and self.model is not None
