from flask import Flask, redirect, url_for, render_template, jsonify, request
from manage import manager
import query

app = Flask(__name__, static_url_path="/static")

app.register_blueprint(manager)
app.secret_key = "lkj()984kljl;:LKJF?.a<faskdjkl"

@app.route("/", methods=["GET"])
def view_only():
    articles = query.view_articles()
    return render_template("/view_only.html", articles=articles)

if __name__ == "__main__":
    app.run(threaded=True, debug=True)
