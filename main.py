from flask import Flask, redirect, url_for, render_template, jsonify, request
from manage import manager

app = Flask(__name__, static_url_path="/static")
app.register_blueprint(manager)
app.secret_key = "lkj()984kljl;:LKJF?.a<faskdjkl"

if __name__ == "__main__":
    app.run(threaded=True, debug=True)
