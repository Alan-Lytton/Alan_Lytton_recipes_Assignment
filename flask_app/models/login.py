# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
db = "recipes_schema"

class Login:

    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        # adjust the "FROM" target to be the required table
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def get_one_reg(cls, data):
        query = "select users.id, users.first_name, users.last_name from users WHERE id = %(user_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_login(cls, data):
        query = "select users.id, users.first_name, users.last_name from users WHERE email = %(email)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s) ;"
        return connectToMySQL(db).query_db(query, data)


    @staticmethod
    def validate_reg(user):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, user)
        is_valid = True
        if len(user['fname']) < 2 or not user['fname'].isalpha():
            flash('First Name must be more than 2 characters and only contain letters.', 'reg')
            is_valid = False
        if len(user['lname']) < 2 or not user['lname'].isalpha():
            flash('Last Name must be more than 2 characters and only contain letters.', 'reg')
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email format.', 'reg')
            is_valid = False
        if len(results) > 0:
            flash('Email is already registered.', 'reg')
            print(results)
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash('Password must be at least 8 characters long', 'reg')
            flash('Password must contain one upper case letter', 'reg')
            flash('Password must contain one lower case letter', 'reg')
            flash('Password must contain one number and one special character', 'reg')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash('Provided passwords do not match.', 'reg')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, user)
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email format.', 'login')
            is_valid = False
        elif len(results) < 1:
            flash('Invalid Email/Password combination.', 'login')
            is_valid = False
        elif not bcrypt.check_password_hash(results[0]['password'], user['password']):
            flash('Invalid Email/Password combination.', 'login')
            is_valid = False
        return is_valid
