from flask import jsonify, request, json
from ..services.historicalBioDataService import getAllByUserId as serviceGetAllByUserId
from ..models.Error import IssueError


def getAllByUser(id):
    results = serviceGetAllByUserId(id)
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else :
        return results
    
    
    