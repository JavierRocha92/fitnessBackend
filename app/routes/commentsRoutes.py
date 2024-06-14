
from flask import Blueprint
from ..controllers.commentsController import getAll


comments = Blueprint('comments', __name__)

@comments.route('/', methods=['GET'])
def get_all_users():
    return getAll()
