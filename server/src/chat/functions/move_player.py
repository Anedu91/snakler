
def move_player(player_data: dict[str, any], area: int) -> dict[str, int]:
    kind_of_movement = player_data["movement"]
    if kind_of_movement == "up":
        if not player_data["y"] <= 0:
            player_data["y"] -= 1
    elif kind_of_movement == "down":
        if not player_data["y"] >= area:
            player_data["y"] += 1
    elif kind_of_movement == "left":
        if not player_data["x"] <= 0:
            player_data["x"] -= 1
    elif kind_of_movement == "right":
        if not player_data["x"] >= area:
            player_data["x"] += 1

    return {"x": player_data["x"], "y": player_data["y"]}