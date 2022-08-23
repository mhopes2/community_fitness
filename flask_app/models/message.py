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
    def get_all( cls, data ):
        query = "SELECT users.first_name as from_name, users2.first_name as to_name, messages.* FROM users LEFT JOIN messages ON users.id = messages.from_id LEFT JOIN users as users2 ON users2.id = messages.to_id WHERE users2.id =  %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        messages = []
        for message in results:
                messages.append( cls(message) )
        return messages

    @classmethod
    def get_message(cls, data):
        query = "SELECT * FROM messages LEFT JOIN users on to_id = users.id where messages.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)

        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (message, from_id, from_name, to_id, to_name, users_id) VALUES (%(message)s, %(from_id)s, %(from_name)s,%(to_id)s,%(to_name)s, %(from_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE from messages WHERE messages.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @staticmethod
    def validate_message(message):
        is_valid = True
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,message)
        if len(message['message']) < 2:
            flash("You will need a long message")
            is_valid = False
        #if user['id'] == session.user_id:
            #flash("Don't send a message to yourself dork")
            #is_valid = False
        return is_valid

    @classmethod
    def get_name(cls,data):
        query = "SELECT first_name FROM users where users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        return cls(results[0])