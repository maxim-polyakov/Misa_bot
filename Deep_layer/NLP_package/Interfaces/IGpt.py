from abc import ABC, abstractmethod
import torch
DEVICE = torch.device('cpu')


class IGpt(ABC):
    """

    """
    @abstractmethod
    def generate(self):
        pass