from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Needed for session

@app.route('/')
def index():
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0
    return render_template("index.html")

@app.route('/guess', methods=['POST'])
def guess():
    user_guess = int(request.json['guess'])
    session["attempts"] += 1
    number = session["number"]
    attempts = session["attempts"]

    if attempts >= 5 and user_guess != number:
        revealed_number = number
        session.pop("number", None)
        session.pop("attempts", None)
        return jsonify({
            "result": f"❌ Game Over! The number was {revealed_number}.",
            "status": "reveal",
            "gameOver": True
        })

    if user_guess < number:
        return jsonify({"result": f"Attempt {attempts}: Too low! 🔽", "status": "low"})
    elif user_guess > number:
        return jsonify({"result": f"Attempt {attempts}: Too high! 🔼", "status": "high"})
    else:
        session.pop("number", None)
        session.pop("attempts", None)
        return jsonify({
            "result": f"🎉 Correct! You guessed it in {attempts} attempts.",
            "status": "correct",
            "gameOver": True
        })

@app.route('/reset', methods=['POST'])
def reset():
    session["number"] = random.randint(1, 100)
    session["attempts"] = 0
    return jsonify({"message": "Game reset!"})

if __name__ == '__main__':
    app.run(debug=True)
