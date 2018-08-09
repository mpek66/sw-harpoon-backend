from flask import Flask, redirect, url_for, render_template, jsonify, request
from manage import manager
from query import fetcher, get_article_titles
from git import Repo

app = Flask(__name__, static_url_path="/static")

app.register_blueprint(fetcher)
app.secret_key = "lkj()984kljl;:LKJF?.a<faskdjkl"

@app.route("/", methods=["GET"])
def view_only():
    articles = get_article_titles()
    return render_template("/view_only.html", articles=articles)

if __name__ == "__main__":
    repo = Repo(".")
    #REMOVE LATER, WE WANT IT TO CRASH WITHOUT ABILITY TO PULL
    try:
        repo.git.pull()
    except Exception as e:
        print(e, type(e))
    app.register_blueprint(manager)
    app.run(threaded=True, debug=True)
