import json
from chat.functions.move_player import move_player as move_player_func
from chat.typedef import MessageFromClient, MessageToClient



def message_from_client(message: str) -> MessageFromClient:
    try:
      data = json.loads(message)
      return MessageFromClient(type=data["type"], payload=data["payload"])
    except json.JSONDecodeError:
      raise ValueError("Non-JSON message")


def message_to_client(message: MessageFromClient) -> str:
    message_result:MessageToClient
    if message.type == "move":
        position = move_player_func(message.payload, 500)
        message_result=MessageToClient(type=message.type, position=position)
    elif message.type == "click":
        message_result=MessageToClient(type=message.type, position=message.payload["position"])
    else:
        message_result=MessageToClient(type=message.type, message=message.payload)

    return json.dumps({
        "type": message_result.type,
        "position": message_result.position,
        "message": message_result.message
    })