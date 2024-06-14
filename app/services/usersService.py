from flask import Flask, jsonify, json
from ..db.dbConnection import DbConnection
from ..lib.serviceFunctions import getAll as functionsGetAll, getAllByParams as functionsGetAllByParams, getOneById as functionsGetOneById
from ..models.Error import IssueError
def getAll():
    results = functionsGetAll('users')
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else :
        return results
def getAllByParams(table, data, params, order = False):
    results = functionsGetAllByParams(table, data, params, order)
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else :
        results = json.loads(results)[0]
        return json.dumps(results)
def getUserById(id : str):
    results = functionsGetOneById(id, 'users', 'id')
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else :
        results = json.loads(results)[0]
        return json.dumps(results)
    
    