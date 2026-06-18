from flask import Flask, jsonify

from routes.user import users_blueprint

app = Flask(__name__)

app.register_blueprint(users_blueprint)


@app.route("/status")
def status():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run()
