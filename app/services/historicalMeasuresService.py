from flask import Flask, jsonify
from ..lib.serviceFunctions import getAllByParams, getAllByField,getAll as functionsGetAll

def getAll():
    return functionsGetAll('anthropometric_measurements_hsitory')

def getAllByUserId(id):
    data = {
        'virtual_user_id' : id
    }
    result =  getAllByParams('anthropometric_measurements_history',data, (id,), 'Date_time')

    return result

def getAllWeights():
    return getAllByField('weight', 'anthropometric_measurements_history')
    
