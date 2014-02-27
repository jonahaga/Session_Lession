from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        return "User %s is logged in!" %session['username']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    username = model.authenticate(username, password)
    print username
    if username == False:
        flash("User does not exist. Please register below.")
        return redirect(url_for("register"))
    elif username != None:
        flash("User authenticated!")
        session['username'] = username
        return redirect(url_for("view_user", username=request.form.get("username")))
    elif username == None:
        flash("Password incorrect, there may be a ferret stampede in progress!")
        return redirect(url_for("index"))


@app.route("/register")
def register():
    if session.get("username"):
        username = model.get_username_by_id(session.get("username"))
        return redirect(url_for('view_user', username=username))
    return render_template("register.html")

@app.route("/")
def session_clear():
    session.clear()
    return render_template("index.html")

@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    user_id = model.get_userid_by_name(username)
    wall_posts = model.get_wall_posts_by_user(user_id)
    return render_template("wall.html", wall_posts = wall_posts, username = username, session = session)

@app.route("/wall/<username>", methods=["POST"])
def post_to_wall(username):
    model.connect_to_db()
    user_id = model.get_userid_by_name(username)
    post_input = request.form.get("content")
    author_id = session['username']
    model.create_wall_post(user_id, author_id, post_input)
    return redirect(url_for("view_user", username=username))

@app.route("/create_account", methods=["POST"])
def create_account():
    # Receive form from Register template
    model.connect_to_db()
    username = request.form.get("username")
    
    user_id = model.get_userid_by_name(username)
    if user_id == None:
        username = request.form.get("username")
        password = request.form.get("password")
        flash("Account successfully created. Please sign in below.")
        model.create_account(username, password)
        return redirect(url_for("index"))
    else:
        flash("User already exists.")
        return redirect(url_for("register"))

if __name__ == "__main__":
    app.run(debug = True)