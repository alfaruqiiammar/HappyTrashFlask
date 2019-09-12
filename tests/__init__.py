import pytest, json, logging
from flask import Flask, request, json
from apps import app, db
from app import cache
import json
from apps.users.model import Users
from passlib.hash import sha256_crypt

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def reset_database():
    """Reset database for testing purpose"""
    db.drop_all()
    db.create_all()

    user_password_encrypted = sha256_crypt.hash('user')
    admin_password_encrypted = sha256_crypt.hash('admin')

    user = Users('user', 'user@user.com', '081122112211', user_password_encrypted, False)
    admin = Users('admin', 'admin@admin.com', '0811221122112', admin_password_encrypted, True)

    db.session.add(user)
    db.session.add(admin)
    db.session.commit()
