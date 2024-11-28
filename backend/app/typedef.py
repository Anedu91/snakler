from dataclasses import dataclass
from typing import Literal


@dataclass
class Position:
    x: int
    y: int

MessageType = Literal["move", "click", "message"]

@dataclass(frozen=True)
class MessageFromClient:
    type: MessageType
    payload: dict[str, str]

@dataclass(frozen=True)
class MessageToClient:
    type: MessageType
    position: Position | None = None
    message: str | None = None



DirectionType = Literal["up", "down", "left", "right"]


@dataclass
class MoveData:
    direction: DirectionType
    x: int
    y: int
