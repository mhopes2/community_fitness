from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

db = "eventmanager"

class Event:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.date = data['date']
        self.start_time= data['start_time']
        self.end_time = data['end_time']
        self.num_of_pple = data['num_of_pple']
        self.street = data['street']
        self.apt = data['apt']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.users_who_joined_event = []
        


    @classmethod
    def get_all_events(cls):
        query = "SELECT * FROM events;"
        results = connectToMySQL(db).query_db(query)
        print(results)
        events = []
        for row in results:
            events.append( cls(row))
        print(events)
        return events


    @classmethod
    def get_event(cls, data):
        query = "SELECT * FROM events LEFT JOIN users on user_id = users.id where events.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)

        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO events (title, description, date, start_time, end_time, num_of_pple, street, apt, city, state, zip, user_id) VALUES (%(title)s, %(description)s, %(date)s, %(start_time)s, %(end_time)s,%(num_of_pple)s, %(street)s,%(apt)s, %(city)s, %(state)s, %(zip)s, %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE events SET title=%(title)s, description=%(description)s, date=%(date)s, start_time=%(start_time)s, end_time=%(end_time)s, num_of_pple=%(num_of_pple)s, street=%(street)s,apt=%(apt)s, city=%(city)s, state=%(state)s, zip=%(zip)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def attending_event(cls,data):
        query = "INSERT INTO signedUp_event (user_id,event_id) VALUES (%(user_id)s,%(event_id)s);"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def event_not_yet_joined(cls,data):
        query = "SELECT * FROM events where events.user_id !=%(id)s;" 
        results = connectToMySQL(db).query_db(query, data)
        events = []
        for row in results:
            events.append(cls(row))
        print(events)
        return events

    @classmethod
    def del_event(cls, data):
        query = "DELETE from events WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_event_with_users( cls , data ):
        query = "SELECT * FROM events JOIN users ON users.id = user_id WHERE events.id = %(id)s;"
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
                event.users = (user.User(user_data))
            return event
        return False

    @staticmethod
    def validate_event(event):
        is_valid = True
        if (event['title']) == "":
            flash("Event title must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['description']) == "":
            flash("Add some info please.","eventadd")
            is_valid = False
        if (event['start_time']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if len(event['end_time']) < 1:
            flash("Duration must be longer than 30 minutes","eventadd")
            is_valid = False
        if len(event['num_of_pple']) < 0:
            flash("Num should be greater than 0","eventadd")
            is_valid = False
        if (event['street']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['apt']) == "":
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
        return is_valid