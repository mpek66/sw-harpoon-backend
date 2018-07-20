from flask import Blueprint, jsonify, Flask, redirect, request, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
import server

manager = Blueprint("manager", __name__, template_folder='templates')

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    image = StringField("Image", validators=[DataRequired()])
    caption = StringField("Caption", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    article = StringField("Article", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    scope = StringField("Scope", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class EditArticleForm(FlaskForm):
    id = StringField("Id", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    image = StringField("Image", validators=[DataRequired()])
    caption = StringField("Caption", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    article = StringField("Article", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    scope = StringField("Scope", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class RemoveArticleForm(FlaskForm):
    id = StringField("Id", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

#functions for validating credentials
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
        status = server.add_article(form)
        if status == "SUCCESS":
            return redirect(url_for("manager.success"))
        else:
            return redirect(url_for("manager.errors", errors=status))
    return render_template("/add_article.html", form=form)

@manager.route("/edit_article/", methods=["GET", "POST"])
def edit_article():
    form = EditArticleForm()
    if form.validate_on_submit():
        if form.name.data != get_credential_name() or form.password.data != get_credential_password():
            return render_template("/edit_article.html", form=form)
        status = server.edit_article(form)
        if status == "SUCCESS":
            return redirect(url_for("manager.success"))
        else:
            return redirect(url_for("manager.errors", errors=status))
    return render_template("/edit_article.html", form=form)

@manager.route("/remove_article/", methods=["GET", "POST"])
def remove_article():
    form = RemoveArticleForm()
    if form.validate_on_submit():
        if form.name.data != get_credential_name() or form.password.data != get_credential_password():
            return render_template("/remove_article.html", form=form)
        status = server.remove_article(form)
        if status == "SUCCESS":
            return redirect(url_for("manager.success"))
        else:
            return redirect(url_for("manager.errors", errors=status))
    return render_template("/remove_article.html", form=form)

@manager.route("/success/", methods=["GET"])
def success():
    return render_template("/success.html")

@manager.route("/errors/", methods=["GET"])
def errors():
    problems = request.args.get("errors")
    return render_template("/errors.html", errors=problems)
