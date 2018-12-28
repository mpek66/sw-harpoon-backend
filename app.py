from flask import Flask, Blueprint, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

from forms import ArticleForm, EditArticleForm, RemoveArticleForm

import sys
from copy import copy
import json
import datetime

app = Flask(__name__, static_url_path="/static")
app.secret_key = "lkj()984kljl;:LKJF?.a<faskdjkl"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    date = db.Column(db.Date())
    author = db.Column(db.Text())
    image = db.Column(db.Text())
    caption = db.Column(db.Text())
    location = db.Column(db.Text())
    article = db.Column(db.Text())
    category = db.Column(db.Text())
    scope = db.Column(db.Text())

    def __repr__(self):
        return self.title

    def __init__(self, data):
        self.title = data['title']
        self.date = data['date']
        self.author = data['author']
        self.image = data['image']
        self.caption = data['caption']
        self.location = data['location']
        self.article = data['article']
        self.category = data['category']
        self.scope = data['scope']

#------------------------------------------------------------------------------#
#Database management
manager = Blueprint("manager", __name__, template_folder='templates')
def get_credential_name():
    return "test"
def get_credential_password():
    return "test"

@manager.route("/manage/", methods=["GET", "POST"])
def manage():
    return render_template("/manage.html")

@manager.route("/add_article/", methods=["GET", "POST"])
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        if form.name.data != get_credential_name() or form.password.data != get_credential_password():
            return render_template("/add_article.html", form=form)
        indata = Article(form.data)
        data = copy(indata.__dict__)
        del data["_sa_instance_state"]
        last = Article.query.order_by(Article.id.desc()).first()
        if last:
            indata.id = last.id + 1
        else:
            indata.id = 1
        try:
            db.session.add(indata)
            db.session.commit()
        except Exception as e:
            print("\n FAILED entry: {}\n".format(json.dumps(data)))
            print(e)
            sys.stdout.flush()
            return redirect(url_for("manager.errors", errors="\n FAILED entry: {}\n".format(json.dumps(data))))
        return redirect(url_for("manager.success"))
    return render_template("/add_article.html", form=form)

@manager.route("/edit_article/", methods=["GET", "POST"])
def edit_article():
    form = EditArticleForm()
    if form.validate_on_submit():
        if form.name.data != get_credential_name() or form.password.data != get_credential_password():
            return render_template("/edit_article.html", form=form)
        try:
            article = Article.query.get(form.id.data)
            for key in form.data:
                if key != "id" and key != "csrf_token" and form[key].data != "" and form[key].data != None:
                    setattr(article, key, form[key].data)
            db.session.commit()
        except Exception as e:
            print("\n FAILED entry: {}\n".format(json.dumps(form.data)))
            print(e)
            sys.stdout.flush()
            return redirect(url_for("manager.errors", errors="\n FAILED entry: {}\n".format(json.dumps(form.data))))
        return redirect(url_for("manager.success"))
    return render_template("/edit_article.html", form=form)

@manager.route("/remove_article/", methods=["GET", "POST"])
def remove_article():
    form = RemoveArticleForm()
    if form.validate_on_submit():
        if form.name.data != get_credential_name() or form.password.data != get_credential_password():
            return render_template("/remove_article.html", form=form)
        try:
            article = Article.query.get(form.id.data)
            db.session.delete(article)
            decrements = Article.query.filter(Article.id > form.id.data).order_by(Article.id.asc())
            for item in decrements:
                item.id -= 1
            db.session.commit()
        except Exception as e:
            print("\n FAILED entry: {}\n".format(json.dumps(form.data)))
            print(e)
            sys.stdout.flush()
            return redirect(url_for("manager.errors", errors="\n FAILED entry: {}\n".format(json.dumps(form.data))))
        return redirect(url_for("manager.success"))
    return render_template("/remove_article.html", form=form)

@manager.route("/success/", methods=["GET"])
def success():
    return render_template("/success.html")

@manager.route("/errors/", methods=["GET"])
def errors():
    problems = request.args.get("errors")
    return render_template("/errors.html", errors=problems)

app.register_blueprint(manager)

#------------------------------------------------------------------------------#
#Data fetching
fetcher = Blueprint("fetcher", __name__, template_folder='templates')

@fetcher.route("/view_articles/")
def view_articles():
    data = Article.query.order_by(Article.id).all()
    return render_template("view_articles.html", articles=data)

# routes to get shit
@fetcher.route("/get_article/<string:id>/", methods=["GET"])
def get_article_data(id):
    result = {
        "status": None,
        "data": None
    }
    try:
        num = float(id)
        article = Article.query.get(id)
        result["status"] = "SUCCESS"
        result["data"] = {
            "id": article.id,
            "title": article.title,
            "date": article.date,
            "author": article.author,
            "image": article.image,
            "caption": article.caption,
            "article": article.article,
            "category": article.category,
            "scope": article.scope
        }
        return jsonify(result)
    except Exception as e:
        result["status"] = "ERROR: can't get article data for id " + id
        result["data"] = repr(e)
        return jsonify(result)

