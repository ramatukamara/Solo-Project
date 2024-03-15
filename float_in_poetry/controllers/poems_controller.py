from flask import render_template, session, redirect, request
from float_in_poetry import app
from float_in_poetry.models.poems_model import Poem
from float_in_poetry.models.users_model import User


# =================================Fetch all poems from the database

@app.route('/homepage')
def homepage():
    if 'uid' not in session:
        return redirect('/')

    poems = Poem.get_all()
    user_id = session['uid']  
    user = User.get_users_username(user_id)  

    return render_template('homepage.html', poems=poems, user=user)


# ================================== Fetch one poem to view=====change for one

@app.route('/poem/<int:id>')
def view_poem(id):
    if 'uid' not in session:
        return redirect('/')

    poems = Poem.get_by_id(id)

    return render_template('poem_only.html', poems=poems)

# =======================================Create a new poem
@app.route('/new_poem')
def new_poem():
    if 'uid' not in session:
        return redirect('/login')
    return render_template('create_poem.html')

@app.route('/create_poem', methods=['POST'])
def create_poem():
    if 'uid' not in session:
        return redirect('/login')
    
    if not Poem.validate_poem(request.form):
        return redirect('/new_poem')

    data = {
        'title': request.form['title'],
        'your_poem': request.form['your_poem'],
        'description': request.form['description'],
        'user_id': session['uid'] 
    }
    Poem.create(data)
    return redirect('/homepage')

# =========================================Routes for editing

@app.route('/poem/<int:id>/edit')
def edit_poem(id):
    if 'uid' not in session:
        return redirect('/login')
        
    poem = Poem.get_by_id(id)

    return render_template('edit_poem.html', poem=poem)

@app.route('/poem/<int:id>/update', methods=['POST'])
def update_poem(id):
    if 'uid' not in session:
        return redirect('/login')

    data = {
        'id': id,
        'title': request.form['title'],
        'your_poem': request.form['your_poem'],
        'description': request.form['description'], 
    }

    if not Poem.validate_poem(data):
        return redirect(f'/poem/{id}/edit')

    Poem.update(data)
    return redirect('/homepage')


#========================================= Route for deleting

@app.route('/poem/<int:id>/delete', methods=['GET'])
def delete_poem(id):
    if 'uid' not in session:
        return redirect('/login')

    poem = Poem.get_by_id(id)

    if poem.user_id != session['uid']:
        return redirect('/homepage')

    Poem.delete(id)
    return redirect('/homepage')