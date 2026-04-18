from flask import Flask, render_template, request, session, redirect, url_for
import os
from predict import predict_text
from generator import generate_image
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from model import custom_predict

app = Flask(__name__)

# 🔥 REQUIRED for session
app.secret_key = "secret123"

# 🔥 Upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔥 DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# =========================
# 🔥 USER MODEL
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()


# =========================
# 🔹 HOME PAGE
# =========================
@app.route("/")
def home():
    return render_template("home.html")


# =========================
# 🔹 OTHER PAGES
# =========================
@app.route("/business")
def business():
    return render_template("business.html")


@app.route("/demo")
def demo():
    return render_template("demo.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================
# 🔹 LOGIN PAGE (GET)
# =========================
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# =========================
# 🔹 SIGNUP LOGIC
# =========================
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "User already exists"

    # Hash password
    hashed_password = generate_password_hash(password)

    # Save user
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/login")


# =========================
# 🔹 LOGIN LOGIC
# =========================
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session["user"] = username
        return redirect("/convert")

    return "Invalid username or password"


# =========================
# 🔹 LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# =========================
# 🔹 OCR PAGE (CORE LOGIC)
# =========================
@app.route("/convert", methods=["GET", "POST"])
def convert():

    text = ""
    output_image = None
    uploaded_image = None

    if request.method == "POST":

        file = request.files["image"]

        if file:
            # ✅ SAVE FILE FIRST
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            uploaded_image = path

            # ✅ THEN APPLY OCR
            if "user" in session:
                # 🔵 Logged-in → Google Vision
                text = predict_text(path)
            else:
                # 🟢 Free user → Custom model
                from model import custom_predict
                text = custom_predict(path)

            # ✅ CUSTOMIZATION
            font_size = int(request.form.get("font_size", 28))
            color = request.form.get("color", "blue")
            spacing = int(request.form.get("spacing", 10))

            # ✅ GENERATE OUTPUT IMAGE
            output_image = generate_image(text, font_size, color, spacing)

    return render_template(
        "index.html",
        text=text,
        image=uploaded_image,
        output_image=output_image
    )




# =========================
# 🔥 RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)