import pytest, json, logging
from flask import Flask, request

from apps import db
from app import cache

def call_client(request):
  client = app.test_client()
  return client

@pytest.fixture
def client(request):
    return call_client(request)