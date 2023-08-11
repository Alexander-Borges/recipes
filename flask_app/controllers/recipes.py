from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User 
from flask_app.models.recipe import Recipe 
from flask import flash 
from flask_bcrypt import Bcrypt
from datetime import datetime
bcrypt = Bcrypt(app)


########## GET ROUTES #############

@app.route("/recipes/dashboard")
def recipes_dashboard():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")

    # TO DO:
    # Get all the recipes and send to the template
    #user = User.get_by_id(session["user_id"])
    user = User.get_by_id(session["user_id"])  # Retrieve the user object
    recipes = Recipe.get_all()  # Make sure you have a get_all() method in your Recipe model
    return render_template("dashboard.html", user=user, recipes=recipes)

#Render Page Details Page for One Recipe
@app.route("/recipes/<int:recipe_id>")
def recipe_detail(recipe_id):
    print("In details: ", recipe_id) 
    # Need to get that recipe from the database
    recipe = Recipe.get_by_id(recipe_id)
    # Pass the recipe into the template
    return render_template("recipe_detail.html")

# Render Page with Create Form
@app.route("/recipes/new")
def create_page():
    print("In create route.")
    return render_template("create_recipe.html")

# Render Page with Edit Form
@app.route("/recipes/edit/<int:recipe_id>")
def edit_page(recipe_id):
    print("In edit page: ", recipe_id)
    recipe = Recipe.get_by_id(recipe_id)
    # Need to get that recipe from the database
    # Pass the recipe into the template
    return render_template("edit_recipe.html", recipe = recipe)


# GET Action Routes:
# Delete Route (GET request)
@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    print("In delete page: ", recipe_id)
    # Call delete method
    return redirect("/recipes/dashboard")

######## POST Routes ########


# CREATE (Process Form)
@app.route("/recipes", methods=["POST"])
def create_recipe():
    print("In the create process POST route: ", request.form)
    recipe_data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under_30": request.form["under_30"],
        "user_id": request.form["user_id"]
    }

    print("Recipe Data:", recipe_data)

    try:
        Recipe.save(recipe_data)
        flash("Recipe created successfully!", "success")
    except Exception as e:
        flash("Error creating recipe: " + str(e), "danger")

    return redirect("/recipes/dashboard")

# Update (Process Form)
@app.route("/recipes/update", methods=["POST"])
def update_recipe():
    print("In update POST route: ", request.form)
    return redirect("/recipes")


