from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Dummy user data (replace with your actual user authentication logic)
users = {'john': 'password', 'jane': 'password'}


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('success', username=username))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/success/<username>')
def success(username):
    return f'Welcome, {username}!'


if __name__ == '__main__':
    app.run(debug=True)
