import hashlib
from User import User

class UserManager:
    def __init__(self, users=None):
        self.users = users if users else []

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        if any(u.username == username for u in self.users):
            return None  # user tồn tại
        new_user = User(username, self.hash_password(password))
        self.users.append(new_user)
        return new_user

    def login(self, username, password):
        pw_hash = self.hash_password(password)
        for u in self.users:
            if u.username == username and u.password_hash == pw_hash:
                return u
        return None