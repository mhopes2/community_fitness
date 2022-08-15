from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')

    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    
    id = User.save(data)

    session['id'] = id
    session['first_name'] = request.form['first_name']
    return redirect('/success')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user = User.get_by_id(user_data), events = Event.get_all_events(), messages = Message.get_all(user_data))

@app.route('/update',methods=['POST'])
def update():
    if not User.validate_updateuser(request.form):
        return redirect('/')

    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "dob": request.form['dob'],
        "ustreet": request.form['ustreet'],
        "uapt": request.form['uapt'],
        "ucity": request.form['ucity'],
        "ustate": request.form['ustate'],
        "uzip": request.form['uzip']
    }
    
    id = User.save(data)

    session['id'] = id
    session['first_name'] = request.form['first_name']
    return redirect('/success')

@app.route('/login',methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    elif not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password","login")
        return redirect('/')
    session['id'] = user.id
    return redirect('/dashboard')

@app.route('/success')
def success():
    if 'id' not in session:
        return redirect('/logout')

    data = {
        'id': session['id']
    }

    return render_template("account_page.html", user=User.get_by_id(data))

        # return render_template("dashboard.html", all_users=User.get_all_users())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')