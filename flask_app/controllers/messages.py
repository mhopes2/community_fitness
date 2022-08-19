from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User
from flask_app.models.message import Message


@app.route('/add_message')
def add_message():

    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id": session['user_id']
    }

    return render_template('create_message.html', users=User.get_all())

@app.route('/save/message',methods=['POST'])
def save_message():
    if 'user_id' not in session:
        return redirect('/')
        
    if not Message.validate_message(request.form):
        return redirect('/add_message')

    data = {
        "message": request.form['message'],
        "from_id": request.form['from_id'],
        "from_name": request.form['from_name'],
        "to_id": request.form['to_id'],
        "to_name": request.form['to_name'],
    }
    print(data)
    Message.save(data)
    return redirect('/dashboard')

@app.route('/send/message',methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect('/')
        
    if not Message.validate_message(request.form):
        return redirect('/view_message')

    data = {
        "message": request.form['message'],
        "from_id": request.form['from_id'],
        "from_name": request.form['from_name'],
        "to_id": request.form['to_id'],
        "to_name": request.form['to_name']
    }

    print(data)
    Message.save(data)
    return redirect('/dashboard')

@app.route('/view/message/<int:id>')
def view_message(id):

    data = {
        'id': id
    }

    message=Message.get_message(data)

    return render_template('/view_message.html/', one_message = message)

@app.route('/view/messages/')
def view_messages():
    data = {
        'id': session['user_id']
    }

    return render_template('/view_all_messages.html', all_messages = Message.get_all(data))

@app.route('/delete/message/<int:id>')
def del_message(id):
    data = {
        'id': id
    }
    Message.delete(data)
    return redirect('/dashboard')