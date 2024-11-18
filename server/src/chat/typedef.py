from dataclasses import dataclass
from typing import Literal


@dataclass
class Coordinates:
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
    coordinates: Coordinates | None = None
    message: str | None = None



MovementType = Literal["up", "down", "left", "right"]


@dataclass
class MoveData:
    movement: MovementType
    x: int
    y: int
