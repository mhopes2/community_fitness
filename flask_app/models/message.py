from asyncio.windows_events import NULL
from pickle import FALSE
import pprint
from queue import Empty
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
    def get_all_cars(cls):
        query = "SELECT * FROM cars LEFT JOIN users on user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        print(results)
        cars = []
        for row in results:
            temp_car = cls(row)
            temp_car.seller = User(row)
            cars.append(temp_car)
        print(cars)
        return cars

    @classmethod
    def get_car(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users on user_id = users.id where cars.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)

        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (price, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def del_car(cls, data):
        query = "DELETE from cars WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @staticmethod
    def validate_addcar(car):
        is_valid = True
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,car)
        if (car['model']) == "":
            flash("Input model,  must be at least 3 characters.","caradd")
            is_valid = False
        if (car['make']) == "":
            flash("Input make,  must be at least 3 characters.","caradd")
            is_valid = False
        if (car['description']) == "":
            flash("Add some info please.","caradd")
            is_valid = False
        if len(car['year']) < 4:
            flash("Input proper year please.","caradd")
            is_valid = False
        if len(car['price']) < 1:
            flash("Input at least a buck","caradd")
            is_valid = False
        return is_valid