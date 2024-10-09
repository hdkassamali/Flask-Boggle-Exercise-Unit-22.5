class BoggleGame {
  constructor() {
    this.score = 0;
    this.playedWords = new Set();
    this.timer = null;
    this.timeLeft = 60;
    this.startTimer();
  }

  startTimer() {
    this.timer = setInterval(() => {
      this.timeLeft--;
      $("#timer").text(`Time Left: ${this.timeLeft}`);

      if (this.timeLeft <= 0) {
        this.endGame();
      }
    }, 1000);
  }

  endGame() {
    clearInterval(this.timer);
    $("#timer").text("Game Over");
    $("#guess_form").find("input, button").attr("disabled", true);
    $("#result_message").text("Time's up! No more guesses.");
    $("#score").text(`Final Score: ${this.score}`);

    this.sendGameStats();
  }

  async sendGameStats() {
    try {
      const response = await axios.post("/game_stats", {
        score: this.score,
      });

      $("#games_played").text(response.data.games_played);
      $("#highest_score").text(response.data.highest_score);
    } catch (error) {
      console.error("Error sending game stats:", error);
    }
  }

  async sendGuess(guess) {
    if (this.playedWords.has(guess)) {
      $("#result_message").text("You already guessed that word!");
      return;
    }
    try {
      const response = await axios.post("/get_guess", { user_guess: guess });

      const result = response.data.result;

      if (result === "ok") {
        this.score += guess.length;
        this.playedWords.add(guess);
        $("#score").text(`Current Score: ${this.score}`);
        $("#result_message").text("Great! The word is valid and on the board.");
      } else if (result === "not-on-board") {
        $("#result_message").text("Sorry, that word is not on the board.");
      } else {
        $("#result_message").text("That's not a valid word.");
      }
    } catch (error) {
      console.error("Error sending guess:", error);
    }
  }
}

$(document).ready(() => {
  const game = new BoggleGame();

  $("#guess_form").on("submit", (event) => {
    event.preventDefault();
    const userGuess = $("#guess").val();
    $("#guess").val("");
    game.sendGuess(userGuess);
  });
});
