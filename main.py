import os
import smtplib
from flask import Flask, render_template, redirect, flash, url_for
from myforms import MyForm
import datetime as dt
import time
from flask_wtf import CSRFProtect

today = str(dt.datetime.now())
year = today.split("-")[0]
app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
csrf = CSRFProtect(app)

ugo = 'Welcome.I am Ugonna Ogoke\nA backend developer and a Data Analyst'


@app.route("/")
def welcome_page():
    return render_template("trial.html", year=year, ugo=ugo, time=time)


my_email = "anthonyugonnaa@gmail.com"
password = os.environ.get('password')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = MyForm()
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="anthonyugonnaa@gmail.com",
                                msg=f"Subject:NEW CONTACT \n\n\n {form.name.data}\n"
                                    f"{form.email.data}\nsays:{form.message.data}")
        flash("Message sent, will respond soon!")
        return redirect(url_for('contact'))
    return render_template("contact.html", form=form)


@app.route("/projects")
def projects():
    return render_template("project.html")


if __name__ == "__main__":
    app.run(debug=True)
