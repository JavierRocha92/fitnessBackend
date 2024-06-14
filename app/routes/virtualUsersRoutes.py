

from flask import Blueprint
from ..controllers.virtualUsersController import getAllByUser


virtualUsers = Blueprint('virtualUsers', __name__)

@virtualUsers.route('/', methods=['GET'])
def get_all_users():
    return getAllByUser()
