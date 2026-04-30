import pytest
from SQLConnections.DatabaseService import DatabaseService
from game_logic.ruleset import Ruleset


@pytest.fixture
def db():
    service = DatabaseService()
    yield service
    service.close()

@pytest.fixture(autouse=True)
def cleanup_db():
    service = DatabaseService()
    yield

    # Delete data in correct order (respect foreign keys)
    service.db.execute("DELETE FROM Moves")
    service.db.execute("DELETE FROM GameHistory")
    service.db.execute("DELETE FROM FriendsList")
    service.db.execute("DELETE FROM Games")
    service.db.execute("DELETE FROM Users")
    service.db.commit()

    service.close()


def unique_name(prefix):
    import uuid
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def create_test_user(db, prefix="testuser"):
    username = unique_name(prefix)
    password = "Password123"
    email = f"{username}@test.com"

    success, user = db.sign_up(username, password, email)

    assert success is True
    return user, username, password, email


def test_sign_up_creates_user(db):
    user, username, password, email = create_test_user(db)

    assert user["username"] == username
    assert user["email"] == email
    assert user["password"] != password


def test_duplicate_username_rejected(db):
    user, username, password, email = create_test_user(db)

    success, result = db.sign_up(username, "OtherPass123", "other@test.com")

    assert success is False
    assert result == "Username Exists"


def test_login_correct_password_success(db):
    user, username, password, email = create_test_user(db)

    logged_in_user, error = db.log_in(username, password)

    assert logged_in_user is not None
    assert error is None
    assert logged_in_user["username"] == username


def test_login_wrong_password_rejected(db):
    user, username, password, email = create_test_user(db)

    logged_in_user, error = db.log_in(username, "WrongPassword")

    assert logged_in_user is None
    assert error == "Incorrect Password"


def test_password_is_hashed(db):
    user, username, password, email = create_test_user(db)

    saved_user, error = db.get_user_by_id(user["user_id"])

    assert saved_user is not None
    assert saved_user["password"] != password
    assert saved_user["salt"] is not None


def test_change_password(db):
    user, username, password, email = create_test_user(db)

    success, error = db.change_password(user["user_id"], password, "NewPassword123")

    assert success is True

    logged_in_user, error = db.log_in(username, "NewPassword123")

    assert logged_in_user is not None
    assert error is None


def test_change_username(db):
    user, username, password, email = create_test_user(db)
    new_username = unique_name("newname")

    success, error = db.change_username(user["user_id"], new_username)

    assert success is True

    saved_user, error = db.get_user_by_id(user["user_id"])

    assert saved_user["username"] == new_username


def test_delete_user(db):
    user, username, password, email = create_test_user(db)

    success, error = db.delete_user(user["user_id"])

    assert success is True

    saved_user, error = db.get_user_by_id(user["user_id"])

    assert saved_user is None
    assert error == "User Not Found"


def test_create_game_stores_ruleset_and_seed(db):
    ruleset = Ruleset({"num_decks": 3})
    seed = 12345

    success, game_id = db.create_game(ruleset, seed)

    assert success is True

    success, game = db.get_game(game_id)

    assert success is True
    assert game["game_id"] == game_id
    assert game["status"] == "In Lobby"
    assert game["seed"] == seed


def test_get_ruleset_returns_saved_ruleset(db):
    ruleset = Ruleset({"num_decks": 3, "min_meld_size": 4})

    success, game_id = db.create_game(ruleset, 999)

    assert success is True

    success, saved_ruleset = db.get_ruleset(game_id)

    assert success is True
    assert saved_ruleset["num_decks"] == 3
    assert saved_ruleset["min_meld_size"] == 4


def test_pause_game_changes_status(db):
    ruleset = Ruleset()

    success, game_id = db.create_game(ruleset, 111)
    assert success is True

    success, error = db.pause_game(game_id)
    assert success is True

    success, status = db.get_game_status(game_id)

    assert success is True
    assert status == "Paused"


