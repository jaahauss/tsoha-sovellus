from app import app
from flask import redirect, render_template, request, session
import users, archiving, suggestions, books, comments

@app.route("/")
def index():
    user_id = users.user_id()
    result = books.index(user_id)
    return render_template("index.html", books=result[0], suggestions=result[1], is_admin=result[2])
    
@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/new_suggestion")
def new_suggestion():
    return render_template("new_suggestion.html")
    
@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    books.create()
    return redirect("/")

@app.route("/write/<int:id>")
def write(id):
    topic = comments.write(id)
    return render_template("new_message.html", id=id, topic=topic)

@app.route("/send", methods=["POST"])
def send():
    user_id = users.user_id()
    content = request.form["content"]
    book_id = request.form["id"]
    comments.send(user_id, content, book_id)
    return redirect("/")
    
@app.route("/result/<int:id>")
def result(id):
    user_id = users.user_id()
    result = comments.result(user_id, id)
    return render_template("result.html", topic=result[0], messages=result[1], user_name=result[2], is_admin=result[3])

@app.route("/archive/<int:id>")
def archive(id):
    archiving.archive(id)
    return redirect("/")

@app.route("/archive_result")
def archive_result():
    books = archiving.archive_result()
    return render_template("archive_result.html", books=books)

@app.route("/unarchive/<int:id>")
def unarchive(id):
    archiving.unarchive(id)
    return redirect("/archive_result")

@app.route("/suggest", methods=["POST"])
def suggest():
    content = request.form["content"]
    suggestions.suggest(content)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
