
from app.routes.usersRoutes import users as users_bp 
from app.routes.loginRoutes import login as login_bp 
from app.routes.registerRoutes import register as register_bp 
from app.routes.virtualUsersRoutes import virtualUsers as virtualUsers_bp 
from app.routes.commentsRoutes import comments as comments_bp 
from app.routes.historicalBioDataRoutes import historicalBioData as historicalBioData_bp 
from app.routes.historicalMeasuresRoutes import historicalMeasures as historicalMeasures_bp 
from app.routes.recipesRoutes import recipes as recipes_bp 
from flask import Flask
from app.lib.middlewareFunctions import jwt_middleware
from flask_cors import CORS
# Crear una instancia de la aplicación
app = Flask(__name__)

CORS(app, expose_headers='Authorization', resources={r"/*": {"origins": "http://localhost:4200"}})

#Llamada al middleware para veririfcar la veracidad de el token de acceso

jwt_middleware(app)


# Registra el blueprint
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(virtualUsers_bp, url_prefix='/virtualUsers')
app.register_blueprint(comments_bp, url_prefix='/comments')
app.register_blueprint(recipes_bp, url_prefix='/recipes')
app.register_blueprint(historicalBioData_bp, url_prefix='/historicalBioData')
app.register_blueprint(historicalMeasures_bp, url_prefix='/historicalMeasures')


# Definir una ruta para la API
@app.route('/', methods=['GET'])
def index():
    return '¡Bienvenido a mi aplicación Flask!'
# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True)





    
    
