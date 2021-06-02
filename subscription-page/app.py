from flask import Flask, render_template, url_for, request
import requests

app = Flask(__name__)
BASE_URL = 'https://v7l4qsdr3b.execute-api.us-east-1.amazonaws.com/Prod/emails'


def subscribe_user(email):
    resp = requests.post(f'{BASE_URL}', data={'email':f'{email}','id':'4'})
    print(resp.status_code)
    return resp

@app.route("/", methods=["GET", "POST"])
def index():
    # if user submits the form
    if request.method == "POST":
        email = request.form.get('email')
        subscribe_user(email=email)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)