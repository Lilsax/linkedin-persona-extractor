import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from introgen import fetch_person_data


app = Flask(__name__)


@app.route("/")
def index():
    # Minimal landing page to avoid missing template errors
    return (
        "<h1>IntroGen</h1>"
        "<p>Generate a short professional intro, highlights, and tailored ice-breakers for a candidate.</p>"
        "<p>Use: GET /process?name=\"Full Name and Title\"</p>"
    )


@app.route("/process", methods=["GET"])
def process():
    # Only support GET and read 'name' from query parameters
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Missing 'name' parameter"}), 400

    result = fetch_person_data(name=name)

    # Ensure we return JSON-serializable structure
    return jsonify(
        {
            "summary_and_facts": result.get("summary_and_facts", {}),
            "interests": result.get("interests", []),
            "ice_breakers": result.get("ice_breakers", []),
            "picture_url": result.get("profile_pic_url", ""),
        }
    )


if __name__ == "__main__":
    # Read port from environment (useful for changing port without editing code)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
