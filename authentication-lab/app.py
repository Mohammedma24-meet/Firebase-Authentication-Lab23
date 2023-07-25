from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyAKHPGxzNjnNilijGrg6Ka77cKMlc0CJ0Y",
  "authDomain": "project-1-a9381.firebaseapp.com",
  "projectId": "project-1-a9381",
  "storageBucket": "project-1-a9381.appspot.com",
  "messagingSenderId": "320826528353",
  "appId": "1:320826528353:web:08daa4f79e2f5789055020",
  "databaseURL": "https://project-1-a9381-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {
            "email": email,
            "password": password,
            "full_name": full_name,
            "username": username,
            "bio": bio,
            }
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        Title = request.form['Title']
        Text = request.form['Text']
        UID = login_session['user']['localId']

        try:
            tweet = {"Title": Title,
                      "Text": Text, 
                      "UID" : UID}
            db.child("Tweets").push(tweet)
            return redirect(url_for('tweets'))
        except:
            print("Couldn't add tweet")
   


    return render_template("add_tweet.html")

    


@app.route('/tweets.html')
def tweets():
    tweet1=db.child("Tweets").get().val()
    return render_template("tweets.html", tweet1=tweet1)




if __name__ == '__main__':
    app.run(debug=True)


