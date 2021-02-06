from flask import Flask, render_template, request, \
    redirect, url_for, flash
import pandas as pd
import csv
from collections import defaultdict
import random
from models import User
from config import Config
from extension import db

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_url, login_required, current_user, login_user

## Setting up app essentials
app = Flask(__name__, static_folder='./static')
app.config.from_object(Config)
# db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
db.init_app(app)

@app.route('/', methods=["GET", "POST"])
def initial():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = request.form
    if request.method == "POST":
        user = User.query.filter_by(username=form['username']).first()
        if user is None or not user.check_password(form['password']):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return render_template('home.html')
    return render_template('home.html')


@app.route('/index', methods=["GET", "POST"])
def index():
    d = None
    if request.method == "POST":  # if the request is post (i.e. new video annotated?)
        # print(request.form)
        j = request.form
        k = request.form.getlist('culture')

        # if statement is for setting up the csv file
        # Write each parameter to a txt file so it can be called later and stored in csv file.

        if len(k) > 0:

            cult = j['culture']
            IDV = j['IDV']
            nat = j['country']
            lang = j['language']
            with open("store_culture.txt", "a+") as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(nat)
                file_object.write("\n")
                file_object.write(lang)
                file_object.write("\n")
                file_object.write(cult)
                file_object.write("\n")
                file_object.write(IDV)

            vid = 'video' + str(random.randint(1, 6)) + '.mp4'
            with open("store_video.txt", "a+") as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(vid)

            return render_template('index.html', video=vid)

        # this component takes user input after initial setup
        d = request.form.to_dict()
        r = open("store_culture.txt", "r")  # read last 4 items stored from the txt file from initial setup
        # print(r)
        word = r.read().splitlines()
        # print(word)
        p = word[-1]
        s = word[-2]
        q = word[-3]
        t = word[-4]
        d['culture'] = p
        d['language'] = s
        d['country'] = q
        d['IDV'] = t

        r = open("store_video.txt", "r")
        n = r.readline()
        word = n.split()
        v = word[-1]
        d['video'] = v

        grp = defaultdict(list)
        for k, v in d.items():
            if k[0:3] == "soc":
                grp['socialsignals'].append(v)
            else:
                grp[k] = v
        print(grp)

        fields = grp.values()
        # print(fields)

        # writes everything that is in the dictionary to the csv file
        with open('out.csv', 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

        # store new video so it can be used for the next setup of user input
        vid = 'video' + str(random.randint(1, 6)) + '.mp4'
        with open("store_video.txt", "a+") as file_object:
            file_object.seek(0)
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            file_object.write(vid)
        return render_template('index.html', video=vid)

    vid = 'video' + str(random.randint(1, 6)) + '.mp4'
    return render_template('index.html', video=vid)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
