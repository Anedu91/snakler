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
        coordinates = move_player_func(message.payload, 500)
        message_result=MessageToClient(type=message.type, coordinates=coordinates)
    elif message.type == "click":
        message_result=MessageToClient(type=message.type, coordinates=message.payload)
    else:
        message_result=MessageToClient(type=message.type, message=message.payload)

    return json.dumps({
        "type": message_result.type,
        "coordinates": message_result.coordinates,
        "message": message_result.message
    })