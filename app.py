from flask import *
import random

app = Flask(__name__)
app.secret_key = "SETKEYHERE"


@app.route('/')
def index():
    if "user" in session:
        return render_template("user.html", users=session["user"])
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)


@app.route('/signup', methods=["POST"])
def Signup():
    if request.method == "POST":
        with open("main.json", 'r') as f:
            data = json.load(f)
        username = request.form.get("usernamelog")
        password = request.form.get("passwordsign")
        username = username.lower()
        x = {"username": (username), "password": (password), "passwords": []}
        data["users"].append(x)
        with open("main.json", 'w') as f:
            json.dump(data, f, indent=2)
        return "Signup sucessful"

    else:
        return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def Login():
    if request.method == "POST":
        passfound = False
        username = request.form.get("username")
        password = request.form.get("password")
        username = username.lower()
        with open("main.json", 'r') as f:
            data = json.load(f)
        for x in data["users"]:
            if x["username"] == username:
                passfound == True
                if x["password"] == password:
                    session["user"] = username
                    return redirect(url_for("user", usr=username))
                else:
                    return "Password Incorrect"
        if passfound == False:
            return f"Incorect username :{username}:"
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", users=user)
    else:
        return render_template("index.html")


@app.route('/user/new', methods=['GET', 'POST'])
def NewPasswordForm():
    if request.method == 'POST':
        if "user" in session:
            user = session["user"]
        else:
            return render_template("index.html")
        text = request.form.get("text")
        specialCharsConfig = request.form.get("specialschars")
        text = text.lower()
        if text == "":
            return "Enter a valid Password"
        letters = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ]
        special = ["@", "#", "-"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        with open("main.json", 'r') as f:
            data = json.load(f)
        for x in data["users"]:
            if x["username"] == user:
                for y in x["passwords"]:
                    if y["name"] == text:
                        return f"Already a password for {text}"
        passwordlist = []
        specialcharacters = 0
        for x in range(15):
            if specialCharsConfig == "on":
                if random.randint(1,5) == 1 and specialcharacters <= 2:
                    specialcharacters += 1
                    character = random.choice(special)
                    passwordlist.append(character)
                elif random.randint(1,2) == 1:
                    character = random.choice(letters)
                    passwordlist.append(character)
                else:
                    character = random.choice(numbers)
                    passwordlist.append(character)
            else:
                if random.randint(1,2) == 1:
                    if random.randit(1,2) == 1:
                        character = random.choice(letters.upper())
                        passwordlist.append(character)
                    else:
                        character = random.choice(letters)
                        passwordlist.append(character)
                else:
                    character = random.choice(numbers)
                    passwordlist.append(character)
        password = ''.join(passwordlist)
                
        
        userfound = False
        newData = {"name": str(text.lower()), "password": str(password)}
        for x in data["users"]:
            if x["username"] == user:
                userfound = True
                x["passwords"].append(newData)
        if userfound == True:
            with open("main.json", 'w') as f:
                json.dump(data, f, indent=1)
        else:
            return f"error {user} was not found it our data base"
        return f"Your password for {text} is {password}"
    else:
        return redirect(url_for("user", users=user))


@app.route('/user/Read', methods=['GET', 'POST'])
def Read():
    if request.method == 'POST':
        textfound = False
        if "user" in session:
            user = session["user"]
        else:
            return render_template("index.html")
        text = request.form.get("ReadText")
        text = text.lower()
        with open("main.json", 'r') as f:
            data = json.load(f)

        text.lower()
        for x in data["users"]:
            if x["username"] == user:
                for y in x["passwords"]:
                    if y["name"] == text:
                        textfound = True
                        return f"The password for {text} is " + y["password"]
        if textfound == False:
            return "name for password not found"
        if text == "":
            return redirect(url_for("user", users=user))
    else:
        return redirect(url_for("user", users=user))


@app.route('/user/Delete', methods=['Get', 'Post'])
def Delete():
    if request.method == "POST":
        if "user" in session:
            user = session["user"]
        else:
            return render_template("index.html")
        password = request.form.get("DeleteText")
        password = password.lower()
        with open("main.json", 'r') as f:
            data = json.load(f)
        namefound = False
        passwords = []
        for x in data["users"]:
            if x['username'] == user:
                for pwdict in x['passwords']:
                    if pwdict['name'] != password:
                        passwords.append(pwdict)
                    else:
                        namefound = True
                x['passwords'] = passwords

        if namefound == False:
            return f"There is no password to delete for {password}"
        with open("main.json", 'w') as f:
            json.dump(data, f, indent=1)
        return redirect(url_for("user", users=user))

    else:
        return render_template("user.html")
