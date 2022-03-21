import os
import re
import secrets
import smtplib
import random
from flask import render_template, url_for, flash, redirect, request, abort
import flask
from flaskapp import app, db, bcrypt, admin
from flaskapp.models import  signup, head, article
from flaskapp.form import SignUp, Login, UpdateInfo, ForgotPassword, ApprovePass,CreateArticle
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/')
def index():
    mains = head.query.all()



    return render_template("index.html", mains = mains)

@app.route('/userform')
def userform():
    form = Login()
    return render_template("signin.html",form = form)

@app.route('/signin', methods = ['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = Login()

    if form.validate_on_submit():
        user = signup.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))



        else:
            flash("Hesaba daxil olmaq mümkün olmadı! Istifadəçi adı və parolu tekrar yoxlayin.","danger")

    return redirect(url_for("userform"))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUp()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = signup(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Hesab uğurla yaradıldı. Hesaba giriş edə bilərsiniz!', 'success')
        return redirect(url_for('signin'))

    return render_template('newsignup.html', title='Register', form=form)

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():

    form = UpdateInfo()
    if request.method == 'POST':

        current_user.username = form.username.data
        current_user.email = form.email.data


        db.session.commit()
        flash('Sizin hesabiniz ugurla yenilendi', 'success')
        return redirect(url_for('account'))


    form.username.data = current_user.username
    form.email.data = current_user.email

    return render_template("updateaccount.html", form = form)

@app.route('/forgotpass', methods = ['GET','POST'])
def forgotpass():
    form = ForgotPassword()
    if form.validate_on_submit():
        username=form.username.data
        user = signup.query.filter_by(username=form.username.data).first()
        if user:
            user_email = user.email
            print(user_email)
            new_password = form.password.data
            code = random.randint(1111,9999)
            msg = str(code)
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login('umarovfeqan@gmail.com', 'cqiubfezunmdnhqy')
            smtpserver.sendmail('umarovfeqan@gmail.com',user_email, msg)
            smtpserver.quit()
            flash("Email ünvanınıza doğrulama kodu göndərilmişdir. Xahiş edirik həmin kodu daxil edəsiniz","warning")
            return redirect(url_for("approve",msg = msg, new_password = new_password, username = username))

    return render_template("forgot_pass.html", form=form)



@app.route('/approve',methods = ['GET','POST'])
@app.route('/approve/<msg>/<new_password>/<username>',methods = ['GET','POST'])
def approve(msg,new_password,username):
    form = ApprovePass()
    if form.validate_on_submit():
        user = signup.query.filter_by(username=username).first()
        if user and msg == form.approve.data:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash("Yeni parolunuz teyin edilmisdir. Hesabiniza daxil ola bilersiniz","success")
            return redirect(url_for('signin'))





    return render_template("approve_pass.html", form = form)


@app.route('/newarticle', methods=['GET','POST'])
@login_required
def newarticle():
    form = CreateArticle()
    if form.validate_on_submit():
        user_article = article(articletitle = form.title.data, content = form.content.data, author = current_user)
        db.session.add(user_article)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("article.html", form=form)
@app.route('/map')
def map():
    return redirect('http://localhost:1234')

@app.route('/articles',methods=["GET","POST"])
def articles():
    articles = article.query.all()
    return render_template("articles.html", articles = articles)

@app.route('/article_content/<int:article_id>')
def article_content(article_id):
    article_data = article.query.get_or_404(article_id)
    return render_template("article_content.html", title = article.articletitle, article_data = article_data )

@app.route('/deletearticle/<int:article_id>',methods = ['POST'])
@login_required
def deletearticle(article_id):
    article_delete = article.query.get_or_404(article_id)
    if article_delete.author != current_user:
        flash('Siz yanlız öz məqalənizi silə bilərsiniz', 'danger')
        return redirect(url_for('articles'))
    db.session.delete(article_delete)
    db.session.commit()
    flash("Məqalə uğurla silindi", 'successs')
    return redirect(url_for('articles'))
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/mapdetail")
def mapdetail():
    return render_template ("map_detail.html")

@app.route("/viewQgisMap")
def viewQgisMap():
    return render_template("mapqgis.html")

@app.route("/arcgisapi")
def arcgisapi():
    return render_template("arcgisapi.html")

@app.route("/openlayer")
def openlayer():
    return redirect ("http://localhost:1234")

