from flask import render_template, request, redirect, session, url_for
from flask_app.models import recipe  #change this import line based on your extra .py file for generating OOP instances
from flask_app import app


@app.route("/recipes")     # lines 6 through 11 can be changed depending on what we need server.py to do.
def r_get_recipes():
    if 'user_id' not in session:
        return redirect('/')
    # call the get all classmethod to get all users
    return render_template("recipes.html", recipes = recipe.Recipe.get_all())

@app.route('/recipes/new')
def r_new_recipes():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipes/add', methods = ['POST'])
def f_add_recipes():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    recipe.Recipe.add_recipe(request.form)
    return redirect('/recipes')

@app.route('/recipes/view/<int:id>')
def r_view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('view_recipe.html', recipe = recipe.Recipe.get_one({'id':id}))

@app.route('/recipes/edit/<int:id>')
def r_edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('edit_recipe.html', recipe = recipe.Recipe.get_one({'id':id}))

@app.route('/recipes/edit', methods = ['POST'])
def f_edit_recipe():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(url_for('r_edit_recipe', id = request.form['id']))
    recipe.Recipe.update_recipe(request.form)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    recipe.Recipe.delete_recipe({'id':id})
    return redirect('/recipes')