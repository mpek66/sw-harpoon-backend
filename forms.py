from flask import Blueprint, jsonify, Flask, redirect, request, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField
from wtforms.validators import DataRequired

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date", format='%m/%d/%Y', validators=[DataRequired()])
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
    id = IntegerField("Id", validators=[DataRequired()])
    title = StringField("Title")
    date = DateField("Date", format='%m/%d/%Y')
    author = StringField("Author")
    image = StringField("Image")
    caption = StringField("Caption")
    location = StringField("Location")
    article = StringField("Article")
    category = StringField("Category")
    scope = StringField("Scope")
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class RemoveArticleForm(FlaskForm):
    id = IntegerField("Id", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
