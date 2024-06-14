from app import app
from flask import redirect, render_template, request, session
import users, archiving, suggestions, books, comments, reviews

@app.route("/")
def index():
    user_id = users.user_id()
    if user_id != 0:
        result = books.index(user_id)
        return render_template("index.html", books=result[0], suggestions=result[1], is_admin=result[2])
    else:
        return render_template("index.html")
    
@app.route("/new")
def new():
    return render_template("new.html")
    
@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    books.create(topic)
    return redirect("/")
        
@app.route("/review/<int:id>")
def review(id):
    topic = reviews.review(id)
    return render_template("new_review.html", id=id, topic=topic)

@app.route("/send_review", methods=["POST"])
def send_review():
    grade = request.form["grade"]
    book_id = request.form["id"]
    reviews.send(grade, book_id)
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
    return redirect("/result/"+str(book_id))
    
@app.route("/result/<int:id>")
def result(id):
    user_id = users.user_id()
    result = comments.result(user_id, id)
    return render_template("result.html", topic=result[0], messages=result[1], user_name=result[2], is_admin=result[3], book_id=id)

@app.route("/delete_message/<int:id>/<int:book_id>")
def delete_message(id, book_id):
    comments.delete(id)
    return redirect("/result/"+str(book_id))

@app.route("/alter_message/<int:id>/<int:book_id>")
def alter_message(id, book_id):
    topic = comments.alter(book_id)
    return render_template("alter_message.html", id=id, book_id=book_id, topic=topic)

@app.route("/send_altered", methods=["POST"])
def send_altered():
    content = request.form["content"]
    book_id = request.form["book_id"]
    message_id = request.form["id"]
    comments.send_altered(content, message_id)
    return redirect("/result/"+str(book_id))
    
@app.route("/archive/<int:id>")
def archive(id):
    archiving.archive(id)
    return redirect("/")

@app.route("/archive_index")
def archive_index():
    books = archiving.archive_index()
    return render_template("archive_index.html", books=books)

@app.route("/unarchive/<int:id>")
def unarchive(id):
    archiving.unarchive(id)
    return redirect("/archive_index")

@app.route("/new_suggestion")
def new_suggestion():
    return render_template("new_suggestion.html")
    
@app.route("/suggest", methods=["POST"])
def suggest():
    content = request.form["content"]
    suggestions.suggest(content)
    return redirect("/")

@app.route("/delete_suggestion/<int:id>")
def delete_suggestion(id):
    suggestions.delete(id)
    return redirect("/")

@app.route("/approve_suggestion/<int:id>")
def approve_suggestion(id):
    suggestions.approve(id)
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
            return render_template("error.html", message="Salasanat eroavat toisistaan")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
