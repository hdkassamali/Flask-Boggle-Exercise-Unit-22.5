from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config["TESTING"] = True


class FlaskTests(TestCase):

    def test_boggle_board_creation(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<section id="boggle_board">', html)
            self.assertTrue(session["board"])

    def test_statistics_creation(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<p>Games Played: <span id='games_played'>", html)
            self.assertIn("<p>Highest Score: <span id='highest_score'>", html)

    def test_statistics_tracking(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session["games_played"] = 10
                session["highest_score"] = 45

            res = client.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session["games_played"], 10)
            self.assertEqual(session["highest_score"], 45)

    def test_user_guess(self):
        with app.test_client() as client:
            res = client.post("/get_guess", json={"user_guess": "ball"})
            data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["result"], "not-on-board")
            self.assertEqual(data["guess"], "ball")

    def test_update_game_stats(self):
        with app.test_client() as client:
            res = client.post("/game_stats", json={"score": 25})
            data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["games_played"], 1)
            self.assertEqual(data["highest_score"], 25)

            with client.session_transaction() as session:
                self.assertEqual(session["games_played"], 1)
                self.assertEqual(session["highest_score"], 25)

            res = client.post("/game_stats", json={"score": 30})
            data = res.get_json()

            self.assertEqual(data['games_played'], 2)
            self.assertEqual(data['highest_score'], 30)

            with client.session_transaction() as session:
                self.assertEqual(session['games_played'], 2)
                self.assertEqual(session['highest_score'], 30)

            res = client.post('/game_stats', json={'score': 15})
            data = res.get_json()

            self.assertEqual(data['games_played'], 3)
            self.assertEqual(data['highest_score'], 30)

            with client.session_transaction() as session:
                self.assertEqual(session['games_played'], 3)
                self.assertEqual(session['highest_score'], 30)
