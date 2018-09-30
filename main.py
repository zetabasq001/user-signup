from flask import Flask, request, redirect
import os 
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), \
autoescape=True)

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/signup")
def display_signup_form():
    template = jinja_env.get_template("signup-form.html")
    return template.render()

@app.route("/signup", methods=["POST"])
def validate_signup():
    template = jinja_env.get_template("signup-form.html")
    username = request.form["username"]
    password = request.form["password"]
    verify_password = request.form["verify"]
    email = request.form["email"]

    username_error, password_error, verify_password_error, email_error = "","","",""

    if username == "" or " " in username or len(username) < 3 or len(username) > 20:
        username_error = """Please enter a valid username:
                            no spaces, no less than three
                            characters and no greater than 
                            twenty"""

    if password == "" or " " in password or len(password) < 3 or len(password) > 20:
        password_error = """Please enter a valid password:
                            no spaces, no less than three
                            characters and no greater than 
                            twenty"""
    elif verify_password != password:
        verify_password_error = "Password mismatch"

    if email and (email.count("@") != 1 or email.count(".") != 1 or " " in email \
    or len(email) < 3 or len(email) > 20):
        email_error = "Please enter a valid email"

    if not username_error and not password_error and not verify_password_error \
    and not email_error:
        return redirect("/valid-signup?username={0}".format(username))
    else:
        return template.render(username=username, email=email, \
        username_error=username_error, password_error=password_error, \
        verify_password_error=verify_password_error, email_error=email_error)

@app.route("/valid-signup")
def valid_signup():
    template = jinja_env.get_template("valid-form.html")
    username = request.args.get("username")
    return template.render(username=username)


app.run()