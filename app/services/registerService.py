from flask import Flask, jsonify, request
from ..db.dbConnection import DbConnection
from ..models.Error import IssueError
import datetime
import jwt
import datetime
import uuid
import bcrypt
from ..lib.serviceFunctions import encodedPass


SECRET_PASSWORD = "uYVyuvVYUyvY67678t807T7&&9rf76_F-7T8-gf8"
"""Función para checkear si las credenciales de acceso de un usario son correctas"""


def registerUser(user_data):
    userExists = isUserExists(user_data)

    # Condicional para manejar errores que puedan venir del servicio
    if isinstance(userExists, IssueError):
        return userExists
    # Condicional para seguir la ejecución si el usuario si que existe
    if not userExists:
        query = "Insert into users VALUES(%s, %s, %s, %s, %s, %s);"
        uuid_random = str(uuid.uuid4())
        

        params = (
            uuid_random,
            user_data["first_name"],
            user_data["last_name"],
            user_data["email"],
            encodedPass(user_data['pass']),
            # user_data['pass'],
            datetime.datetime.now().strftime("%Y-%m-%d"),
        )

        results = DbConnection().insertQuery(query, params)
        return results
        # Condicional para devolver si el usuario no existe
    else:
        return IssueError(6000, "This user is already registered")


def registerVirtualUser(user_data):
   
    query = """
    INSERT INTO virtual_users (
        id, physical_user_id, name, gender, goal, daily_calories, target_weight,
        target_hip_circumference, target_waist_circumference,
        target_bmi, target_body_fat, start_date, end_date,
        activity_level, age, height
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
    uuid_random = str(uuid.uuid4())
    params = (
        uuid_random,
        user_data["physical_user_id"],
        user_data["name"],
        user_data["gender"],
        user_data["goal"],
        user_data["daily_calories"],
        user_data["target_weight"],
        user_data["target_hip_circumference"],
        user_data["target_waist_circumference"],
        user_data["target_bmi"],
        user_data["target_body_fat"],
        user_data["start_date"],
        user_data["end_date"],
        user_data["activity_level"],
        user_data["age"],
        user_data["height"]
    )

    results = DbConnection().insertQuery(query, params)
    if isinstance(results, IssueError):
        print('eeror de insercion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return results

    result_user_data = registerVirutalUserData(user_data, uuid_random)
    if isinstance(result_user_data, IssueError):
        print('errpr del virtual user!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return result_user_data
    
    print('esta es la response en el servicio!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(results)
    
    return results


def isUserExists(user):
    query = "SELECT email FROM users WHERE email = %s;"
    params = (user["email"],)
    results = DbConnection().getQuery(query, params)

    if isinstance(results, IssueError) and results.code == 2000:
        return False
    return results


def registerVirutalUserData(user_data, virtual_user_id):

    
    bio_data_id = str(uuid.uuid4())
    params_biodata = (
        bio_data_id,
        virtual_user_id,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user_data["weight"],
        user_data["bmi"],
        user_data["body_fat"],
    )

    query_biodata = """
    INSERT INTO biometric_data_history (
        id, virtual_user_id, date_time, weight, bmi, body_fat
    ) VALUES (%s, %s, %s, %s, %s, %s)
"""
    anthropometric_id = str(uuid.uuid4())
    params_athropometric = (
        anthropometric_id,
        virtual_user_id,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user_data["height"] if "height" in user_data else '177',
        user_data["weight"],
        user_data["waist_circumference"],
        user_data["hip_circumference"],
    )

    query_athropometric = """
    INSERT INTO anthropometric_measurements_history (
        id, virtual_user_id, date_time, height, weight, waist_circumference,hip_circumference
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    
"""

    result_biodata = DbConnection().insertQuery(query_biodata, params_biodata)
    if isinstance(result_biodata, IssueError):
        return result_biodata
    result_athropometric = DbConnection().insertQuery(
        query_athropometric, params_athropometric
    )
    if isinstance(result_athropometric, IssueError):
        return result_athropometric


def deleteVirtualUser(user_id):
    query = """DELETE FROM virtual_users WHERE id = %s"""
    params = (user_id,)
    results = DbConnection().deleteQuery(query, params)
    return results


        
