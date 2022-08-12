from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

db = "eventmanager"

class Event:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.time = data['time']
        self.duration = data['duration']
        self.location = data['location']
        self.street = data['street']
        self.apt = data['apt']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.users = None


    @classmethod
    def get_all_events(cls):
        query = "SELECT * FROM events LEFT JOIN users on user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        print(results)
        events = []
        for row in results:
            temp_event = cls(row)
            temp_event.users = User(row)
            events.append(temp_event)
        print(events)
        return events

    @classmethod
    def get_event(cls, data):
        query = "SELECT * FROM events LEFT JOIN users on user_id = users.id where events.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)

        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO events (name, date, time, duration, location, street, city, state, zip, description, user_id) VALUES (%(name)s, %(date)s, %(time)s, %(duration)s, %(location)s, %(street)s, %(city)s, %(state)s, %(zip)s, %(description)s %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE events SET name=%(name)s, date=%(date)s, time=%(time)s, duration=%(duration)s, location=%(location)s, street=%(street)s, city=%(city)s, state=%(state)s, zip=%(zip)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def del_event(cls, data):
        query = "DELETE from events WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_event_with_users( cls , data ):
        query = "SELECT * FROM events JOIN users ON users.id = events.users_id WHERE events.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if results:
            event = cls(results[0])
            for row_from_db in results:
                user_data = {
                    'id' : row_from_db['users.id'],
                    'first_name' : row_from_db['first_name'],
                    'last_name' : row_from_db['last_name'],
                    'email' : row_from_db['email'],
                    'password' : row_from_db['password'],
                    "dob": row_from_db['dob'],
                    "ustreet": row_from_db['ustreet'],
                    "uapt": row_from_db['uapt'],
                    "ucity": row_from_db['ucity'],
                    "ustate": row_from_db['ustate'],
                    "uzip": row_from_db['uzip'],
                    'created_at' : row_from_db['users.created_at'],
                    "updated_at" : row_from_db["users.updated_at"]
                }
                event.users = (User(user_data))
            return event
        return False

    @staticmethod
    def validate_event(event):
        is_valid = True
        query = "SELECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,event)
        if len(results) >= 1:
            flash("Event already exists", "eventadd")
        if (event['name']) == "":
            flash("Event name must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['date']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['time']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if len(event['duration']) < 1:
            flash("Duration must be longer than 30 minutes","eventadd")
            is_valid = False
        if (event['location']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['street']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['city']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['state']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if len(event['zip']) < 5:
            flash("Please input proper zip code","eventadd")
            is_valid = False
        if (event['description']) == "":
            flash("Add some info please.","eventadd")
            is_valid = False
        return is_valid