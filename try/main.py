from flask import Flask, flash
from flask_socketio import send, SocketIO
from website import create_app, socketio
from flask_login import current_user
from website import socketio

from flask import session, request, render_template
from flask_socketio import emit, join_room, leave_room

app = create_app()
# socketio = SocketIO(app, cors_allowed_origins='*')

import eventlet
import eventlet.wsgi
eventlet.monkey_patch()
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")


@socketio.on('joined')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print(message)
    room = session.get('room')
    join_room(room)
    print(str(current_user.nick_name)+ ' has entered the room.')
    emit('status', {'msg': str(current_user.nick_name) + ' has entered the room.'}, room=room)


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    print(message, room)
    if message['msg'] == '' or message['msg'] == ' ':
        flash('Cannot send an empty message')
    else:
        emit('message', {'msg': str(current_user.nick_name) + ': ' + message['msg']}, room=room)


@socketio.on('left')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': str(current_user.nick_name) + ' has left the room.'}, room=room)



if __name__ == '__main__':
    print('running 3')
    # eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    # app.run(debug=True)
    # socketio.run(app)
    socketio.run(app, host='0.0.0.0', port='5000', debug=True)



