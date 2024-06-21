# login_app/models.py
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Dummy user (replace with your actual user authentication logic)
users = {
    'john': User('john', 'password'),
    'jane': User('jane', 'password'),
}
