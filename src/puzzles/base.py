from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")  # board / puzzle state
S = TypeVar("S")  # solution type


class PuzzleGenerator(ABC, Generic[T]):
    """Contract every puzzle generator must satisfy."""

    @abstractmethod
    def generate(self) -> T: ...


class PuzzleSolver(ABC, Generic[T, S]):
    """Contract every puzzle solver must satisfy."""

    @abstractmethod
    def solve(self) -> Optional[S]: ...
