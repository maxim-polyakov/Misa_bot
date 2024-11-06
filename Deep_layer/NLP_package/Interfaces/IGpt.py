from abc import ABC, abstractmethod
import torch
DEVICE = torch.device('cpu')


class IGpt(ABC):
    """
    It is entyti of gpt
    """
    @abstractmethod
    def generate(self):
        pass