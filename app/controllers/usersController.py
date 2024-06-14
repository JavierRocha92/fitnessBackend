

from flask import jsonify
from ..services.usersService import getAll as serviceGetAll
def getAll():
    return serviceGetAll()