# route to get articles
@fetcher.route("/get_articles/<string:type>/<string:value>/", methods=["GET"])
def get_articles(type, value):
    #some standardization to input
    type = type.lower()
    value = value.lower()
    result = {
        "status": None,
        "data": None
    }
    if type not in ["time", "author", "category", "scope"]:
        result["status"] = "ERROR: '" + type + "' is not a valid query type"
        result["data"] = None
        return jsonify(result)
    try:
        articles = None
        if type == "time":
            today = datetime.date.today()
            if value == "weekly":
                cutoff = today - datetime.timedelta(days=7)
                articles = Article.query.filter(Article.date >= str(cutoff)).order_by(Article.date.desc()).all()
            elif value == "monthly":
                cutoff = today.replace(day=1)
                articles = Article.query.filter(Article.date >= str(cutoff)).order_by(Article.date.desc()).all()
            elif value == "yearly":
                cutoff = today - datetime.timedelta(days=365)
                articles = Article.query.filter(Article.date >= str(cutoff)).order_by(Article.date.desc()).all()
            else:
                articles = Article.query.order_by(Article.date.desc()).all()
        elif type == "author":
            articles = Article.query.filter(Article.author == value).order_by(Article.id.desc()).all()
        elif type == "category":
            articles = Article.query.filter(Article.category == value).order_by(Article.id.desc()).all()
        elif type == "scope":
            articles = Article.query.filter(Article.scope == value).order_by(Article.id.desc()).all()
        result["status"] = "SUCCESS"
        result["data"] = []
        for article in articles:
            itemdata = {
                "id": article.id,
                "title": article.title,
                "date": article.date,
                "author": article.author,
                "image": article.image,
                "caption": article.caption,
                "article": article.article,
                "category": article.category,
                "scope": article.scope
            }
            result["data"].append(itemdata)
        return jsonify(result)
    except Exception as e:
        result["status"] = "ERROR: can't get articles of type '" + type + "' and value '" + value + "'"
        result["data"] = repr(e)
        return jsonify(result)

#route to get options for a browse search
@fetcher.route("/get_options/<string:type>/", methods=["GET"])
def get_options(type):
    result = {
        "status": None,
        "data": None
    }
    if type not in ["time", "author", "category", "scope"]:
        result["status"] = "ERROR: '" + type + "' is not a valid option type"
        result["data"] = None
        return result
    try:
        options = []
        if type == "time":
            options = ["Weekly", "Monthly", "Yearly", "All Time"]
        elif type == "author":
            for option in Article.query.distinct(Article.author):
                options.append(option.author)
        elif type == "category":
            for option in Article.query.distinct(Article.category):
                options.append(option.category)
        elif type == "scope":
            for option in Article.query.distinct(Article.scope):
                options.append(option.scope)
        result["status"] = "SUCCESS"
        result["data"] = options
        return jsonify(result)
    except Exception as e:
        result["status"] = "ERROR: can't get options of type '" + type + "'"
        result["data"] = repr(e)
        return jsonify(result)

#route to get articles sorted by title
@fetcher.route("/get_ordered_titles/", methods=["GET"])
def get_ordered_titles():
    result = {
        "status": None,
        "data": None
    }
    try:
        result["data"] = []
        for article in Article.query.order_by(Article.title).all():
            itemdata = {
                "id": article.id,
                "title": article.title,
                "date": article.date,
                "author": article.author,
                "image": article.image,
                "caption": article.caption,
                "article": article.article,
                "category": article.category,
                "scope": article.scope
            }
            result["data"].append(itemdata)
        result["status"] = "SUCCESS"
        return jsonify(result)
    except Exception as e:
        result["status"] = "ERROR: can't get articles sorted by title"
        result["data"] = repr(e)
        return jsonify(result)

#the "clutch" call
@fetcher.route("/load_app/", methods=["GET"])
def load_app():
    result = {
        "status": None,
        "data": None
    }
    try:
        result["data"] = {
            "articles": [],
            "titles": [],
            "options": {}
        }
        for article in Article.query.order_by(Article.id.desc()).all():
            itemdata = {
                "id": article.id,
                "title": article.title,
                "date": article.date,
                "author": article.author,
                "image": article.image,
                "caption": article.caption,
                "article": article.article,
                "category": article.category,
                "scope": article.scope
            }
            result["data"]["articles"].append(itemdata)
        result["data"]["titles"] = get_ordered_titles()["data"]
        for option in ["time", "authors", "categories", "scopes"]:
            result["data"]["options"][option] = get_options(option)["data"]
        result["status"] = "SUCCESS"
        return jsonify(result)
    except Exception as e:
        result["status"] = "ERROR: can't load app"
        result["data"] = repr(e)
        return jsonify(result)

app.register_blueprint(fetcher)

if __name__ == '__main__':
    app.debug = True
    app.run()
