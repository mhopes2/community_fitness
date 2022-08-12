from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User
from flask_app.models.message import Message


@app.route('/add_message')
def add_message():

    if 'id' not in session:
        return redirect('/logout')

    data = {
        "id":session['id']
    }

    return render_template('newmessage.html',user=User.get_by_id(data))

@app.route('/save/message',methods=['POST'])
def save_message():

    if not Message.validate_message(request.form):
        return redirect('/add_message')

    data = {
        "message": request.form['message'],
        "from_id": request.form['from_id'],
        "from_name": request.form['from_name'],
        "to_id": request.form['to_id'],
        "to_name": request.form['to_name'],
        "user_id": session['id']
    }
    print(data)
    Message.save(data)
    return redirect('/success/')


@app.route('/edit/message/<int:id>')
def edit_message(id):

    if 'id' not in session:
        return redirect('/logout')

    data = {
        "id": id
    }
    
    return render_template("editmessage.html",one_message=Message.get_message(data))

@app.route('/update/message/', methods=['POST'])   
def update_message():

    if not Message.validate_addmessage(request.form):
        return redirect(f'/edit/message/{request.form["id"]}')

    data = {
        "message": request.form['message'],
        "from_id": request.form['from_id'],
        "from_name": request.form['from_name'],
        "to_id": request.form['to_id'],
        "to_name": request.form['to_name'],
        "id": request.form['id']
    }

    print(data)
    Message.update(data)
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def view_message(id):

    data = {
        'id': id
    }

    message=Message.get_message(data)

    return render_template('/show_message.html/', one_message = message, user = User.get_by_id(data))

@app.route('/delete/message/<int:id>')
def del_message(id):
    data = {
        'id': id
    }
    Message.delete(data)
    return redirect('/dashboard')