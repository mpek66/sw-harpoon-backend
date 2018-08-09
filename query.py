from flask import Blueprint, jsonify, Flask, redirect, request, url_for, render_template
import os
import server

fetcher = Blueprint("fetcher", __name__, template_folder='templates')

def get(id, key):
    try:
        realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
        idpath = realpath + "/articles/" + id
        with open(idpath + "/" + key + ".txt", "r+", encoding="utf8", errors='ignore') as fin:
            return str(fin.read())
    except Exception as e:
        print("ERROR: querying article with id " + id + " for " + key, e, )
        return "ERROR: querying article with id " + id + " for " + key + ", " + str(e)

def get_article_titles():
    try:
        realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
        ids = []
        with open(realpath + "/all/ids.txt", "r") as fin:
            for line in fin:
                ids.append(line.strip())
        result = []
        for id in ids:
            title = get(id, "title")
            result.append(id + " --- " + title)
        return result
    except:
        print("ERROR: querying the view of all articles")
        return "ERROR: querying the view of all articles"

# returns a json for a single article
def get_article(id):
    result = {
        "id": get(id, "id"),
        "title": get(id, "title"),
        "date": get(id, "date"),
        "author": get(id, "author"),
        "image": get(id, "image"),
        "caption": get(id, "caption"),
        "article": get(id, "article"),
        "category": get(id, "category"),
        "scope": get(id, "scope")
    }
    return result

#returns a json with metadata about the request status and a array of articles
def get_articles_by(type, value):
    #utility for accessing files
    realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
    status = "SUCCESS"
    articles = []

    try:
        if type == "time":
            with open(realpath + "/all/ids.txt", "r+") as fin:
                for line in fin:
                    articles.append(get_article(line.strip()))
        else:
            if type == "authors":
                value = server.clean_author(value)
            with open(realpath + "/" + type + "/" + value + "/articles.txt", "r+") as fin:
                for line in fin:
                    articles.append(get_article(line.strip()))
    except Exception as e:
        status = "ERROR: can't get articles by " + type + " with value " + value

    return (status, articles[::-1])

def get_options_data(type):
    realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
    status = "SUCCESS"
    options = []

    try:
        if type.lower() == "time":
            options = ["Weekly", "Monthly", "Yearly", "All Time"]
        else:
            type = type.lower()
            with open(realpath + "/" + type + "/" + type + ".txt", "r+") as fin:
                for line in fin:
                    raw = line.strip()
                    words = raw.split("_")
                    result = ""
                    for word in words[:-1]:
                        result += word[0].upper() + word[1:] + " "
                    result += words[-1][0].upper() + words[-1][1:]
                    options.append(result)
    except Exception as e:
        status = "ERROR: can't get options by " + type
    return status, options

def get_ordered_titles_data():
    realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
    result = []
    status = "SUCCESS"
    try:
        with open(realpath + "/all/title_ordered.txt", "r+") as fin:
            for line in fin:
                id = line.strip()
                pair = {
                    "id": id,
                    "title": get(id, "title")
                }
                result.append(pair)
    except Exception as e:
        status = "ERROR: can't fetch articles by title"
    return (status, result)

@fetcher.route("/view_articles/", methods=["GET", "POST"])
def view_articles():
    articles = get_article_titles()
    return render_template("/view_articles.html", articles=articles)

# routes to get shit
@fetcher.route("/get_article/<string:id>/", methods=["GET"])
def get_article_data(id):
    return jsonify(get_article(id))

# route to get articles
@fetcher.route("/get_articles/<string:type>/<string:value>/", methods=["GET"])
def get_articles(type, value):
    if type not in ["time", "authors", "categories", "scopes"]:
        return jsonify(status="ERROR: can't get articles of type " + type)
    (status, articles) = get_articles_by(type, value)
    return jsonify(status=status, articles=articles)

#route to get options for a browse search
@fetcher.route("/get_options/<string:type>/", methods=["GET"])
def get_options(type):
    if type not in ["time", "authors", "categories", "scopes"]:
        return jsonify(status="ERROR: can't get options of type " + type)
    (status, options) = get_options_data(type)
    return jsonify(status=status, options=options)

#route to get articles sorted by title
@fetcher.route("/get_ordered_titles/", methods=["GET"])
def get_ordered_titles():
    (status, result) = get_ordered_titles_data()
    return jsonify(status=status, result=result)

#the "clutch" call
@fetcher.route("/load_app/", methods=["GET"])
def load_app():
    data = {}
    status = "SUCCESS"

    try:
        data["articles"] = get_articles_by("time", "null")[1]
    except Exception as e:
        status = "ERROR: can't fetch time ordered articles"

    try:
        data["titles"] = get_ordered_titles_data()[1]
    except Exception as e:
        status = "ERROR: can't fetch ordered titles"

    try:
        for option in ["time", "authors", "categories", "scopes"]:
            data[option] = get_options_data(option)[1]
    except Exception as e:
        status = "ERROR: can't fetch browsing options"

    return jsonify(status=status, data=data)
