from crypt import methods
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.event import Event
import pprint

@app.route('/add_event')
def add_event():
    if 'id' not in session:
        return redirect('/logout')

    data = {
        "id":session['user_id']
    }

    return render_template('createEvent.html',user=User.get_by_id(data))

@app.route('/event/save',methods=['POST'])
def save_event():
    if 'id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect('/add_event')

    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "date": request.form["date"],
        "start_time": request.form["start_time"],
        "end_time": request.form["end_time"],
        "num_of_pple": request.form["num_of_pple"],
        "street": request.form["street"],
        "apt": request.form["apt"],
        "city": request.form["city"],
        "state": request.form["state"],
        "zip": request.form["zip"],
        "user_id": session["id"]
    }
    print(data)
    events = Event.save(data)
    print(events)
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

@app.route('/view/event/<int:event_id>')
def view_event(event_id):
    if 'id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['id']
    }
    event_data = {
        'id': event_id
    }
    event = Event.get_event_with_users(event_data)
    user = User.get_by_id(user_data)
    print(event)
    print(user)
    return render_template('join_event.html', event = event ,user = user )

@app.route('/event/delete/<int:id>')
def del_event(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Event.del_event(data)
    return redirect('/dashboard')

@app.route('/join/event', methods =["post"])
def join_event():
    data = {
        "user_id": session['user_id'],
        "event_id": request.form['event_id']
    }
    Event.attending_event(data)
    return redirect('/dashboard')