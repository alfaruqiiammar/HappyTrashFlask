import pytest, json, logging
from flask import Flask, request, json
from apps import app, db
from app import cache
import json

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
