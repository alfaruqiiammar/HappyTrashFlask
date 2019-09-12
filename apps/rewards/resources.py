from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Rewards
from sqlalchemy import desc
from apps import app, db
from flask_jwt_extended import jwt_required, get_jwt_claims
from passlib.hash import sha256_crypt

bp_rewards = Blueprint('rewards', __name__)
api = Api(bp_rewards)