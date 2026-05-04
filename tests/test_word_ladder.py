from __future__ import annotations

import pytest

from src.puzzles.word_ladder import WordLadderGenerator, WordLadderSolver


class TestWordLadderGenerator:
    def test_produces_correct_word_count(self):
        _, _, words = WordLadderGenerator(10, 4).generate()
        assert len(words) == 10

    def test_all_words_have_correct_length(self):
        _, _, words = WordLadderGenerator(8, 6).generate()
        assert all(len(w) == 6 for w in words)

    def test_start_and_end_are_first_and_last(self):
        start, end, words = WordLadderGenerator(15, 5).generate()
        assert start == words[0]
        assert end == words[-1]

    def test_consecutive_words_differ_by_one_char(self):
        _, _, words = WordLadderGenerator(12, 5).generate()
        for w1, w2 in zip(words, words[1:]):
            diffs = sum(c1 != c2 for c1, c2 in zip(w1, w2))
            assert diffs == 1, f"'{w1}' → '{w2}' differs by {diffs} chars"


class TestWordLadderSolver:
    def test_direct_neighbors_solved_in_one_step(self):
        words = ["abcde", "xbcde"]
        path = WordLadderSolver("abcde", "xbcde", words).solve()
        assert path == ["abcde", "xbcde"]

    def test_known_chain_finds_shortest_path(self):
        words = ["abcde", "abcdf", "abcef", "avcef"]
        path = WordLadderSolver("abcde", "avcef", words).solve()
        assert path is not None
        assert path[0] == "abcde"
        assert path[-1] == "avcef"
        for w1, w2 in zip(path, path[1:]):
            diffs = sum(c1 != c2 for c1, c2 in zip(w1, w2))
            assert diffs == 1

    def test_returns_none_when_no_path_exists(self):
        path = WordLadderSolver("aaaaa", "zzzzz", ["aaaaa", "zzzzz"]).solve()
        assert path is None

    def test_start_not_in_vocab_returns_none(self):
        path = WordLadderSolver("xxxxx", "abcde", ["abcde"]).solve()
        assert path is None

    def test_end_not_in_vocab_returns_none(self):
        path = WordLadderSolver("abcde", "xxxxx", ["abcde"]).solve()
        assert path is None

    def test_generated_puzzle_is_solvable(self):
        # The generator always builds a chain, so a path must exist
        start, end, words = WordLadderGenerator(20, 5).generate()
        path = WordLadderSolver(start, end, words).solve()
        assert path is not None
        assert path[0] == start
        assert path[-1] == end
