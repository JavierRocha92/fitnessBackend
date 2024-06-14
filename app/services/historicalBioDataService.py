from flask import Flask, jsonify, request
from ..lib.serviceFunctions import getAllByParams, getAll as functionsGetAll

def getAllByUserId(id):
    data = {
        'virtual_user_id' : id
    }
    return getAllByParams('biometric_data_history',data, (id,), 'Date_time')

