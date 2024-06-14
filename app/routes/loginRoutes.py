
from flask import Blueprint
from ..controllers.loginController import checkUser


login = Blueprint('login', __name__)

@login.route('/', methods=['POST'])
def get_all_users():
    token = checkUser()
    return token
    # return checkUser()
