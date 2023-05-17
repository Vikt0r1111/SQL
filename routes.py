from app import app, db
from models import User
from flask import render_template, flash, redirect, url_for
from flask import session
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
@app.route("/index/")
def index():
    if session.get("is_auth"):
        return render_template("index.html")
    return redirect(url_for(login.__name__))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("is_auth"):
        return redirect(url_for(index.__name__))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()

        if user is not None and \
          check_password_hash(user.password_hash, form.password.data):
            flash(f"Login {form.login.data}")
            session["is_auth"] = True
            return redirect(url_for("index"))
        flash(f"Такого користувача не існує {form.login.data}")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("is_auth"):
        return redirect(url_for(index.__name__))
    form = RegisterForm()
    if form.validate_on_submit():
        encrypted = generate_password_hash(form.password.data)
        user = User(login=form.login.data, password_hash=encrypted)
        db.session.add(user)
        try:
            db.session.commit()
            flash(f"Registered {form.login.data}")
            return redirect(url_for("login"))
        except:
            db.session.rollback()
            flash(f"Такий користувач вже зареєстрований: {form.login.data}!")

    return render_template("register.html", form=form)

def postform():
    if session.get(""):
        return redirect(url_for(index.__name__))
    form = RegisterForm()
    if form.validate_on_submit():
        encrypted = generate_password_hash(form.password.data)
        user = User(login=form.login.data, password_hash=encrypted)
        db.session.add(user)
        try:
            db.session.commit()
            flash(f"Registered {form.login.data}")
            return redirect(url_for("body"))
        except:
            db.session.rollback()
            flash(f"Такий пост вже є: {form.login.data}!")

    return render_template("register.html", form=form)
@app.errorhandler(404)
def page_not_found(error):
    flash('This page does not exist 404')
    return redirect(url_for(index.__name__))

import posts