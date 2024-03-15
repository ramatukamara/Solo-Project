from float_in_poetry import DATABASE
from float_in_poetry.config.mysqlconnections import connectToMySQL
from float_in_poetry.models.poems_model import Poem
from flask import flash, session
from float_in_poetry import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users(name, username, email, password) VALUES(%(name)s, %(username)s, %(email)s, %(password)s)"
        return connectToMySQL("poems_db").query_db(query, data)
    
    @classmethod
    def get_users_username(cls, user_id):
        query = "SELECT username FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL("poems_db").query_db(query, {'user_id': user_id})
        if result:
            return result[0]['username']
        return None
        
    @classmethod
    def get_user_with_poems(cls, user_id):
        query = """
            SELECT users.*, poems.*
            FROM users
            LEFT JOIN poems ON users.id = poems.user_id
            WHERE users.id = %(user_id)s;
        """
        data = {'user_id': user_id}
        results = connectToMySQL("poems_db").query_db(query, data)

        if not results:
            return None

        user_data = results[0]
        user = cls({
            'id': user_data['id'],
            'name': user_data['name'],
            'username': user_data['username'],
            'email': user_data['email'],
            'password': user_data['password'],
            'created_at': user_data['created_at'],
            'updated_at': user_data['updated_at']
        })

        user.poems = []
        for row in results:
            user.poems.append(Poem(row))

        return user
        
# ================================== Validators 
    
    @staticmethod
    def confirm(user):
        is_valid = True
        if len(user['name']) == 0:
            flash('Name is required.','register_name')
            is_valid = False
        if len(user['email']) < 3:
            flash('Email is required.', 'register_email')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!",'register_invalid')
            is_valid = False
        if len(user['password']) == 0:
            flash('Password is required.','register_password')
            is_valid = False
        if user['password'] != user["confirm_password"]:
            flash('Passwords do not match!','register_confirm')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['username']) == 0:
            flash('Username is required.', 'login_username')
            is_valid = False
        if len(user['password']) == 0:
            flash('Password is required.', 'login_password')
            is_valid = False
        if is_valid:
            potential_user = User.get_users_username({'username':user['username']})
            if not potential_user or not bcrypt.check_password_hash(potential_user.password, user['password']):
                flash('Incorrect Username or Password', 'login')
                is_valid = False
            else:
                session['uid'] = potential_user.id

            
        return is_valid