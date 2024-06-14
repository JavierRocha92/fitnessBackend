from flask import Flask, jsonify, json
from ..lib.serviceFunctions import getAllByParams as functionsGetAllByParams, getOneById as functionsGetOneById
from ..models.Error import IssueError

def getAllByParams(table, data, params, order = False):
    results = functionsGetAllByParams(table, data, params, order)
    
    if isinstance(results, IssueError):
        return results
    else :
        return results
def getOneById(id, table, keyword):
    results = functionsGetOneById(id, table, keyword)
    if isinstance(results, IssueError):
        return results.to_json()
    else :
        return results
    
def getVirutalUserById(virtual_user_id):
    return functionsGetOneById(virtual_user_id, 'virtual_users', 'id')
        