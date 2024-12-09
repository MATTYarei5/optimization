from flask import jsonify, request
from models.users import User
from db import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def create_user(data):
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


def read_users():
    users = User.query.all()
    return jsonify([user.email for user in users])


def update_user(id, data):
    user = User.query.get(id)
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    db.session.commit()
    return jsonify({'message': 'User updated!'})


def delete_user(data):
    user = User.query.get(data['user_id'])
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted!'})
