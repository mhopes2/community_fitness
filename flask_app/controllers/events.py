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

    return render_template('newevent.html',user=User.get_by_id(data))

@app.route('/save/event',methods=['POST'])
def save_event():

    if not Event.validate_addevent(request.form):
        return redirect('/add_event')

    data = {
        "name": request.form['name'],
        "date": request.form['date'],
        "time": request.form['time'],
        "duration": request.form['duration'],
        "location": request.form['location'],
        "description": request.form['description'],
        "posted_by": request.form['posted_by'],
        "user_id": session['id']
    }
    print(data)
    Event.save(data)
    return redirect('/success/')


@app.route('/edit/event/<int:id>')
def edit_event(id):

    if 'id' not in session:
        return redirect('/logout')

    data = {
        "id": id
    }
    
    return render_template("editevent.html",one_event=Event.get_event(data))

@app.route('/update/event/', methods=['POST'])   
def update_event():

    if not Event.validate_event(request.form):
        return redirect(f'/edit/event/{request.form["id"]}')

    data = {
        "name": request.form['name'],
        "date": request.form['date'],
        "time": request.form['time'],
        "duration": request.form['duration'],
        "location": request.form['location'],
        "description": request.form['description'],
        "posted_by": request.form['posted_by'],
        "id": request.form['id']
    }

    print(data)
    Event.update(data)
    return redirect('/success/')

@app.route('/view/<int:id>')
def view_event(id):

    data = {
        'id': id
    }

    event=Event.get_event(data)


    return render_template('/show_event.html/', one_event = event, user = User.get_seller(data))

@app.route('/delete/event/<int:id>')
def del_event(id):
    data = {
        'id': id
    }
    Event.del_event(data)
    return redirect('/success/')