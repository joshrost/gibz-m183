import bcrypt
from hashlib import sha256
from base64 import b64encode

from app.database import db

PEPPER = b"$6$S9cvmZfrSawoXMJ4"


class User(db.Model):
    """
    User class for the database including all requred fields
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    phonenumber = db.Column(db.String(), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Integer, nullable=False)


def add_user(name, username, password, phonenumber, role=0, state=0):
    new_user = User(
        name=name,
        username=username,
        password=hash_password(password),
        phonenumber=phonenumber,
        role=role,
        state=state,
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def hash_password(password, rounds=20):
    """
    Hashes the given password with the given times or default
    """
    # Pepper password
    pepperd = str.encode(password) + PEPPER

    # trim
    trimed = b64encode(sha256(pepperd).digest())

    # hash
    return bcrypt.hashpw(trimed, bcrypt.gensalt(rounds))


def check_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    print(user)
    # return bcrypt.checkpw(password, hashed)