def test_add_player_to_game_creates_history_record(db):
    user, username, password, email = create_test_user(db)
    ruleset = Ruleset()

    success, game_id = db.create_game(ruleset, 222)
    assert success is True

    success, error = db.add_player_to_game(user["user_id"], game_id, "Player")

    assert success is True

    success, history = db.get_player_history(user["user_id"])

    assert success is True
    assert any(row["game_id"] == game_id for row in history)


def test_record_game_result_updates_history(db):
    user, username, password, email = create_test_user(db)
    ruleset = Ruleset()

    success, game_id = db.create_game(ruleset, 333)
    assert success is True

    db.add_player_to_game(user["user_id"], game_id, "Player")

    success, error = db.record_game_result(user["user_id"], game_id, "Won")

    assert success is True

    success, history = db.get_player_history(user["user_id"])

    assert success is True
    assert any(row["game_id"] == game_id and row["result"] == "Won" for row in history)


def test_add_move_stores_move(db):
    user, username, password, email = create_test_user(db)
    ruleset = Ruleset()

    success, game_id = db.create_game(ruleset, 444)
    assert success is True

    success, move_id = db.add_move(game_id, user["user_id"], "Draw_Deck")

    assert success is True
    assert move_id is not None


def test_get_moves_returns_moves_in_order(db):
    user, username, password, email = create_test_user(db)
    ruleset = Ruleset()

    success, game_id = db.create_game(ruleset, 555)
    assert success is True

    db.add_move(game_id, user["user_id"], "Draw_Deck")
    db.add_move(game_id, user["user_id"], "Discard")

    success, moves = db.get_moves(game_id)

    assert success is True
    assert len(moves) == 2
    assert moves[0]["move_number"] == 1
    assert moves[1]["move_number"] == 2


def test_get_move_count(db):
    user, username, password, email = create_test_user(db)
    ruleset = Ruleset()

    success, game_id = db.create_game(ruleset, 666)
    assert success is True

    db.add_move(game_id, user["user_id"], "Draw_Deck")
    db.add_move(game_id, user["user_id"], "Discard")

    success, count = db.get_move_count(game_id)

    assert success is True
    assert count == 2


def test_send_friend_request(db):
    user1, username1, password1, email1 = create_test_user(db, "friend_a")
    user2, username2, password2, email2 = create_test_user(db, "friend_b")

    success, error = db.send_friend_request(user1["user_id"], user2["user_id"])

    assert success is True


def test_accept_friend_request(db):
    user1, username1, password1, email1 = create_test_user(db, "friend_a")
    user2, username2, password2, email2 = create_test_user(db, "friend_b")

    db.send_friend_request(user1["user_id"], user2["user_id"])

    success, error = db.accept_friend_request(user1["user_id"], user2["user_id"])

    assert success is True

    success, friends = db.get_friends(user1["user_id"])

    assert success is True
    assert any(friend["user_id"] == user2["user_id"] for friend in friends)


def test_reject_friend_request(db):
    user1, username1, password1, email1 = create_test_user(db, "friend_a")
    user2, username2, password2, email2 = create_test_user(db, "friend_b")

    db.send_friend_request(user1["user_id"], user2["user_id"])

    success, error = db.reject_friend_request(user1["user_id"], user2["user_id"])

    assert success is True

    success, pending = db.get_pending_requests(user1["user_id"])

    assert success is False
    assert pending == "No Pending Requests"


def test_get_friends_returns_only_accepted_friends(db):
    user1, username1, password1, email1 = create_test_user(db, "friend_a")
    user2, username2, password2, email2 = create_test_user(db, "friend_b")
    user3, username3, password3, email3 = create_test_user(db, "friend_c")

    db.send_friend_request(user1["user_id"], user2["user_id"])
    db.accept_friend_request(user1["user_id"], user2["user_id"])

    db.send_friend_request(user1["user_id"], user3["user_id"])

    success, friends = db.get_friends(user1["user_id"])

    assert success is True
    assert any(friend["user_id"] == user2["user_id"] for friend in friends)
    assert all(friend["user_id"] != user3["user_id"] for friend in friends)