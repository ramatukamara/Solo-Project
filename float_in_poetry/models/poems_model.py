from float_in_poetry.config.mysqlconnections import connectToMySQL
from flask import flash


class Poem:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.your_poem = data['your_poem']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']    

    @classmethod
    def get_all(cls):
        query = """
            SELECT poems.*, users.username 
            FROM poems 
            JOIN users ON users.id = poems.user_id
        """
        results = connectToMySQL("poems_db").query_db(query)
        poems = []
        if results:
            for row in results:
                poem_data = {
                    'id': row['id'],
                    'title': row['title'],
                    'your_poem': row['your_poem'],
                    'description': row['description'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'user_id': row['user_id'],
                    'username': row['username']  
                }
                poems.append(cls(poem_data))
        return poems
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM poems WHERE id = %(id)s;"
        result = connectToMySQL("poems_db").query_db(query, {'id': id})
        if result:
            return cls(result[0])
        return None

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO poems (title, your_poem, description, user_id)
            VALUES (%(title)s, %(your_poem)s, %(description)s, %(user_id)s);
        """
        return connectToMySQL("poems_db").query_db(query, data)

    
    @classmethod
    def update(cls, data):  
        query = """
            UPDATE poems
            SET title = %(title)s, your_poem = %(your_poem)s, description = %(description)s
            WHERE id = %(id)s;
        """
        return connectToMySQL("poems_db").query_db(query, data)


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM poems WHERE id = %(id)s;"
        return connectToMySQL("poems_db").query_db(query, {'id': id})
    
    # ================================== Validators 
    
    @staticmethod
    def validate_poem(poem):
        is_valid = True
        if len(poem['title']) == 0:
            flash('Please enter a valid Title!', 'create_poem_title')
            is_valid = False
        if len(poem['your_poem']) == 0:
            flash('Poem box cannot be empty!', 'create_poem_poem')
            is_valid = False
        if len(poem['description']) == 0:
            flash('Please describe your entry!', 'create_poem_descrip')
            is_valid = False
        return is_valid

