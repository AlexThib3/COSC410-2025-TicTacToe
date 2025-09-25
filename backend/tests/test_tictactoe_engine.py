import pytest
from app.tictactoe.engine import new_game, move, available_moves, status

def test_new_game_initial_state():
    gs = new_game()
    assert gs.board == [None]*9
    assert gs.winner is None
    assert gs.is_draw is False
    assert status(gs) == "waiting for move"

def test_valid_move_with_player():
    gs = new_game()
    gs = move(gs, 0, "X")
    assert gs.board[0] == "X"
    assert gs.winner is None
    assert not gs.is_draw

    gs = move(gs, 1, "O")
    assert gs.board[1] == "O"
    assert gs.winner is None
    assert not gs.is_draw

def test_cannot_play_occupied_cell():
    gs = new_game()
    gs = move(gs, 0, "X")
    with pytest.raises(ValueError):
        move(gs, 0, "O")

def test_winning_rows_cols_diagonals():
    # Row win
    gs = new_game()
    gs = move(gs, 0, "X")
    gs = move(gs, 3, "O")
    gs = move(gs, 1, "X")
    gs = move(gs, 4, "O")
    gs = move(gs, 2, "X")  # X wins
    assert gs.winner == "X"

    # Column win
    gs = new_game()
    gs = move(gs, 0, "X")
    gs = move(gs, 1, "O")
    gs = move(gs, 3, "X")
    gs = move(gs, 2, "O")
    gs = move(gs, 6, "X")  # X wins
    assert gs.winner == "X"

    # Diagonal win
    gs = new_game()
    gs = move(gs, 0, "X")
    gs = move(gs, 1, "O")
    gs = move(gs, 4, "X")
    gs = move(gs, 2, "O")
    gs = move(gs, 8, "X")  # X wins
    assert gs.winner == "X"

def test_draw_condition():
    gs = new_game()
    # X O X
    # X X O
    # O X O
    # sequence crafted to avoid earlier wins
    moves = [(0, "X"), (1, "O"), (2, "X"), (5, "O"), (3, "X"), (6, "O"), (4, "X"), (8, "O"), (7, "X")]
    for pos, player in moves:
        gs = move(gs, pos, player)
    assert gs.is_draw is True
    assert gs.winner is None

def test_available_moves_updates():
    gs = new_game()
    assert set(available_moves(gs)) == set(range(9))
    gs = move(gs, 4, "X")
    assert 4 not in available_moves(gs)
    assert len(available_moves(gs)) == 8

def test_game_over_disallows_moves():
    gs = new_game()
    gs = move(gs, 0, "X")
    gs = move(gs, 3, "O")
    gs = move(gs, 1, "X")
    gs = move(gs, 4, "O")
    gs = move(gs, 2, "X")  # X wins
    with pytest.raises(ValueError):
        move(gs, 8, "O")


def test_four_corners_win():
    """Test the special four corners win condition"""
    gs = new_game()
    # X takes all four corners
    gs = move(gs, 0, "X")  # corner
    gs = move(gs, 1, "O")  # center
    gs = move(gs, 2, "X")  # corner
    gs = move(gs, 3, "O")  # edge
    gs = move(gs, 6, "X")  # corner
    gs = move(gs, 4, "O")  # center
    gs = move(gs, 8, "X")  # corner - X should win with all four corners
    assert gs.winner == "X"
    assert not gs.is_draw


def test_invalid_move_indices():
    """Test that invalid indices raise appropriate errors"""
    gs = new_game()

    # Test negative index
    with pytest.raises(IndexError):
        move(gs, -1, "X")

    # Test index too large
    with pytest.raises(IndexError):
        move(gs, 9, "X")

    # Test index way too large
    with pytest.raises(IndexError):
        move(gs, 100, "X")


def test_invalid_players():
    """Test that only X and O are valid players"""
    gs = new_game()

    # This would fail type checking in a real implementation
    # but let's test the existing constraints
    with pytest.raises(Exception):  # Could be TypeError or other validation
        move(gs, 0, "Y")  # type: ignore


def test_game_state_copy():
    """Test that GameState.copy() works correctly"""
    gs = new_game()
    gs = move(gs, 0, "X")
    gs = move(gs, 1, "O")

    gs_copy = gs.copy()

    # Should be equal but not the same object
    assert gs.board == gs_copy.board
    assert gs.winner == gs_copy.winner
    assert gs.is_draw == gs_copy.is_draw
    assert gs is not gs_copy
    assert gs.board is not gs_copy.board


def test_status_messages():
    """Test all possible status messages"""
    gs = new_game()
    assert status(gs) == "waiting for move"

    # Test X win
    gs = move(gs, 0, "X")
    gs = move(gs, 3, "O")
    gs = move(gs, 1, "X")
    gs = move(gs, 4, "O")
    gs = move(gs, 2, "X")
    assert status(gs) == "X wins"

    # Test O win
    gs = new_game()
    gs = move(gs, 0, "O")
    gs = move(gs, 3, "X")
    gs = move(gs, 1, "O")
    gs = move(gs, 4, "X")
    gs = move(gs, 2, "O")
    assert status(gs) == "O wins"

    # Test draw
    gs = new_game()
    moves = [(0, "X"), (1, "O"), (2, "X"), (5, "O"), (3, "X"), (6, "O"), (4, "X"), (8, "O"), (7, "X")]
    for pos, player in moves:
        gs = move(gs, pos, player)
    assert status(gs) == "draw"


def test_available_moves_comprehensive():
    """Test available_moves in various scenarios"""
    gs = new_game()

    # All moves available initially
    assert len(available_moves(gs)) == 9

    # After one move
    gs = move(gs, 4, "X")
    assert len(available_moves(gs)) == 8
    assert 4 not in available_moves(gs)

    # After multiple moves
    gs = move(gs, 0, "O")
    gs = move(gs, 8, "X")
    assert len(available_moves(gs)) == 6
    assert 0 not in available_moves(gs)
    assert 4 not in available_moves(gs)
    assert 8 not in available_moves(gs)

    # After game ends, no moves available (though game state prevents moves anyway)
    gs = new_game()
    gs = move(gs, 0, "X")
    gs = move(gs, 3, "O")
    gs = move(gs, 1, "X")
    gs = move(gs, 4, "O")
    gs = move(gs, 2, "X")  # X wins
    # available_moves still works even though moves aren't allowed
    assert len(available_moves(gs)) == 6


def test_edge_case_wins():
    """Test edge cases for wins"""
    # Test O winning with four corners
    gs = new_game()
    gs = move(gs, 0, "O")
    gs = move(gs, 1, "X")
    gs = move(gs, 2, "O")
    gs = move(gs, 3, "X")
    gs = move(gs, 6, "O")
    gs = move(gs, 4, "X")
    gs = move(gs, 8, "O")
    assert gs.winner == "O"

    # Test that three corners don't win
    gs = new_game()
    gs = move(gs, 0, "X")
    gs = move(gs, 2, "X")
    gs = move(gs, 6, "X")
    # Missing corner 8, should not be a win
    assert gs.winner is None
    assert not gs.is_draw