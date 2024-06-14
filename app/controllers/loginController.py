from flask import  request
import json
from ..services.loginService import  checkUser as serviceCheckUser
from ..models.Error import IssueError
# from ..lib.controllerFunctions import getResponse
from ..services.usersService import getAllByParams as userGetAllByParams
from ..services.virtualUsersService import getAllByParams as virtualUserGetAllByParams
from ..services.historicalMeasuresService import getAllWeights, getAllByUserId as measurementsGetAllByUserid
from ..services.historicalBioDataService import getAllByUserId as bioDataGetAllByUserid
from ..lib.controllerFunctions import getAccessToken
from ..services.usersService import getUserById
def checkUser():
    user = request.json
    results = serviceCheckUser(user)
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else :
        user_token = getAccessToken(json.loads(results)[0])
        response = getResponse(user, user_token)
        return json.dumps(response)
    
    
def addDataToVirtualUsers(virtual_user_data):
    for virtual_user in virtual_user_data:
        
        
        id_on_search = virtual_user['ID']
        historical_measurements = measurementsGetAllByUserid(id_on_search)
        if(isinstance(historical_measurements, IssueError)):
            historical_measurements = '[]'
        
        virtual_user['historical_measurements'] = json.loads(historical_measurements)
        historical_bio_data = bioDataGetAllByUserid(id_on_search)
        if(isinstance(historical_bio_data, IssueError)):
            historical_bio_data = '[]'
            
        virtual_user['historical_bio_data'] = json.loads(historical_bio_data)
    return virtual_user_data

def getResponse(user, user_token, id = False):
    
    if id :
        user_data_json = json.loads(getUserById(id))
    if user :
        user_data = userGetAllByParams('users', {'email' : user['email']},(user['email'],))
        user_data_json = json.loads(user_data)

    virtual_user_data = virtualUserGetAllByParams('virtual_users', {'Physical_user_id' : user_data_json['ID']}, (user_data_json['ID'],))
    if(isinstance(virtual_user_data, IssueError)):
        if virtual_user_data.to_json()['code'] == 2000:
            virtual_user_data = '[]'
            
    if(virtual_user_data):
        virtual_user_data = json.loads(virtual_user_data)
    
    virtual_user_data_full_filled = []
    
    all_weight = json.loads(getAllWeights())
    
    
    if isinstance(virtual_user_data, list) and len(virtual_user_data):
        virtual_user_data_full_filled = addDataToVirtualUsers(virtual_user_data)
        if (isinstance(virtual_user_data_full_filled, IssueError)):
            return virtual_user_data_full_filled
        
    response = {
        'success' : True,
        'token' : user_token,
        'user' : user_data_json,
        'virtual_users' : virtual_user_data_full_filled,
        'avg_data'  : all_weight
    }
    
    return response
