from flask import Flask, render_template, session, redirect, url_for, g, request
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, SellForm
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect( url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/")
@app.route("/home")
def home():
    db = get_db()
    items = db.execute("""SELECT * FROM items;""").fetchall()
    return render_template("home.html", items=items)


@app.route("/item/<int:item_id>")
def item(item_id):
    db = get_db()
    item = db.execute("""
                SELECT * FROM items
                WHERE item_id = ?;""", (item_id,)).fetchone()
    return render_template("item.html", item=item)

@app.route("/likes")
def likes():
    if "likes" not in session:
        session["likes"] = {}
    names = {}
    images = {}
    db = get_db()
    for item_id in session["likes"]:
        item = db.execute("""SELECT * FROM items
                             WHERE item_id = ?;""", (item_id,)).fetchone()
        name = item["name"]
        names[item_id] = name
        image = item["image"]
        images[item_id] = image
    return render_template("likes.html", likes=session["likes"], names=names, images=images)
    
@app.route("/add_to_likes/<int:item_id>")
def add_to_likes(item_id):
    if "likes" not in session:
        session["likes"] = {}
    if item_id not in session["likes"]:
        session["likes"][item_id] = 1
    else:
        session["likes"][item_id] = session["likes"][item_id] + 1
    session.modified = True
    return redirect( url_for("home") )

@app.route("/remove_from_likes/<int:item_id>")
def remove_from_likes(item_id):
    if "likes" not in session:
        session["likes"] = {}
    if session["likes"][item_id] >= 1:
        del session["likes"][item_id]
    session.modified = True
    return redirect( url_for("likes") )


@app.route("/cart")
def cart():
    if "cart" not in session:
        session["cart"] = {}
    names = {}
    images = {}
    db = get_db()
    for item_id in session["cart"]:
        item = db.execute("""SELECT * FROM items
                             WHERE item_id = ?;""", (item_id,)).fetchone()
        name = item["name"]
        names[item_id] = name
        image = item["image"]
        images[item_id] = image
    return render_template("cart.html", cart=session["cart"], names=names, images=images)
    
@app.route("/add_to_cart/<int:item_id>")
def add_to_cart(item_id):
    if "cart" not in session:
        session["cart"] = {}
    if item_id not in session["cart"]:
        session["cart"][item_id] = 1
    else:
        session["cart"][item_id] = session["cart"][item_id] + 1
    session.modified = True
    return redirect( url_for("home") )

@app.route("/purchase/<int:item_id>")
def purchase(item_id):
    if "cart" not in session:
        session["cart"] = {}
    if session["cart"][item_id] > 1:
        session["cart"][item_id] = session["cart"][item_id] - 1
    elif session["cart"][item_id] == 1:
        del session["cart"][item_id]
    session.modified = True
    return redirect( url_for("cart") )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        conflict_user = db.execute(
            """SELECT * FROM users
                WHERE user_id =?;""", (user_id,)).fetchone()
        if conflict_user is not None:
            form.user_id.errors.append("User name already taken")
        else:
            db.execute("""
                       INSERT INTO users (user_id, password)
                       VALUES (?, ?);""",
                       (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user = db.execute(
            """SELECT * FROM users
            WHERE user_id = ?;""", (user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("No such user name!")
        elif not check_password_hash(user["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("home")
            return redirect(next_page)
    return render_template("login.html", form=form)   
    
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect( url_for("home"))


@app.route("/sell", methods=["GET", "POST"])
def sell():
    form = SellForm()
    if form.validate_on_submit():
        name = form.name.data
        type = form.type.data
        price = form.price.data
        description = form.description.data
        #image = form.image.data
        db = get_db()
        db.execute(""" INSERT INTO selling (name, type, price, description)
                       VALUES (?, ?, ?, ?);""",
                       ((name, type, price, description)))
        db.commit()
        return redirect( url_for("myshop") )
        
    return render_template("sell.html", form=form)


@app.route("/myshop", methods=["GET", "POST"])
def myshop():
    db = get_db()
    selling = db.execute("""SELECT * FROM selling;""").fetchall()
    return render_template("myshop.html", selling=selling)

@app.route("/purchased/<int:item_id>")
def purchased(item_id):
    if "selling" not in session:
        session["selling"] = {}
    else:
        db = get_db()
        db.execute("""DELETE FROM selling
                   WHERE item_id = ? """,
                   (item_id,))
        db.commit()
    session.modified = True
    return redirect( url_for("myshop") )

        