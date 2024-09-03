from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import time
import random
import string
import secrets
import os

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db.init_app(app)

app.secret_key = os.getenv("SECRET_KEY", secrets.token_bytes(32))


def get_flag():
    return os.getenv("FLAG", "testflag")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    registration_date = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "registration_date": self.registration_date,
            "printable_registration_date": time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(self.registration_date)
            ),
        }


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


def init_db():
    print("Initializing database")
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.before_first_request
def init_app():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        regdate = time.time()
        random.seed(regdate)
        password = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        admin = User(username="admin", password=password, registration_date=regdate)
        db.session.add(admin)
        db.session.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []
    if "username" in session:
        return redirect("/notes")
    if request.method == "POST":
        try:
            regdate = time.time()
            random.seed(regdate)
            password = "".join(
                random.choices(string.ascii_letters + string.digits, k=16)
            )
            username = request.form["username"]
            user = User(username=username, password=password, registration_date=regdate)
            db.session.add(user)
            db.session.commit()
            session["username"] = username
            session["user_id"] = user.id
            flash(
                "Registration successful, your password is: " + password
            )
            return redirect("/notes")
        except Exception as e:
            print(e)
            errors.append("Username already in use")
    return render_template("auth.html", action="register", errors=errors)


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if "username" not in session:
        return redirect("/register")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        note = Note(title=title, content=content, user_id=session["user_id"])
        db.session.add(note)
        db.session.commit()
    notes = Note.query.filter_by(user_id=session["user_id"]).all()
    if session["username"] == "admin":
        notes.append(
            Note(
                title="The flag",
                content=get_flag(),
            )
        )
    return render_template("notes.html", notes=notes)


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = []
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["username"] = username
            session["user_id"] = user.id
            return redirect("/notes")
        else:
            errors.append("Wrong username or password")
    return render_template("auth.html", action="login", errors=errors)


@app.route("/users")
def users():
    if "username" not in session:
        return redirect("/register")
    users = User.query.filter(
        (User.username == "admin") | (User.username == session["username"])
    ).all()
    return render_template("users.html", users=users)
