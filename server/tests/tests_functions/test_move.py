from chat.functions.move import move

def test_move():
    assert move({"x": 0, "y": 0}, "up") == {"x": 0, "y": 1}


def test_move_area():
    assert move({"x": 0, "y": 0}, "up", 500) == {"x": 0, "y": 1}
