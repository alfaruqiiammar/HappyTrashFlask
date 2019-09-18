from apps import db
from flask_restful import fields


class UserAttributes(db.Model):
    """Class for storing information about user_attributes table

    Attributes:
        __tablename__: a string of table name
        user_id: an integer of foreign key from user's table, field 'id'
        point: an integer of point that user has
        total_trash: an integer of total trash that user already sell (in kg)
        onboarding_status: a boolean that indicates user's onboarding status. True if user already finish onboarding and False if user have not finish onboarding
        date_created: a datetime that indicates when the row created
        date_updated: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "user_attributes"
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    point = db.Column(db.Integer, nullable=False)
    total_trash = db.Column(db.Float, nullable=False)
    onboarding_status = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'user_id': fields.Integer,
        'point': fields.Integer,
        'total_trash': fields.Integer,
        'onboarding_status': fields.Boolean
    }

    def __init__(self, user_id, point, total_trash, onboarding_status):
        """Inits user attributes with data that user inputted

        The data already validated on the resources function

        Args:
            user_id: an integer of foreign key from user's table, field 'id'
            point: an integer of point that user has
            total_trash: an integer of total trash that user already sell (in kg)
            onboarding_status: a boolean that indicates user's onboarding status. True if user already finish onboarding and False if user have not finish onboarding
        """
        self.user_id = user_id
        self.point = point
        self.total_trash = total_trash
        self.onboarding_status = onboarding_status
