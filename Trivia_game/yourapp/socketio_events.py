from flask_socketio import join_room, leave_room, emit
from yourapp import socketio

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'msg': f"{data['username']} has joined the room."}, room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f"{data['username']} has left the room."}, room=room)

@socketio.on('send_question')
def handle_send_question(data):
    room = data['room']
    emit('new_question', data, room=room)

@socketio.on('send_answer')
def handle_send_answer(data):
    room = data['room']
    emit('new_answer', data, room=room)
