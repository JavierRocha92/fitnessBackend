from flask import Blueprint, request
from ..controllers.registerController import (
    registerVirtualUser as controllerRegisterVirtualUser,
    registerUser as controllerRegisterUser,
    deleteVirtualUser as controllerDeleteVirtualUser,
    registerMeasuresVirtualUser as controllerRegisterMeasuresVirtualUser,
)


register = Blueprint("register", __name__)


@register.route("/", methods=["POST"])
def registerUser():
    return controllerRegisterUser()


@register.route("/virtual", methods=["POST"])
def registerVirtualUser():
    return controllerRegisterVirtualUser()


@register.route("/virtual/measures", methods=["POST"])
def registerMeasuresVirtualUser():
    return controllerRegisterMeasuresVirtualUser()


@register.route("/virtual/<user_id>/<virtual_user_id>", methods=["DELETE"])
def deleteVirtualUser(user_id, virtual_user_id):
    
    return controllerDeleteVirtualUser(user_id, virtual_user_id)
