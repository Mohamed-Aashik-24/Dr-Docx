import os
from typing import Tuple, Dict, Any, Optional, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

from src.config import ElementType, MODEL_PATH, VECTORIZER_PATH, MODEL_DIR, CONFIDENCE_THRESHOLD
from src.feature_extractor import FeatureExtractor
from data.training_data import generate_training_data

class DocumentClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1, class_weight='balanced')
        self.feature_extractor = FeatureExtractor()
        self.label_encoder = LabelEncoder()
        self._is_trained = False
        
    def train(self) -> Dict[str, Any]:
        data = generate_training_data()
        
        texts = [item[0] for item in data]
        metadata_list = [item[1] for item in data]
        labels = [item[2] for item in data]
        
        self.feature_extractor.fit_tfidf(texts)
        
        X = []
        for text, meta in zip(texts, metadata_list):
            X.append(self.feature_extractor.get_feature_vector(
                text=text,
                is_bold=meta.get('is_bold', False),
                is_italic=meta.get('is_italic', False),
                font_size=meta.get('font_size'),
                position_ratio=meta.get('position_ratio', 0.5)
            ))
        X = np.array(X)
        y = self.label_encoder.fit_transform(labels)
        
        self.model.fit(X, y)
        
        scores = cross_val_score(self.model, X, y, cv=5)
        accuracy = np.mean(scores)
        print(f"Cross-validation accuracy: {accuracy:.4f}")
        
        self._is_trained = True
        self.save()
        
        return {
            "accuracy": accuracy,
            "num_samples": len(data),
            "num_features": X.shape[1]
        }
        
    def predict(self, text: str, is_bold: bool = False, is_italic: bool = False, font_size: Optional[float] = None, position_ratio: float = 0.5) -> Tuple[ElementType, float]:
        if not self.is_trained():
            raise RuntimeError("Model is not trained or loaded.")
            
        features = self.feature_extractor.get_feature_vector(text, is_bold, is_italic, font_size, position_ratio)
        features_2d = features.reshape(1, -1)
        
        pred_idx = self.model.predict(features_2d)[0]
        probas = self.model.predict_proba(features_2d)[0]
        
        confidence = probas[pred_idx]
        label_str = self.label_encoder.inverse_transform([pred_idx])[0]
        
        try:
            element_type = ElementType(label_str)
        except ValueError:
            for e in ElementType:
                if e.value == label_str:
                    element_type = e
                    break
            else:
                raise ValueError(f"Unknown label: {label_str}")
        
        return element_type, confidence

    def predict_batch(self, items: List[dict]) -> List[Tuple[ElementType, float]]:
        if not self.is_trained():
            raise RuntimeError("Model is not trained or loaded.")
        if not items:
            return []
            
        X = self.feature_extractor.get_feature_vectors_batch(items)
        preds = self.model.predict(X)
        probas = self.model.predict_proba(X)
        
        results = []
        for i, pred_idx in enumerate(preds):
            confidence = float(probas[i, pred_idx])
            label_str = self.label_encoder.inverse_transform([pred_idx])[0]
            try:
                elem_type = ElementType(label_str)
            except ValueError:
                elem_type = ElementType.BODY
            results.append((elem_type, confidence))
            
        return results

    def load(self) -> bool:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            return False
            
        try:
            self.model = joblib.load(MODEL_PATH)
            self.feature_extractor.load_vectorizer(VECTORIZER_PATH)
            label_encoder_path = os.path.join(MODEL_DIR, "label_encoder.joblib")
            if os.path.exists(label_encoder_path):
                self.label_encoder = joblib.load(label_encoder_path)
            self._is_trained = True
            return True
        except Exception:
            return False
            
    def save(self) -> None:
        os.makedirs(MODEL_DIR, exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        self.feature_extractor.save_vectorizer(VECTORIZER_PATH)
        joblib.dump(self.label_encoder, os.path.join(MODEL_DIR, "label_encoder.joblib"))
        
    def is_trained(self) -> bool:
        return self._is_trained
