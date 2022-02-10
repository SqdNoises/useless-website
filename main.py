print("Loading...")
from flask import *
from os import environ, getenv
from random import randint
from getpass import getuser as u
from socket import gethostname as h
if u()+"@"+h() == "heroku@railway":
    address = "https://ADDRESS-HERE:5000"
else:
    address = "http://127.0.0.1:5000" # Device

def check():
    if getenv("STATE") == None:
        environ["STATE"] = "Something"

def checkprint(p):
    if getenv("STATE") == "Something":
        print(p)

def users():
    with open("users", "r") as usersfile:
        userslist = usersfile.read().splitlines()
    return userslist

def randletter(length=5, mode=None):
    word = ""
    for x in range (length):
        a = randint(1, 26)
        if a == 1:
            a = "a"
        elif a == 2:
            a = "b"
        elif a == 3:
            a = "c"
        elif a == 4:
            a = "d"
        elif a == 5:
            a = "e"
        elif a == 6:
            a = "f"
        elif a == 7:
            a = "g"
        elif a == 8:
            a = "h"
        elif a == 9:
            a = "i"
        elif a == 10:
            a = "j"
        elif a == 11:
            a = "k"
        elif a == 12:
            a = "l"
        elif a == 13:
            a = "m"
        elif a == 14:
            a = "n"
        elif a == 15:
            a = "o"
        elif a == 16:
            a = "p"
        elif a == 17:
            a = "q"
        elif a == 18:
            a = "r"
        elif a == 19:
            a = "s"
        elif a == 20:
            a = "t"
        elif a == 21:
            a = "u"
        elif a == 22:
            a = "v"
        elif a == 23:
            a = "w"
        elif a == 24:
            a = "x"
        elif a == 25:
            a = "y"
        else:
            a = "z"
        if mode == None:
            mode_ = randint(1, 2)
        elif mode:
            mode_ = 1
        elif mode == False:
            mode_ = 2
        else:
            print("Invalid mode '{}'".format(mode))
            return "Invalid mode '{}'".format(mode)
        if mode_ == 1:
            word = word + a.upper()
        else:
            word = word + a
    return word

def randletterint(length=5, mode=None):
    word = ""
    for x in range(length):
        a = randint(1, 2)
        if a == 1:
            a = randletter(1, mode)
        else:
            a = randint(0, 9)
        word = word + str(a)
    return word

SECURE_PASSWORD = randletterint(20)
checkprint("Your secret password now is {}".format(SECURE_PASSWORD))

checkprint("Preparing...")
app = Flask(__name__)

@app.route("/home", methods=["POST"])
def home():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    if username == "":
        return render_template("user_empty.html",  a=address)
    if username in users():
        if getenv(username+":PASS") == None:
            return render_template("homenp.html", user=username, a=address)
        elif getenv(username+":PASS") == password:
            return render_template("home.html", user=username, pw=password, a=address)
        else:
            return render_template("wrong_password.html", user=username, pw=password, a=address)
    else:
        return render_template("user_not_found.html", username=username, a=address)
checkprint("-> Route /home ready")

@app.route("/cp_func", methods=["POST"])
def cp_func():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    new_password=request.form["new_password"].strip()
    if username == "":
        return render_template("user_empty.html", a=address)
    if new_password == "":
        return render_template("newpass_empty.html",a=address)
    if username in users():
        if getenv(username+":PASS") == None:
            environ[username+":PASS"] = new_password
            success = True
        elif getenv(username+":PASS") == password:
            environ[username+":PASS"] = new_password
            success = True
        else:
            success = False
        if success:
            return render_template("pwc.html", user=username, npw=new_password)
        else:
            return render_template("wrong_password.html", user=username, pw=password)
    else:
        return render_template("user_not_found.html", username=username)

@app.route("/create_func", methods=["POST"])
def create_func():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    if username == "":
        return render_template("user_empty.html")
    if username in users():
        return render_template("user_exists.html")
    else:
        with open("users", "a") as usersfile:
            usersfile.write("\n{0}\n".format(username))
        if password == "":
            return render_template("ucnp.html", user=username)
        else:
            environ[username+":PASS"] = password
            return render_template("uc.html", user=username, pw=password)
checkprint("-> Route /create_func ready")

@app.route("/cp_user/<username>")
def cp_user(username):
    if username == "":
        return render_template("user_empty.htmlp")
    if username in users():
        return render_template("cp_user.html", user=username)
    else:
        return render_template("user_not_found.html", username=username)
checkprint("-> Route /cp_user/<username> ready")

@app.route("/login")
def login():
    return render_template("login.html")
checkprint("-> Route /login ready")

@app.route("/change_password")
def change_password():
    return render_template("change.html")
checkprint("-> Route /change_password ready")

@app.route("/create")
def create():
    return render_template("create.html")
checkprint("-> Route /create ready")

@app.route("/")
def root():
    return render_template("root.html")
checkprint("-> Route / ready")

@app.route("/secret_panel")
def secret_panel():
    print("@ Your secret password is {}".format(SECURE_PASSWORD))
    return render_template("secret_panel.html")
checkprint("-> Route /secret_panel ready")

@app.route("/secret", methods=["POST"])
def secret():
    password = request.form["panel_password"].strip()
    try:
        option = request.form["option"].strip()
        is_option = True
    except:
        is_option = False
    if password == SECURE_PASSWORD:
        if is_option:
            pass
        else:
            return render_template("secret.html")
    else:
        return "lol nice try tryna unlock this page\n(psst. you entered the wrong password)"
checkprint("-> Route /secret ready")

if __name__ == "__main__":
    checkprint("=> Starting site on localhost with port 5000...")
    check()
    app.run(debug=True)