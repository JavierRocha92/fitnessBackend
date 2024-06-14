from flask import jsonify, request
import json
from ..services.registerService import registerVirtualUser as serviceRegisterVirtualUser, registerUser as serviceRegisterUser, deleteVirtualUser as serviceDeleteVirtualUser, registerVirutalUserData as serviceRegisterVirtualUserData
from ..lib.controllerFunctions import getAccessToken
from ..models.Error import IssueError
from ..services.usersService import getAllByParams as userGetAllByParams, getUserById as userGetUserById
from ..services.virtualUsersService import getAllByParams as virtualUserGetAllByParams, getVirutalUserById as virtualGetVirutalUserById
from ..services.historicalMeasuresService import getAllByUserId as measurementsGetAllByUserId, getAllWeights
from ..services.historicalBioDataService import getAllByUserId as bioDataGetAllByUserId
from ..lib.controllerFunctions import getAccessToken

def registerUser():
    user = request.json
    results = serviceRegisterUser(user)
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else :
        user_token = getAccessToken(user)
        return json.dumps(getResponseData(user, user_token, False))
    
def registerVirtualUser():
    user = request.json
    results = serviceRegisterVirtualUser(user)
    
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else :
        user_id = user['physical_user_id']
        response = getResponseData(None, None, user_id)
        return json.dumps(response)
    
def registerMeasuresVirtualUser():
    user = request.json
    results = serviceRegisterVirtualUserData(user, user['id'])
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else :
        virtual_user = request.json
        results = getOneVirtualUser(virtual_user)
        
        if(isinstance(results, IssueError)):
            return json.dumps(results.to_json())
        return json.dumps({'success' : True, 'virtual_user' : results[0]})
    
    
def deleteVirtualUser(user_id, virtual_user_id):
    results = serviceDeleteVirtualUser(virtual_user_id)
    if isinstance(results, IssueError):
        return json.dumps(results.to_json())
    else:
        response = getResponseData(None, None, user_id)
        return json.dumps(response)
    
def getOneVirtualUser(virtual_user):
    virtual_user_data = virtualGetVirutalUserById(virtual_user['id'] if 'id' in virtual_user else 'ID')
    if (isinstance(virtual_user_data, IssueError)):
        return virtual_user_data
    virtual_user_data_fullfilled = addDataToVirtualUsers(json.loads(virtual_user_data))
    return virtual_user_data_fullfilled 

   
def getResponseData(user, user_token, user_id):
    
    if user_id :
        user_data_json = json.loads(userGetUserById(user_id))
    if user :
        user_data = userGetAllByParams('users', {'email' : user['email']},(user['email'],))
        user_data_json = json.loads(user_data)
        
    all_weight = json.loads(getAllWeights())
    
    virtual_user_data = virtualUserGetAllByParams('virtual_users', {'physical_user_id' : user_data_json['ID']}, (user_data_json['ID'],))
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(virtual_user_data)
    print(type(virtual_user_data))
    if isinstance(virtual_user_data, IssueError):
        if virtual_user_data.code == 2000:
            virtual_user_data = '[]'
    else :
        virtual_user_data = json.loads(virtual_user_data)
    
    virtual_user_data_full_filled = []
    
    if isinstance(virtual_user_data, list) and len(virtual_user_data):
        virtual_user_data_full_filled = addDataToVirtualUsers(virtual_user_data)
        
    response = {
        'success' : True,
        'token' : user_token,
        'user' : user_data_json,
        'virtual_users' : virtual_user_data_full_filled,
        'avg_data' : all_weight
    }
    
    print('esta es ña respuesta final al insertar un usuario')
    print(response)
    
    return response
    
    
def addDataToVirtualUsers(virtual_user_data):
  
    for virtual_user in virtual_user_data:
            
        id_on_search = virtual_user['ID']
        historical_measurements = measurementsGetAllByUserId(id_on_search)
        if(isinstance(historical_measurements, IssueError)):
            historical_measurements = '[]'
        
        virtual_user['historical_measurements'] = json.loads(historical_measurements)
        
        historical_bio_data = bioDataGetAllByUserId(id_on_search)
        if(isinstance(historical_bio_data, IssueError)):
            historical_bio_data = '[]'
            
        virtual_user['historical_bio_data'] = json.loads(historical_bio_data)
    return virtual_user_data


