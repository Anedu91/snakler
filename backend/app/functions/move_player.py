
def move_player(player_data: dict[str, any], area: int) -> dict[str, int]:
    kind_of_direction = player_data["direction"]
    position = player_data["position"]
    if kind_of_direction == "up":
        if not position["y"] <= 0:
            position["y"] -= 1
    elif kind_of_direction == "down":
        if not position["y"] >= area:
            position["y"] += 1
    elif kind_of_direction == "left":
        if not position["x"] <= 0:
            position["x"] -= 1
    elif kind_of_direction == "right":
        if not position["x"] >= area:
            position["x"] += 1

    return position