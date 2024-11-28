from app.functions.move_player import move_player, Coordinates, MoveData



AREA = 500
def test_move_top_left_corner():
    assert move_player(MoveData(coordinates=Coordinates(x=0, y=0),movement="up"), area=AREA) == {"x": 0, "y": 0}


def test_move_top_right_corner():
    assert move_player(MoveData(coordinates=Coordinates(x=AREA, y=0),movement="right"), area=AREA) == {"x": AREA, "y": 0}

def test_move_bottom_left_corner():
    assert move_player(MoveData(coordinates=Coordinates(x=0, y=AREA),movement="left"), area=AREA) == {"x": 0, "y": AREA}

def test_move_bottom_right_corner():
    assert move_player(MoveData(coordinates=Coordinates(x=AREA, y=AREA),movement="down"), area=AREA) == {"x": AREA, "y": AREA}

def test_move_center():
    assert move_player(MoveData(coordinates=Coordinates(x=AREA / 2, y=AREA / 2),movement="up"), area=AREA) == {"x": AREA / 2, "y": AREA / 2 - 1}