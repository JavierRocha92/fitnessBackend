

from flask import jsonify
import json
from ..services.virtualUsersService import getAllByParams as serviceGetAllByUserId
def getAllByUser():
    return json.dumps(serviceGetAllByUserId(id))
