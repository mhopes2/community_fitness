import pprint
from flask import session,flash
from flask_app.config.mysqlconnection import connectToMySQL

db = "eventmanager"

class Message:
    def __init__( self , data ):
        self.id = data['id']
        self.message = data['message']
        self.sender_id = data['sender_id']
        self.from_name = data['from_name']
        self.receiver_id = data['receiver_id']
        self.to_name = data['to_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_messages( cls, data ):
        query = """SELECT CONCAT_WS(" ",users.first_name,users.last_name) as from_name, CONCAT_WS(" ",users2.first_name,users2.last_name) as to_name, messages.* FROM users 
        LEFT JOIN messages ON users.id = messages.sender_id 
        LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id = %(id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        messages = []
        for message in results:
                messages.append( cls(message) )
        return messages

    @classmethod
    def get_message(cls, data):
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def reply_message(cls, data):
        query = """SELECT CONCAT_WS(" ",users.first_name,users.last_name) as from_name, CONCAT_WS(" ",users2.first_name,users2.last_name) as to_name, messages.* FROM users 
        LEFT JOIN messages ON users.id = messages.receiver_id 
        LEFT JOIN users as users2 ON users2.id = messages.sender_id WHERE users2.id = %(id)s;"""
        results = connectToMySQL(db).query_db(query, data)
        messages = []
        for message in results:
                messages.append( cls(message) )
        return messages

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (message,sender_id,receiver_id) VALUES (%(message)s,%(sender_id)s,%(receiver_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE from messages WHERE messages.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result