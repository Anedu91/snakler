from dataclasses import dataclass
from enum import Enum
from typing import Literal

class ClientRole(Enum):
    CLICKER = "clicker"    # Can send click messages
    MOVER = "mover"      # Can send move messages
    VIEWER = "viewer"    # Can only send regular messages

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
