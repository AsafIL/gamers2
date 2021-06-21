from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .dms import dm
from . import db
from .models import Note
import json
from .models import User

from .matching import matching
from sqlalchemy.sql.expression import func, select
from sqlalchemy.sql.expression import func
from flask import session, redirect, url_for, render_template, request
from .forms import LoginForm

from flask import session, redirect, url_for, render_template, request
from . import views
from . import main
from .forms import LoginForm


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    print(dm(1, 2))
    print(dm(2, 1))
    print('running home')
    if request.method == 'POST':
        note = request.form.get('note')
        print(len(note))
        if len(note) < 1 or note == '    ':
            flash('Invalid note!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!', category='success')
    # Listt = sorted(User.query(), key='db.')

    return render_template("home1.html", user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    '''This function returns the user profile.'''

    return render_template('profile.html', user=current_user)


@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        discord = request.form.get('discord')
        github = request.form.get('github')
        image = request.form.get('image')

        user = User.query.filter_by(nick_name=current_user.nick_name).first()
        print(full_name, discord, github, image)
        if full_name:
            user.full_name = full_name
        if discord:
            user.discord = discord
        if github:
            user.github = github
        if image:
            user.image = image
        db.session.commit()
        flash('Edit successfully changed')
        return render_template('profile.html', user=current_user)
    return render_template('edit_profile.html', user=current_user)


@views.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    room = session.get('room', '')
    if room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', room=room)


@views.route('/i', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


# @views.route('/search1', methods=['GET', 'POST'])
# @login_required
# def search1():
#     username = current_user.nick_name
#
#     if request.method == "POST":
#
#         # check if the POST method was from adding/accepting friend request and get the username and action(add/accept)
#         try:
#             get_search = ""
#             friend_request = request.form["friend"]
#             print(friend_request)
#             friend_request = friend_request.split(',')
#
#             # when sending friend request:
#             # add his username to my pending requests and my username to his friend requests
#             if friend_request[1] == "Add":
#                 my_user = User.query.filter_by(username=username).first()
#                 if my_user.pending is None:
#                     my_user.pending = friend_request[0] + ','
#                 else:
#                     my_user.pending += friend_request[0] + ','
#                 db.session.commit()
#
#                 friend_user = User.query.filter_by(username=friend_request[0]).first()
#                 if friend_user.requests is None:
#                     friend_user.requests = username + ','
#                 else:
#                     friend_user.requests += username + ','
#                 db.session.commit()
#
#             # when accepting friend request:
#             # remove his name from my pending requests, my username from his friend requests and add each other as friends
#             if friend_request[1] == "Accept":
#                 my_user = User.query.filter_by(username=username).first()
#                 my_user.requests = my_user.requests.replace(friend_request[0] + ',', '')
#                 if my_user.friends is None:
#                     my_user.friends = friend_request[0] + ','
#                 else:
#                     my_user.friends += friend_request[0] + ','
#                 db.session.commit()
#
#                 friend_user = User.query.filter_by(username=friend_request[0]).first()
#                 friend_user.pending = friend_user.pending.replace(username + ',', '')
#                 friend_user.friends += username + ','
#                 db.session.commit()
#
#         # get the username that was search
#         except:
#             get_search = request.form["searchKey"]
#
#         all_users = User.query.all()
#         found_users_list = []
#
#         if User.query.filter_by(username=username).first().friends is None:
#             my_friends = ""
#         else:
#             my_friends = User.query.filter_by(username=username).first().friends.split(',')
#         if User.query.filter_by(username=username).first().requests is None:
#             firnd_requests = ""
#         else:
#             firnd_requests = User.query.filter_by(username=username).first().requests.split(',')
#         if User.query.filter_by(username=username).first().pending is None:
#             pending_requests = ""
#         else:
#             pending_requests = User.query.filter_by(username=username).first().pending.split(',')
#
#         # get all the users that match the search key from the database
#         # and create a list with their username, picture, user creation date and situation(friend/pending/not friend)
#         for user in all_users:
#             if get_search in user.username:
#                 if user.username == username:
#                     pass
#
#                 else:
#                     my_user = User.query.filter_by(username=username).first()
#                     friend_user = User.query.filter_by(username=user.username).first()
#
#                     # Check mutual friends
#                     if my_user.friends is not None:
#                         my_friends = my_user.friends.split(',')
#                     else:
#                         my_friends = ""
#                     if friend_user.friends is not None:
#                         friend_friends = friend_user.friends.split(',')
#                     else:
#                         friend_friends = ""
#                     mutual_friends = ""
#
#                     for f in my_friends:
#                         if f in friend_friends and f != "":
#                             if mutual_friends != "":
#                                 mutual_friends += ', ' + f
#                             else:
#                                 mutual_friends += f
#                     if mutual_friends == "":
#                         mutual_friends = "No mutual friends"
#
#                     if user.username in my_friends:
#                         found_users_list.append(
#                             [user, mutual_friends, "Friend"])
#                     elif user.username in firnd_requests:
#                         found_users_list.append(
#                             [user, mutual_friends, "Accept"])
#                     elif user.username in pending_requests:
#                         found_users_list.append(
#                             [user, mutual_friends, "Pending"])
#                     else:
#                         found_users_list.append(
#                             [user, mutual_friends, "Add"])
#
#                         print(found_users_list)
#
#                         return render_template('search.html', found_users_list=found_users_list)
#
#                 else:
#                 return redirect(url_for("friends"))
#
#     else:
#         return redirect(url_for("login"))


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    '''This function gets a name from the post request the user sent, and redirects to the profile
    matching this name.'''
    if request.method == 'POST':
        # name = request.form.get('searched_name')
        # found_users = User.query.filter(User.nick_name.like(name))
        # found_users = found_users.order_by(User.full_name).all()
        # for user in found_users:
        #     print(matching(current_user=current_user, matched_user=user))
        #     return render_template('profile.html', user=user)
        #     print(user.full_name)
        type = request.form.get('option')
        print(type)
        # if type.checked:
        if type == 'byname':
            name = request.form.get('name')
            founded_users = User.query.filter(User.nick_name.like(name)).all()
            # founded_users = founded_users.order_by(User.full_name).all()
            print(founded_users)
            return render_template('search.html', user=current_user, founded_users=founded_users)
        else:
            game = request.form.get('name')
            game = game.lower()
            if game == 'fortnite':
                founded_users = User.query.filter_by(fortnite_player=True)
                for user in founded_users:
                    print(user.nick_name)
                return render_template('search.html', user=current_user, founded_users=founded_users)
            if game == 'minecraft':
                founded_users = User.query.filter_by(minecraft_player=True)
                for user in founded_users:
                    print(user.nick_name)
                return render_template('search.html', user=current_user, founded_users=founded_users)
            if game == 'league of legends' or game == 'lol':
                founded_users = User.query.filter_by(league_player=True)
                for user in founded_users:
                    print(user.nick_name)
                return render_template('search.html', user=current_user, founded_users=founded_users)
            if game == 'rainbow 6' or game == 'r6':
                founded_users = User.query.filter_by(r6_player=True)
                for user in founded_users:
                    print(user.nick_name)
                return render_template('search.html', user=current_user, founded_users=founded_users)
            if game == 'call of duty' or game == 'cod':
                founded_users = User.query.filter_by(cod_player=True)
                for user in founded_users:
                    print(user.nick_name)
                return render_template('search.html', user=current_user, founded_users=founded_users)
            if game == 'counter strike' or game == 'cs' or game == 'Counter Strike':
                founded_users = User.query.filter_by(cs_player=True)
                for user in founded_users:
                    print(user.nick_name)
                return render_template('search.html', user=current_user, founded_users=founded_users)

    return render_template('search.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteID']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted successfully!', category='success')

        return jsonify({})


@views.route('/forYou', methods=['POST', 'GET'])
@login_required
def forYou():
    j = 0
    k = 0

    def new_user(list_all, j, k, found_user):
        if k < 5 and j < 5 and list_all[j][k] != current_user:
            i = k + 1
            h = j + 1
            return render_template('forYou.html', user=list_all[j][k], found_users_list=found_user)
        else:
            return forYou()

    def user_list(found_user):
        rand2 = User.query.order_by(func.random()).limit(2).all()
        for user in rand2:
            print(user.nick_name)

        print(rand2)
        matching_ok = True
        grades = []
        for user in rand2:
            matched_user = matching(current_user, user)
            grades += [matched_user]
            print(grades)

        list_all = []
        for i in range(0, len(rand2)):
            list_all.append((rand2[i], grades[i]))

        print(sorted(list_all, key=lambda details: details[1], reverse=True))
        list_all = sorted(list_all, key=lambda details: details[1], reverse=True)
        print(current_user)
        return new_user(list_all, j, k, found_user)

    if request.method == 'POST':
        friend_request = request.form['friend']
        print(friend_request)

        # when sending friend request:
        # add his username to my pending requests and my username to his friend requests

        my_user = User.query.filter_by(nick_name=current_user).first()
        if my_user.sended_requests is None:
            my_user.sended_requests = friend_request + ','
        else:
            my_user.sended_requests += friend_request + ','
        db.session.commit()

        friend_user = User.query.filter_by(nick_name=friend_request).first()
        if friend_user.pending_requests is None:
            friend_user.pending_requests = current_user.nick_name + ','
        else:
            friend_user.pending_requests += current_user.nick_name + ','
        db.session.commit()

        all_users = User.query.all()
        found_user = []
        for user in all_users:
            if user.nick_name in current_user.friends:
                forYou()
            elif user.username in current_user.pending_requests:
                forYou()
            elif user.username in current_user.sended_requests:
                forYou()
            else:
                found_user.append([user])
                return user_list(found_user)

    return user_list([])
