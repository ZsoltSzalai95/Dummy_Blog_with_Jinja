from flask import Flask, render_template, request
import requests
import smtplib

MY_MAIL = "YOURMAIL"
MY_PASS = "YOURPASS"

API = "https://api.npoint.io/c790b4d5cab58020d391"
response = requests.get(API)
response_json = response.json()

app = Flask(__name__)



@app.route("/")
def get_all_posts():
    return render_template("index.html", all_posts=response_json)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name_data = request.form['name']
        phone_data = request.form['phone_number']
        email_data = request.form['email']
        message_data = request.form['message']
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_MAIL, password=MY_PASS)
            connection.sendmail(
                from_addr=MY_MAIL,
                to_addrs=MY_MAIL,
                msg="Subject:Hello\n\n"
                    f"Name: {name_data}\n"
                    f"Phone: {phone_data}\n"
                    f"Email: {email_data}\n"
                    f"Message: {message_data}")
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)



@app.route("/post/<int:num>")
def post(num):
    requested_post=None
    for blog_post in response_json:
        if blog_post["id"] == num:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)



if __name__ == "__main__":
    app.run(debug=True)