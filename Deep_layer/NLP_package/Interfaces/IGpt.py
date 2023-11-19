from abc import ABC, abstractmethod
import torch
DEVICE = torch.device('cpu')


class IGpt(ABC):


    """

    This entyty describes a GPT bot

    """

    @abstractmethod
    def generate(self):
        pass