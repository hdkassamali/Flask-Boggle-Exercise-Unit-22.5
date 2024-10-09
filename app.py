from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify


app = Flask(__name__)
app.config["SECRET_KEY"] = "abc123"
app.debug = True

boggle_game = Boggle()


@app.route("/")
def display_board():
    """Display the Boggle board and the current game statistics."""
    board = boggle_game.make_board()
    session["board"] = board
    games_played = session.get("games_played", 0)
    highest_score = session.get("highest_score", 0)
    return render_template(
        "board.html",
        board=board,
        games_played=games_played,
        highest_score=highest_score,
    )


@app.route("/get_guess", methods=["POST"])
def get_user_guess():
    data = request.get_json()
    guess = data["user_guess"].lower()
    board = session["board"]
    result = boggle_game.check_valid_word(board, guess)

    return jsonify({"result": result, "guess": guess})


@app.route("/game_stats", methods=["POST"])
def update_game_stats():
    data = request.get_json()
    score = data["score"]

    if "games_played" not in session:
        session["games_played"] = 0
    session["games_played"] += 1

    if "highest_score" not in session:
        session["highest_score"] = 0
    if score > session["highest_score"]:
        session["highest_score"] = score

    return jsonify(
        {
            "games_played": session["games_played"],
            "highest_score": session["highest_score"],
        }
    )
