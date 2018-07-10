from flask import jsonify
import os
import server

def get(id, key):
    try:
        realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
        idpath = realpath + "/articles/" + id
        with open(idpath + "/" + key + ".txt", "r") as fin:
            return fin.read()
    except:
        print("ERROR: querying article with id " + id + " for " + key)
        return "ERROR: querying article with id " + id + " for " + key

def view_articles():
    try:
        realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
        ids = []
        with open(realpath + "/all/ids.txt", "r") as fin:
            for line in fin:
                ids.append(line.strip())
        print(ids)
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
    articles = []
    status = "SUCCESS"

    try:
        if type == "time":
            with open(realpath + "/all/ids.txt", "r+") as fin:
                for line in fin:
                    articles.append(get_article(line.strip()))
        else:
            with open(realpath + "/" + type + "/" + value + "/articles.txt", "r+") as fin:
                for line in fin:
                    articles.append(get_article(line.strip()))
    except Exception as e:
        status = "ERROR: can't get articles by " + type + " with value " + value

    return jsonify(status=status, articles=articles)
