from crypt import methods
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.event import Event
import pprint

@app.route('/add_event')
def add_event():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id":session['user_id']
    }

    return render_template('createEvent.html',user=User.get_by_id(data))

@app.route('/event/save',methods=['POST'])
def save_event():
    if 'user_id' not in session:
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
        "user_id": session["user_id"]
    }
    print(data)
    events_id = Event.save(data)
    data_dict = {
        "event_id":events_id,
        "user_id": session["user_id"]
    }
    Event.attending_event(data_dict)
    print(events_id)
    return redirect('/dashboard')


@app.route('/event/edit/<int:event_id>')
def edit_event(event_id):
    if 'user_id' not in session:
        return redirect('/logout')
    event_data = {
        "event_id": event_id
    }

    user_data = {
        "id": session['user_id']
    }
    
    return render_template("editEvent.html", event=Event.get_event(event_data), user = User.get_by_id(user_data))

@app.route('/event/update/<int:event_id>', methods=['POST'])   
def update_event(event_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect(f'/event/edit/{event_id}')
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
        "event_id": event_id
    }
    Event.update(data)
    print(data)
    return redirect('/dashboard')

@app.route('/view/event/<int:event_id>')
def view_event(event_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    event_data = {
        'id': event_id
    }
    event = Event.get_event_with_users(event_data)
    user = User.get_by_id(user_data)
    list_of_joined_events_users = Event.list_of_users_joined_event(event_data)
    print(user)
    return render_template('join_event.html', event = event ,user = user, userEventsList = list_of_joined_events_users)


@app.route('/event/delete/<int:event_id>')
def del_event(event_id):
    if 'user_id' not in session:
        return redirect('/logout')
    Event.del_event({'event_id':event_id})
    return redirect('/dashboard')

@app.route('/cancel_event/<int:event_id>')
def unjoin(event_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        'event_id': event_id
    }
    Event.unjoin_event(data)
    print(data)
    return redirect('/dashboard')

@app.route('/join/event', methods =["POST"])
def join_event():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session['user_id'],
        "event_id": request.form['event_id']
    }
    Event.attending_event(data)
    return redirect('/dashboard')