from float_in_poetry import app, bcrypt
from flask import render_template, redirect, request, session
from float_in_poetry.models.users_model import User

# ================================================Login Form Submission Route

@app.route('/')
def first_page():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if 'uid' in session:  
        return redirect('/homepage')  

    if not User.validate_login(request.form): 
        return redirect('/')

    user = User.get_users_username(request.form['username'])
    if user:
        session['uid'] = user.id
        return redirect('/homepage')
    
    return redirect('/homepage') 

# ===========================================Register Form Submission Route

@app.route('/register', methods=['POST'])
def register():
    if not User.confirm(request.form):
        return redirect('/')

    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        'name': request.form['name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': hashed_password
    }
    session['uid'] = User.create(user_data)

    return redirect('/homepage')

# # ========================================Fetch a profile to view

# @app.route('/profile/<int:user_id>')
# def user_profile(user_id):
#     if 'uid' not in session:
#         return redirect('/login')

#     user = User.get_user_with_poems(user_id)
#     if not user:
#         return redirect('/homepage')

#     return render_template('profile_page.html', user=user, user_id=user_id)


# ===========================================Logout Route

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
