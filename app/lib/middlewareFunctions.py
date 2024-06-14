from flask import Flask, request, jsonify
import jwt
from ..models.Error import IssueError
SECRET_PASSWORD = 'uYVyuvVYUyvY67678t807T7&&9rf76_F-7T8-gf8'

public_routes = ['/login/', '/register/', '/register/virtual', '/recipes/']

def jwt_middleware(app):
    
    #Decorador para ejecutar autimaticamente este funcion cuando se reciben peticiones http
    @app.before_request
    def check_token():
        
        # print('headers')
        # print(request.headers)
        

        if starts_with_any(request.path , public_routes) : return 
        # Obtener el token JWT de la solicitud
        
        # if request.path in public_routes :
        #     return 
        
        token = request.headers.get('Authorization')
        

        if not token:
            # print('no hayy token')
            return jsonify(IssueError(3000, 'Forbidden pass without a token auth').to_json()), 401

        try:
            # Decodificar el token utilizando la clave secreta
            decoded_token = jwt.decode(token, SECRET_PASSWORD, algorithms=['HS256'])
            # Puedes hacer más validaciones aquí, si es necesario
            # print('este es el token decoded')
            # print(decoded_token)

        except jwt.ExpiredSignatureError:
            # print('expired token')
            return jsonify(IssueError(4000, 'Expired token auth').to_json()), 401
        except jwt.InvalidTokenError:
            # print('invalida token')
            return jsonify(IssueError(5000, 'Invalid token').to_json()), 401

    return app

def starts_with_any(route, public_routes):
    for public_route in public_routes:
        if route.startswith(public_route):
            return True
    return False
