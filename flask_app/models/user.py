from pprint import pprint
from flask import session,flash
from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app.models import event

db = "eventmanager"

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.dob = data['dob']
        self.ustreet = data['ustreet']
        self.uapt = data['uapt']
        self.ucity = data['ucity']
        self.ustate = data['ustate']
        self.uzip = data['uzip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_signedup_event = []

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.","register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 character","register")
            is_valid = False
        if len(results) >= 1:
            flash("Email already taken","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Provide a proper email","register")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be 8 character minimum","register")
            is_valid = False
        if (user['password']) != (user['conf_pass']):
            flash("Password does not match","register")
            is_valid = False
        return is_valid

    def validate_login(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(user['email']) < 8:
            flash("email does not match", "login")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Provide a proper email","login")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password is invalid","login")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_updateuser(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.","register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 character","register")
            is_valid = False
        if len(results) >= 1:
            flash("Email already taken","register")
            is_valid=False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = 'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, dob=%(dob)s, ustreet=%(ustreet)s, uapt=%(uapt)s, ucity=%(ucity)s, ustate=%(ustate)s, uzip=%(uzip)s WHERE id=%(user_id)s;'
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def get_joined_events(cls,data):
        query = """SELECT * FROM users 
        LEFT JOIN signedUp_event ON users.id = signedUp_event.user_id 
        LEFT JOIN events ON events.id = signedUp_event.event_id 
        WHERE users.id = %(id)s;"""
        results = connectToMySQL(db).query_db(query,data)
        user = cls(results[0])
        print(user)
        for row in results:
            pprint(row,sort_dicts=False)
            #if there are no events signed up for
            if row['events.id'] == None:
                break
            event_data = {
                "id": row['events.id'],
                "title": row['title'],
                "description": row['description'],
                "date": row['date'],
                "start_time": row['start_time'],
                "end_time": row['end_time'],
                "num_of_pple": row['num_of_pple'],
                "street": row['street'],
                "apt": row['apt'],
                "city": row['city'],
                "state": row["state"],
                "zip": row['zip'],
                "created_at": row['events.created_at'],
                "updated_at": row['events.updated_at'],
                "user_id": row["user_id"]
            }
            user.users_signedup_event.append(event.Event(event_data))
            print(user)
        return user
