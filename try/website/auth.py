from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from flask import session, redirect, url_for, render_template, request
from .forms import LoginForm
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    ''' This function checks wherever the request type was post(after submit - data being sent)
    or Get request, which just returns the login html page.
    if login was successful, the user will be redirected to the home page.'''
    if request.method == 'POST':


        email = request.form.get('email')
        password = request.form.get('password')


        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.chat'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    print (current_user)

    return render_template("login2.html", user=current_user )


@auth.route('/logout')
@login_required
def logout():
    ''' This function disconnects the user from the session using Flask-Login library, and redirects to login page.'''
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    ''' This function checks wherever the request type was post(after submit - data being sent)
    or Get request, which just returns the sign-up html page.
    the function checks if email is unused, if password is valid, and it adds the user to the database.
    if sign-up was successful, it redirects the user to home page, and flash a successful message.'''
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        nick_name = request.form.get('nick_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        gender = request.form.get('gender')
        country = request.form.get('country')
        age = request.form.get('age')
        league_checked = request.form.get('league') != None
        cs_checked = request.form.get('cs') != None
        fortnite_checked = request.form.get('fortnite') != None
        r6_checked = request.form.get('r6') != None
        minecraft_checked = request.form.get('minecraft') != None
        cod_checked = request.form.get('cod') != None
        print(gender)
        print(league_checked, cs_checked, fortnite_checked, r6_checked, minecraft_checked, cod_checked)



        user = User.query.filter_by(email=email).first()
        user2 = User.query.filter_by(nick_name=nick_name).first()
        if user:
            flash('Email already exits.', category='error')
        elif user2:
            flash('NickName is taken.', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(full_name) < 2:
            flash('Name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        elif int(age) < 12:
            flash('You must be over 12 to use.', category='error')
        else:
            new_user = User(
                            email=email, full_name=full_name, age=age,
                            nick_name=nick_name, gender=gender, country=country,
                            password=generate_password_hash(password1, method='sha256'), cod_player=cod_checked,
                league_player=league_checked, minecraft_player=minecraft_checked, r6_player=r6_checked,
                fortnite_player=fortnite_checked,cs_player=cs_checked, image='https://bootdey.com/img/Content/avatar/avatar7.png')

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!.', category='success')
            return redirect(url_for('views.home'))

    return render_template("signUp.html", user=current_user)
