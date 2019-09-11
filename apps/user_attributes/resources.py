from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import UserAttributes
from sqlalchemy import desc
from apps import app, db
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_user_attributes = Blueprint('user_attributes', __name__)
api = Api(bp_user_attributes)