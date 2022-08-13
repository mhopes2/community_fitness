from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.event import Event

@app.route('/add_event')
def add_event():
    if 'id' not in session:
        return redirect('/logout')

    data = {
        "id":session['id']
    }

    return render_template('createEvent.html',user=User.get_by_id(data))

@app.route('/event/save',methods=['POST'])
def save_event():
    if not Event.validate_event(request.form):
        return redirect('/add_event')

    data = {
        "name": request.form['name'],
        "date": request.form['date'],
        "time": request.form['time'],
        "duration": request.form['duration'],
        "location": request.form['location'],
        "street": request.form['street'],
        "city": request.form['city'],
        "state": request.form['state'],
        "zip": request.form['zip'],
        "description": request.form['description'],
        "users_id": session['id']
    }
    print(data)
    Event.save(data)
    return redirect('/dashboard')


@app.route('/event/edit/<int:id>')
def edit_event(id):
    if 'id' not in session:
        return redirect('/logout')

    data = {
        "id": id
    }
    
    return render_template("editevent.html",one_event=Event.get_event(data))

@app.route('/event/update/<int:id>', methods=['POST'])   
def update_event():
    if not Event.validate_event(request.form):
        return redirect(f'/event/edit/{request.form["id"]}')

    data = {
        "name": request.form['name'],
        "date": request.form['date'],
        "time": request.form['time'],
        "duration": request.form['duration'],
        "spots": request.form['spots'],
        "location": request.form['location'],
        "street": request.form['street'],
        "city": request.form['city'],
        "state": request.form['state'],
        "zip": request.form['zip'],
        "description": request.form['description'],
    }

    print(data)
    Event.update(data)
    return redirect('/dashboard')

@app.route('/event/view/<int:id>')
def view_event(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }

    event=Event.get_event(data)


    return render_template('/show_event.html/', one_event = event, user = User.get_by_id(data))

@app.route('/event/delete/<int:id>')
def del_event(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Event.del_event(data)
    return redirect('/dashboard')

@app.route('/event')
def event():
    return render_template('join_event.html')