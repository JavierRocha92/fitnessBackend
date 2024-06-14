SECRET_PASSWORD = "uYVyuvVYUyvY67678t807T7&&9rf76_F-7T8-gf8"
import datetime
import jwt
import json

from ..services.usersService import getAllByParams as userGetAllByParams
from ..services.virtualUsersService import getAllByParams as virtualUserGetAllByParams
from ..services.historicalMeasuresService import getAllByUserId as measurementsGetAllByUserId
from ..services.historicalBioDataService import getAllByUserId as bioDataGetAllByUserId

def getAccessToken(user):
    EXPIRATION_TIME_IN_MINUTES = 1

    expiration = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=EXPIRATION_TIME_IN_MINUTES
    )
    user["expiration"] = expiration.timestamp()

    user_token = jwt.encode(user, SECRET_PASSWORD, algorithm="HS256")
    return user_token

def getResponse(results, user):
    user_token = getAccessToken(json.loads(results)[0])
    
    user_data = userGetAllByParams('users', {'email' : user['email']},(user['email'],))
    
    user_data_json = json.loads(user_data)
    
    virtual_user_data = virtualUserGetAllByParams('virtual_users', {'ID' : user_data_json['ID']}, (user_data_json['ID'],))
    
    virtual_user_data_full_filled = addDataToVirtualUsers(virtual_user_data)
    
    response = {
        'success' : True,
        'token' : user_token,
        'user' : user_data_json,
        'virtual_users' : virtual_user_data_full_filled
    }
    
def addDataToVirtualUsers(virtual_user_data):
    virtual_user_data_json = json.loads(virtual_user_data)
    for virtual_user in virtual_user_data_json:
            
        id_on_search = virtual_user['ID']
        historical_measurements = measurementsGetAllByUserId(id_on_search)
        
        virtual_user['historical_measurements'] = json.loads(historical_measurements)
        historical_bio_data = bioDataGetAllByUserId(id_on_search)
            
        virtual_user['historical_bio_data'] = json.loads(historical_bio_data)
    return virtual_user_data_json