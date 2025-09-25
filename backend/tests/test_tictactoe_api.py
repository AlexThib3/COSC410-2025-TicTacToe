from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.tictactoe.router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_create_and_get_game():
    r = client.post("/tictactoe/new")
    assert r.status_code == 200
    data = r.json()
    gid = data["id"]
    assert "current_player" not in data  # No longer in response

    r = client.get(f"/tictactoe/{gid}")
    assert r.status_code == 200
    data2 = r.json()
    assert data2["id"] == gid
    assert data2["board"] == [None]*9

def test_make_move_and_win_flow():
    r = client.post("/tictactoe/new")
    gid = r.json()["id"]

    # X at 0
    r = client.post(f"/tictactoe/{gid}/move", json={"index": 0, "player": "X"})
    assert r.status_code == 200
    # O at 3
    r = client.post(f"/tictactoe/{gid}/move", json={"index": 3, "player": "O"})
    assert r.status_code == 200
    # X at 1
    r = client.post(f"/tictactoe/{gid}/move", json={"index": 1, "player": "X"})
    assert r.status_code == 200
    # O at 4
    r = client.post(f"/tictactoe/{gid}/move", json={"index": 4, "player": "O"})
    assert r.status_code == 200
    # X at 2 -> win
    r = client.post(f"/tictactoe/{gid}/move", json={"index": 2, "player": "X"})
    assert r.status_code == 200
    data = r.json()
    assert data["winner"] == "X"
    assert data["status"].startswith("X wins")

def test_bad_requests():
    r = client.post("/tictactoe/new")
    gid = r.json()["id"]

    r = client.post(f"/tictactoe/{gid}/move", json={"index": 99, "player": "X"})
    assert r.status_code == 400
    assert "Index must be in range" in r.json()["detail"]

    # occupy 0 then try again
    client.post(f"/tictactoe/{gid}/move", json={"index": 0, "player": "X"})
    r = client.post(f"/tictactoe/{gid}/move", json={"index": 0, "player": "O"})
    assert r.status_code == 400
    assert "Cell already occupied" in r.json()["detail"]


def test_four_corners_api_win():
    """Test the four corners win condition through the API"""
    r = client.post("/tictactoe/new")
    gid = r.json()["id"]

    # X takes all four corners
    moves = [
        (0, "X"), (1, "O"), (2, "X"), (3, "O"),
        (6, "X"), (4, "O"), (8, "X")
    ]

    for pos, player in moves:
        r = client.post(f"/tictactoe/{gid}/move", json={"index": pos, "player": player})
        assert r.status_code == 200

    # Check that X won
    data = r.json()
    assert data["winner"] == "X"
    assert not data["is_draw"]


def test_api_status_messages():
    """Test status messages through API"""
    # Test initial status
    r = client.post("/tictactoe/new")
    gid = r.json()["id"]
    assert r.json()["status"] == "waiting for move"

    # Test win status
    moves = [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")]
    for pos, player in moves:
        r = client.post(f"/tictactoe/{gid}/move", json={"index": pos, "player": player})

    data = r.json()
    assert data["status"] == "X wins"


def test_api_draw_status():
    """Test draw status through API"""
    r = client.post("/tictactoe/new")
    gid = r.json()["id"]

    # Create a draw
    moves = [(0, "X"), (1, "O"), (2, "X"), (5, "O"), (3, "X"), (6, "O"), (4, "X"), (8, "O"), (7, "X")]
    for pos, player in moves:
        r = client.post(f"/tictactoe/{gid}/move", json={"index": pos, "player": player})

    data = r.json()
    assert data["status"] == "draw"
    assert data["is_draw"] is True
    assert data["winner"] is None