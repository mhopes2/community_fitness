from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User
from flask_app.models.message import Message


@app.route('/create_message')
def create_message():

    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id":session['user_id']
    }

    user = User.get_by_id(data)
    users = User.get_all()


    return render_template('create_message.html',users = users, user=user)

@app.route('/save/message',methods=['POST'])
def save_message():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "message": request.form['message'],
        "sender_id": request.form['sender_id'],
        "receiver_id": request.form['receiver_id'],
    }
    print(data)
    Message.save(data)
    return redirect('/dashboard')

@app.route('/view/all_messages')
def view_messages():

    data = {
        'id': session['user_id']
    }

    messages=Message.get_user_messages(data)

    return render_template('view_all_messages.html', messages = messages, user = User.get_by_id(data))

@app.route('/reply/message/<int:message_id>')
def reply_message(message_id):
    print(message_id)
    data = {
        'id': message_id
    }
    
    message = Message.reply_message(data)

    return render_template('reply_message.html', message = message)

@app.route('/delete/message/<int:message_id>')
def del_message(message_id):
    data = {
        'id': message_id
    }
    Message.delete(data)
    return redirect('/view/all_messages')