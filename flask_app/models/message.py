import pprint
from flask import session,flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

db = "eventmanager"

class Message:
    def __init__( self , data ):
        self.id = data['id']
        self.message = data['message']
        self.from_id = data['from_id']
        self.from_name = data['from_name']
        self.to_id = data['to_id']
        self.to_name = data['to_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @classmethod
    def get_all( cls ):
        query = "SELECT * FROM messages JOIN users ON users.id = messages.users_id;"
        results = connectToMySQL(db).query_db(query)
        print(results)
        messages = []
        for row_from_db in results:
                message = cls(row_from_db)
                message.users = User(row_from_db)
                messages.append(message)
        return messages

    @classmethod
    def get_message(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users on user_id = users.id where cars.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)

        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (message, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE messages SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = "DELETE from messages WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @staticmethod
    def validate_message(message):
        is_valid = True
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,message)
        if (message['model']) == "":
            flash("Input model,  must be at least 3 characters.","caradd")
            is_valid = False
        if (message['make']) == "":
            flash("Input make,  must be at least 3 characters.","caradd")
            is_valid = False
        if (message['description']) == "":
            flash("Add some info please.","caradd")
            is_valid = False
        if len(message['year']) < 4:
            flash("Input proper year please.","caradd")
            is_valid = False
        if len(message['price']) < 1:
            flash("Input at least a buck","caradd")
            is_valid = False
        return is_valid