import query
import os
import shutil
from git import Repo

def clean_author(author):
    return "_".join(author.split()).lower()

def add_article(form):
    #utility for accessing all files
    realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
    #id of the new article, SUPER important
    id = None
    #stats of the new article
    data = {
        "id": id,
        "title": form.title.data,
        "date": form.date.data,
        "author": form.author.data,
        "image": form.image.data,
        "caption": form.caption.data,
        "article": form.article.data,
        "category": form.category.data,
        "scope": form.scope.data,
    }
    #keep track of any errors that occur
    errors = []

    #generate an id and make folder for article
    try:
        lines = []
        with open(realpath + "/all/ids.txt", "r") as fin:
            lines = fin.readlines()
        with open(realpath + "/all/ids.txt", "a+") as fin:
            if len(lines) == 0:
                id = "0"
                fin.write(id + "\n")
            else:
                id = str(int(lines[-1])+1)
                fin.write(id + "\n")
            newpath = realpath + "/articles/" + id
            if not os.path.exists(newpath):
                os.makedirs(newpath)
    except:
        errors.append("ERROR: generating id and making article folder")
    data["id"] = id

    #write all the data to the article folder
    try:
        for key in data:
            articlepath = realpath + "/articles/" + id
            with open(articlepath + "/" + key + ".txt", "w+") as fin:
                fin.write(data[key])
    except:
        errors.append("ERROR: writing data to article folder")

    #add to sorted titles
    try:
        new_title_sort = ""
        with open(realpath + "/all/title_ordered.txt", "r") as fin:
            ids = fin.readlines()
            ix = 0
            while ix < len(ids):
                lookid = ids[ix].strip()
                if lookid == "":
                    ix += 1
                    continue
                if query.get(lookid, "title") < data["title"]:
                    new_title_sort += lookid + "\n"
                    ix += 1
                else:
                    break
            new_title_sort += id + "\n"
            while ix < len(ids):
                lookid = ids[ix].strip()
                if lookid == "":
                    ix += 1
                    continue
                new_title_sort += lookid + "\n"
                ix += 1
        with open(realpath + "/all/title_ordered.txt", "w") as fin:
            fin.write(new_title_sort)
    except:
        errors.append("ERROR: adding id to sorted titles")

    #add to sorted authors
    try:
        new_author_sort = ""
        with open(realpath + "/all/author_ordered.txt", "r") as fin:
            ids = fin.readlines()
            ix = 0
            while ix < len(ids):
                lookid = ids[ix].strip()
                if lookid == "":
                    ix += 1
                    continue
                if query.get(lookid, "author") < data["author"]:
                    new_author_sort += lookid + "\n"
                    ix += 1
                else:
                    break
            new_author_sort += id + "\n"
            while ix < len(ids):
                lookid = ids[ix].strip()
                if lookid == "":
                    ix += 1
                    continue
                new_author_sort += lookid + "\n"
                ix += 1
        with open(realpath + "/all/author_ordered.txt", "w") as fin:
            fin.write(new_author_sort)
    except:
        errors.append("ERROR: adding id to sorted authors")

    #add to authors folder
    try:
        cleanauthor = clean_author(data["author"])
        authorpath = realpath + "/authors/" + cleanauthor
        if not os.path.exists(authorpath):
            os.makedirs(authorpath)
            with open(realpath + "/authors/authors.txt", "a") as fin:
                fin.write(cleanauthor)
        with open(authorpath + "/name.txt", "w+") as fin:
            fin.write(data["author"])
        with open(authorpath + "/articles.txt", "a+") as fin:
            fin.write(id + "\n")
    except:
        errors.append("ERROR: adding to authors folder")

    #add to categories folder
    try:
        categorypath = realpath + "/categories/" + data["category"]
        with open(categorypath + "/articles.txt", "a+") as fin:
            fin.write(id + "\n")
    except:
        errors.append("ERROR: adding to categories folder")

    #add to scopes folder
    try:
        scopepath = realpath + "/scopes/" + data["scope"]
        with open(scopepath + "/articles.txt", "a+") as fin:
            fin.write(id + "\n")
    except:
        errors.append("ERROR: adding to scopes folder")

    repo = Repo("..")
    repo.git.add(".")
    repo.git.commit("-m ADD " + data["title"])
    repo.git.push("origin")
    #repo.git.push("heroku", "master")
    """
    repo = Repo(".")
    to_add = [ item.a_path for item in repo.index.diff(None) ]
    to_add += repo.untracked_files
    index = repo.index
    index.add(to_add)
    new_commit = index.commit("ADD " + data["title"])
    origin = repo.remotes.origin
    origin.push()"""

    if len(errors) == 0:
        return "SUCCESS"
    else:
        return str(errors)

