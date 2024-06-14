
from flask import Blueprint
from ..controllers.historicalMeasuresController import getAllByUser


historicalMeasures = Blueprint('historicalMeasures', __name__)

@historicalMeasures.route('/<id>', methods=['GET'])
def get_all_users(id):
    return getAllByUser(id)
