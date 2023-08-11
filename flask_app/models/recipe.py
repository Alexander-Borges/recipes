from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
from datetime import datetime
import re

class Recipe:
    db = "recipes"

    def __init__(self, recipe):
        self.id = recipe['id']
        self.name = recipe['name']
        self.description = recipe['description']
        self.instructions = recipe['instructions']
        self.date_made = recipe["date_made"]
        self.under_30 = recipe['under_30']
        self.created_at = recipe['created_at']
        self.updated_at = recipe['updated_at']
        self.user = None

    # GET RECIPE BY ID
    def get_by_id(cls, recipe_id):

        # Get recipe data with user data who created it 
        query = """
                SELECT * FROM recipes 
                JOIN users on recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """
        data = {
            "id": recipe_id
        }
        recipe_dict = connectToMySQL(cls, db).query_db(query, data)[0]
        print(recipe_dict)
        # Make a recipe object from data
        recipe_object = Recipe(recipe_dict)
        # Make a user object from data
        user_object = user.User({
            "id" : recipe_dict["users.id"],
            "first_name" : recipe_dict["first_name"],
            "last_name" :recipe_dict["last_name"],
            "email" : recipe_dict["email"],
            #"password" : recipe_dict["password"],
            "created_at" : recipe_dict["users.created_at"],
            "updated_at": recipe_dict["users.updated_at"]
        })
        # Associate user with recipe
        recipe.user = user_object
        # Return recipe
        return recipe_object

    # GET ALL
    @classmethod
    def get_all(cls):

        # Get all recipes, and the user info for the creators
        query = """
                SELECT * FROM recipes
                JOIN users on recipes.user_id = users.id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        # Make a list to hold recipe objects to return
        print("Retrieved recipes:", results)
        recipes = []
        # Iterate thru the list of recipe dictionaries
        for recipe_dict in results:
            # convert data into a recipe object
            recipe_object = Recipe(recipe_dict)
            # convert joined user data into a user object
            user_object = user.User({
                "id" : recipe_dict["users.id"],
                "first_name" : recipe_dict["first_name"],
                "last_name" :recipe_dict["last_name"],
                "email" : recipe_dict["email"],
                #"password" : recipe_dict["password"],
                "created_at" : recipe_dict["users.created_at"],
                "updated_at": recipe_dict["users.updated_at"]
            })
            # Associate user with recipe
            recipe_object.user = user_object
            # append to list
            recipes.append(recipe_object)
        # Return the list of recipes
        return recipes


    # CREATE VALID RECIPE
    @classmethod
    def save(cls, recipe_data):
        # create a new dict to hold the modified data 
        new_recipe_data = {
            "name": recipe_data["name"],
            "description": recipe_data["description"],
            "instructions": recipe_data["instructions"],
            "date_made": datetime.strptime(recipe_data['date_made'], '%Y-%m-%d').date(),
            "under_30": recipe_data["under_30"],
            "user_id": recipe_data["user_id"]
            }
        # takes data dictionary from request.form 
        # validates data
        # Insert the recipe into the database
        print("Inserting the following data:")
        print(new_recipe_data)  # Add this line to print the data before insertion
    
        
        query = """
                INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);
                """
        connectToMySQL(cls.db).query_db(query, new_recipe_data)
        # return id? or False if the validation fails

    # DELETE RECIPE BY ID 
        # Delete recipe using the id

    # UPDATE RECIPE
        # takes data dictionary from request.form 
        # validates data
        # Returns the new recipe as an object or False if the validation fails