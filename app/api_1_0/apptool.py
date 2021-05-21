from app.api_1_0 import api
from flask import jsonify

@api.app_errorhandler(404)
def api_not_found(e):
    return jsonify({'msg':'api not found','error_code':404})

@api.app_errorhandler(500)
def apierror(e):
    return jsonify({'msg':'unknown error','error_code':500})