from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    users = User.get_all()
    return render_template("index.html", users = users)

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
    
    user_info = User.save(data)

    session['user_id'] = user_info
    session['first_name'] = request.form['first_name']

    user_route_id = str(session['user_id'])
    return redirect('/success/'+ user_route_id)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user = User.get_joined_events(user_data), messages = Message.get_all(user_data))

@app.route('/update/<int:user_id>',methods=['POST'])
def update(user_id):

    data ={ 
        "user_id": user_id,
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
    
    User.update(data)
    user_session = session['user_id']
    return redirect ('/success/'+ str(user_session))

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
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/success/<int:user_id>')
def edit(user_id):
    data = {
        "id": user_id
    }
    #user = User.get_by_id({'user_id': user_id})

    return render_template("account_page.html", user = User.get_by_id(data))

        # return render_template("dashboard.html", all_users=User.get_all_users())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')