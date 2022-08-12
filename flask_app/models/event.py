from asyncio.windows_events import NULL
from pickle import FALSE
import pprint
from flask import session,flash
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
        self.posted_by = data['posted_by']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']






    @classmethod
    def get_all_events(cls):
        query = "SELECT * FROM events LEFT JOIN users on user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        print(results)
        events = []
        for row in results:
            temp_event = cls(row)
            temp_event.seller = User(row)
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
        query = "INSERT INTO events (price, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE events SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def del_event(cls, data):
        query = "DELETE from events WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @staticmethod
    def validate_addevent(event):
        is_valid = True
        query = "SELECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,event)
        if (event['model']) == "":
            flash("Input model,  must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['make']) == "":
            flash("Input make,  must be at least 3 characters.","eventadd")
            is_valid = False
        if (event['description']) == "":
            flash("Add some info please.","eventadd")
            is_valid = False
        if len(event['year']) < 4:
            flash("Input proper year please.","eventadd")
            is_valid = False
        if len(event['price']) < 1:
            flash("Input at least a buck","eventadd")
            is_valid = False
        return is_valid