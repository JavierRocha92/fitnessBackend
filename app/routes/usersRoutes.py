

from flask import Blueprint
from ..controllers.usersController import getAll


users = Blueprint('user', __name__)

@users.route('/', methods=['GET'])
def get_all_users():
    return getAll()
