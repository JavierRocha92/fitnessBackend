
from flask import jsonify
from ..services.commentsService import getAll as serviceGetAll
def getAll():
    return serviceGetAll()
