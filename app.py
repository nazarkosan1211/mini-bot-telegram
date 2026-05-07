from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database dummy sementara
users = {
    "user1": {"points": 100, "tasks": ["daily login", "check bot"]},
    "user2": {"points": 50, "tasks": ["daily login"]}
}

@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    user = users.get(username)
    if user:
        return jsonify({"status": "success", "data": user})
    return jsonify({"status": "error", "message": "User not found"}), 404

if __name__ == "__main__":
    # Railway nanti pakai port default, Flask otomatis baca PORT environment
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)