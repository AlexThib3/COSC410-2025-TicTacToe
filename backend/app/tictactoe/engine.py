from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

Player = Literal["X", "O"]
Cell = Optional[Player]

WIN_LINES: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),  # rows
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),  # cols
    (0, 4, 8),
    (2, 4, 6),  # diagonals
)


@dataclass
class GameState:
    board: list[Cell] = field(default_factory=lambda: [None] * 9)
    winner: Player | None = None
    is_draw: bool = False

    def copy(self) -> GameState:
        return GameState(self.board.copy(), self.winner, self.is_draw)


def _check_winner(board: list[Cell]) -> Player | None:
    for a, b, c in WIN_LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


def _is_full(board: list[Cell]) -> bool:
    return all(cell is not None for cell in board)


def new_game() -> GameState:
    return GameState()


def move(state: GameState, index: int, player: Player) -> GameState:
    if state.winner or state.is_draw:
        raise ValueError("Game is already over.")
    if not (0 <= index < 9):
        raise IndexError("Index must be in range [0, 8].")
    if state.board[index] is not None:
        raise ValueError("Cell already occupied.")

    next_state = state.copy()
    next_state.board[index] = player

    w = _check_winner(next_state.board)
    if w:
        next_state.winner = w
    elif _is_full(next_state.board):
        next_state.is_draw = True
    return next_state


def available_moves(state: GameState) -> list[int]:
    return [i for i, cell in enumerate(state.board) if cell is None]


def status(state: GameState) -> str:
    if state.winner:
        return f"{state.winner} wins"
    if state.is_draw:
        return "draw"
    return "waiting for move"
