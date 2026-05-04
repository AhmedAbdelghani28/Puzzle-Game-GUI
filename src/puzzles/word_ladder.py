from __future__ import annotations

import random
import string
from collections import deque
from typing import List, Optional, Tuple

from src.puzzles.base import PuzzleGenerator, PuzzleSolver

WordList = List[str]
Path = List[str]


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class WordLadderGenerator(PuzzleGenerator[Tuple[str, str, WordList]]):
    """Produces (start, end, word_list) by building a chain of single-letter
    mutations, ensuring at least one valid transformation path always exists."""

    def __init__(self, num_words: int = 20, word_length: int = 5) -> None:
        self.num_words = num_words
        self.word_length = word_length

    def generate(self) -> Tuple[str, str, WordList]:
        chain = self._build_chain()
        return chain[0], chain[-1], chain

    def _build_chain(self) -> WordList:
        current = "".join(random.choices(string.ascii_lowercase, k=self.word_length))
        chain = [current]
        for _ in range(self.num_words - 1):
            current = self._mutate(current)
            chain.append(current)
        return chain

    def _mutate(self, word: str) -> str:
        idx = random.randrange(len(word))
        alphabet_without_current = string.ascii_lowercase.replace(word[idx], "")
        new_char = random.choice(alphabet_without_current)
        return word[:idx] + new_char + word[idx + 1:]


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------

class WordLadderSolver(PuzzleSolver[Tuple[str, str, WordList], Path]):
    """BFS solver — guarantees the shortest transformation path."""

    def __init__(self, start: str, end: str, word_list: WordList) -> None:
        self.start = start
        self.end = end
        self.vocab: set[str] = set(word_list)

    def solve(self) -> Optional[Path]:
        if self.start not in self.vocab or self.end not in self.vocab:
            return None

        queue: deque[Path] = deque([[self.start]])
        visited: set[str] = {self.start}

        while queue:
            path = queue.popleft()
            word = path[-1]
            if word == self.end:
                return path
            for neighbor in self._neighbors(word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None

    def _neighbors(self, word: str) -> List[str]:
        return [
            word[:i] + ch + word[i + 1:]
            for i in range(len(word))
            for ch in string.ascii_lowercase
            if ch != word[i] and word[:i] + ch + word[i + 1:] in self.vocab
        ]
