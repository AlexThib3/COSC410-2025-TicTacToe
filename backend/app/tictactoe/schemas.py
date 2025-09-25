from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

Player = Literal["X", "O"]


class GameStateDTO(BaseModel):
    id: str
    board: list[Player | None]
    winner: Player | None
    is_draw: bool
    status: str


class MoveRequest(BaseModel):
    index: int
    player: Player
