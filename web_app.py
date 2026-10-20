
from flask import Flask, request, jsonify, render_template
from engine.basic_engine import BasicEngine
from engine.film_engine import FilmEngine
import core.config as config
from core.tokenziner import tokenize, tokens_to_string
from utils.text_processing import clean_tokens

app = Flask(__name__)

engine_basic = BasicEngine(
    config.keys_basic,
    config.responses_basic
)

engine_film = FilmEngine(
    config.keys_film,
    config.list_film,
    config.responses_film
)

engines = [engine_basic, engine_film]


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    raw = str(data.get("message", "")).strip()

    if not raw:
        return jsonify({
            "response": "Ketik pesan dulu, ya."
        }), 400

    tokens = clean_tokens(tokenize(raw))
    msg = tokens_to_string(tokens)

    scores = [
        (engine, engine.get_score(msg))
        for engine in engines
    ]

    best_engine, best_score = max(
        scores, key=lambda item: item[1]
    )

    if best_score == 0:
        response = "Sorry, I don't understand."
    else:
        result = best_engine.process_input(msg)
        response = result.get("response") or "..."

    return jsonify({"response": response})


if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
