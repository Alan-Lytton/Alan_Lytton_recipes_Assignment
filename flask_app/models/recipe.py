#this whole file can be changed depending on what we need to do with the data and how we want our OOP instances to appear.

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = "recipes_schema"  #add DB name inside quotes

class Recipe:

    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        # adjust the "FROM" target to be the required table
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for recipe in results:
            one_recipe = cls(recipe)
            one_recipe.user = recipe['first_name']
            recipes.append(one_recipe)
        return recipes

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        only_recipe = cls(results[0])
        only_recipe.user = results[0]['first_name']
        return only_recipe


    @classmethod
    def add_recipe(cls,data):
        query = "INSERT INTO recipes (user_id, name, description, instructions, date_made, under_30) VALUES (%(user_id)s, %(name)s, %(desc)s, %(instruct)s, %(cook_date)s, %(under_30)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update_recipe(cls,data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(desc)s, instructions = %(instruct)s, date_made = %(cook_date)s, under_30 = %(under_30)s WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash('Recipe Name must be at least 3 characters long.')
            is_valid = False
        if len(recipe['desc']) < 3:
            flash('Description must be at least 3 characters long.')
            is_valid = False
        if len(recipe['instruct']) < 3:
            flash('Instructions must be at least 3 characters long.')
            is_valid = False
        if len(recipe['cook_date']) <= 0:
            flash('Date Cooked/Made must be provided.')
        return is_valid