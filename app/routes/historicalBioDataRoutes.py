
from flask import Blueprint
from ..controllers.historicalBioDataController import getAllByUser as controllerGetAllByUser


historicalBioData = Blueprint('historicalBioData', __name__)

@historicalBioData.route('/<id>', methods=['GET'])
def getAllbyUser(id):
    return controllerGetAllByUser(id)
    # return 'estas en la ruta'

# @historicalBioData.route('/', methods=['GET'])
# def getAllbyUser():
#     return 'estas en la ruta'

