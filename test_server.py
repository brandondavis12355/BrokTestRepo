"""
Tic Tac Toe — server turn-order tests.

The page fixes the symbols (player = O, AI = X); only who moves first is chosen.
Run: python -m pytest test_server.py -v
"""

import unittest

import server as srv


class TestTurnOrder(unittest.TestCase):
    def setUp(self):
        srv.app.config["TESTING"] = True
        self.client = srv.app.test_client()
        srv._ai_difficulty = "easy"

    def tearDown(self):
        srv._player_goes_first = False
        srv._reset_state()

    def choose(self, choice):
        self.client.post("/api/turn-order", json={"choice": choice})
        return self.client.post("/api/new-game").get_json()

    def test_player_first_means_the_player_moves_first(self):
        state = self.choose("player")
        self.assertEqual(state["current_player"], srv.PLAYER_SYMBOL)
        self.assertTrue(state["player_first"])

    def test_ai_first_means_the_ai_moves_first(self):
        state = self.choose("ai")
        self.assertEqual(state["current_player"], srv.AI_SYMBOL)
        self.assertFalse(state["player_first"])

    def test_player_first_can_move_and_the_ai_answers(self):
        self.choose("player")
        resp = self.client.post("/api/move", json={"cell": 5})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["board"][4], srv.PLAYER_SYMBOL)
        self.assertEqual(data["board"].count(srv.AI_SYMBOL), 1, "the AI replied once")
        self.assertEqual(data["current_player"], srv.PLAYER_SYMBOL, "and it is the player's turn again")

    def test_player_cannot_move_when_the_ai_goes_first(self):
        self.choose("ai")
        resp = self.client.post("/api/move", json={"cell": 5})
        self.assertEqual(resp.status_code, 400)

    def test_ai_first_the_ai_moves_then_the_player_moves(self):
        self.choose("ai")
        resp = self.client.post("/api/ai-move")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["board"].count(srv.AI_SYMBOL), 1)
        self.assertEqual(data["current_player"], srv.PLAYER_SYMBOL)
        free = data["board"].index(None) + 1
        resp = self.client.post("/api/move", json={"cell": free})
        self.assertEqual(resp.status_code, 200)

    def test_ai_cannot_move_when_the_player_goes_first(self):
        self.choose("player")
        resp = self.client.post("/api/ai-move")
        self.assertEqual(resp.status_code, 400)

    def test_turn_order_survives_new_games(self):
        self.client.post("/api/turn-order", json={"choice": "player"})
        for _ in range(3):
            state = self.client.post("/api/new-game").get_json()
            self.assertEqual(state["current_player"], srv.PLAYER_SYMBOL)

    def test_bad_choice_is_rejected(self):
        for bad in ("Player", "AI", "", "x"):
            resp = self.client.post("/api/turn-order", json={"choice": bad})
            self.assertEqual(resp.status_code, 400, bad)


if __name__ == "__main__":
    unittest.main()
