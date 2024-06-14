
from flask import Blueprint
from ..controllers.recipesController import getAll, setRecipes as controllerSetRecipes,getRecipeByVirtualUser as controllerGetRecipeByVirtualUser


recipes = Blueprint('recipes', __name__)

@recipes.route('/', methods=['GET'])
def get_all_users():
    return getAll()
@recipes.route('/', methods=['POST'])
def setRecipes():
    return controllerSetRecipes()
@recipes.route('/<virtual_user_id>', methods=['GET'])
def getRecipeByVirtualUser(virtual_user_id):
    return controllerGetRecipeByVirtualUser(virtual_user_id)