def edit_article(form):
    #utility for accessing all files
    realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
    #stats of the edited article
    data = {
        "id": form.id.data,
        "title": form.title.data,
        "date": form.date.data,
        "author": form.author.data,
        "image": form.image.data,
        "caption": form.caption.data,
        "article": form.article.data,
        "category": form.category.data,
        "scope": form.scope.data,
    }
    #meta status tracking
    idgood = False
    errors = []

    #look for existing id
    with open(realpath + "/all/ids.txt", "r") as fin:
        lines = fin.readlines()
        for line in lines:
            lookid = line.strip()
            if data["id"] == lookid:
                idgood = True
                break
    if not idgood:
        errors.append("ERROR: " + data["id"] + " not found in database")
        return str(errors)

    #write all the data to the article folder
    try:
        for key in data:
            articlepath = realpath + "/articles/" + data["id"]
            with open(articlepath + "/" + key + ".txt", "w+") as fin:
                fin.write(data[key])
    except:
        errors.append("ERROR: writing data to article folder")

    if len(errors) == 0:
        return "SUCCESS"
    else:
        return str(errors)

def remove_article(form):
    #utility for accessing all files
    realpath = os.path.dirname(os.path.realpath(__file__))+"/static"
    #stats of the edited article
    id = form.id.data
    data = {
        "title": query.get(id, "title"),
        "author": query.get(id, "author"),
        "category": query.get(id, "category"),
        "scope": query.get(id, "scope"),
    }
    #meta status tracking
    idgood = False
    errors = []

    #look for existing id
    with open(realpath + "/all/ids.txt", "r") as fin:
        lines = fin.readlines()
        for line in lines:
            lookid = line.strip()
            if id == lookid:
                idgood = True
                break
    if not idgood:
        errors.append("ERROR: " + id + " not found in database")
        return str(errors)

    #remove from author folder
    try:
        cleanauthor = clean_author(data["author"])
        authorpath = realpath + "/authors/" + cleanauthor
        newarticles = ""
        with open(authorpath + "/articles.txt", "r+") as fin:
            lines = fin.readlines()
            for line in lines:
                lookid = line.strip()
                if id != lookid:
                    newarticles += line
        with open(authorpath + "/articles.txt", "w+") as fin:
            fin.write(newarticles)
    except Exception as e:
        print(type(e))
        print(e.args)
        errors.append("ERROR: removing from authors folder")

    #remove from category folder
    try:
        categorypath = realpath + "/categories/" + data["category"]
        newarticles = ""
        with open(categorypath + "/articles.txt", "r+") as fin:
            lines = fin.readlines()
            for line in lines:
                lookid = line.strip()
                if id != lookid:
                    newarticles += line
        with open(categorypath + "/articles.txt", "w+") as fin:
            fin.write(newarticles)
    except Exception as e:
        print(type(e))
        print(e.args)
        errors.append("ERROR: removing from categories folder")

    #remove from scopes folder
    try:
        scopespath = realpath + "/scopes/" + data["scope"]
        newarticles = ""
        with open(scopespath + "/articles.txt", "r+") as fin:
            lines = fin.readlines()
            for line in lines:
                lookid = line.strip()
                if id != lookid:
                    newarticles += line
        with open(scopespath + "/articles.txt", "w+") as fin:
            fin.write(newarticles)
    except Exception as e:
        print(type(e))
        print(e.args)
        errors.append("ERROR: removing from scopes folder")

    #remove from id lists
    paths = [
        realpath + "/all/author_ordered.txt",
        realpath + "/all/ids.txt",
        realpath + "/all/title_ordered.txt"
    ]
    for path in paths:
        try:
            newarticles = ""
            with open(path, "r+") as fin:
                lines = fin.readlines()
                for line in lines:
                    lookid = line.strip()
                    if id != lookid:
                        newarticles += line
            with open(path, "w+") as fin:
                fin.write(newarticles)
        except:
            errors.append("ERROR: removing from all folder")

    #delete directory
    try:
        shutil.rmtree(realpath+"/articles/" + id)
    except:
        errors.append("ERROR: deleting article directory")

    repo = Repo(".")
    repo.git.add(".")
    repo.git.commit("-m REMOVE " + data["title"])
    repo.git.push("origin")

    if len(errors) == 0:
        return "SUCCESS"
    else:
        return str(errors)
