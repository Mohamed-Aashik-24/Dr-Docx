import torch
import torch.nn as nn
import torch.nn.init as init

class DocumentElementNetwork(nn.Module):
    """
    PyTorch Multilayer Perceptron for Document Element Classification.
    Takes TF-IDF n-gram text features concatenated with structural metadata features.
    """

    def __init__(self, input_size: int, num_classes: int, dropout1: float = 0.3, dropout2: float = 0.2):
        super(DocumentElementNetwork, self).__init__()
        self.input_size = input_size
        self.num_classes = num_classes
        self.net = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Dropout(dropout1),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout2),
            nn.Linear(128, num_classes)
        )
        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Returns raw logits (softmax is applied during loss calculation / inference)."""
        return self.net(x)
