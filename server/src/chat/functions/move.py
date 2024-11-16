def move(data, area: int) -> dict:
    cordinates_dict = {
        "x": data["x"],
        "y": data["y"]
    }

    if data["typeOfMovement"] == "up":
        if not cordinates_dict["y"] >= area:
            cordinates_dict["y"] += 1
    elif data["typeOfMovement"] == "down":
        if not cordinates_dict["y"] <= 0:
            cordinates_dict["y"] -= 1
    elif data["typeOfMovement"] == "left":
        if not cordinates_dict["x"] <= 0:
            cordinates_dict["x"] -= 1
    elif data["typeOfMovement"] == "right":
        if not cordinates_dict["x"] >= area:
            cordinates_dict["x"] += 1

    return {
        "x": str(cordinates_dict["x"]),
        "y": str(cordinates_dict["y"]),
        "typeOfMovement": data["typeOfMovement"],
        "type": "move"
    }
