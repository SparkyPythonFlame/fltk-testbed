import logging
from abc import abstractmethod, ABC
from logging import ERROR
from typing import Dict, List, Union, Callable

import torch


class PoisonPill(ABC):

    def __init__(self):
        self.logger = logging.getLogger()

    @abstractmethod
    def poison_input(self, X: torch.Tensor, *args, **kwargs):
        """
        Poison the output according to the corresponding attack.
        """
        pass

    @abstractmethod
    def poison_output(self, X: torch.Tensor, Y: torch.Tensor, *args, **kwargs):
        """
        Poison the output according to the corresponding attack.
        """
        pass

    def poison_targets(self) -> Union[Callable, None]:
        return None

    @abstractmethod
    def __str__(self):
        pass

class FlipPill(PoisonPill):

    def poison_targets(self) -> Callable:
        """
        Apply poison to the targets of a dataset. Note that this is a somewhat strange approach, as the pill ingest the
        targets, instead of the Dataset itself. However, this allows for a more efficient implementation.
        @param targets: Original targets of the dataset.
        @type targets: list
        @return: List of mapped targets according to self.flips.
        @rtype: list
        """
        # Apply mapping to the input, default value is the target itself!
        def flipper(y):
            return  self.flips.get(y, y)
        return flipper

    def __init__(self, flip_description: Dict[int, int]):
        """
            Implements the flip attack scenario, where one or multiple attacks are implemented
            """
        super().__init__()
        self.flips = flip_description

    def poison_output(self, X: torch.Tensor, Y: torch.Tensor, *args, **kwargs) -> (torch.Tensor, torch.Tensor):
        """
        Flip attack does not affect output, rather the pill is taken by the dataset.
        """
        return X, Y

    def poison_input(self, X: torch.Tensor, *args, **kwargs) -> torch.Tensor:
        """
        Flip attack does not change the input during training.
        """
        return X

    def __str__(self):
        return f""""Flip attack: {self.flips}"""