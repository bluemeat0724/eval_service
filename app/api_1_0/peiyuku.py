from app.api_1_0 import api
from flask import request
import json
from flask import jsonify
import os

from app.utils.peiyuku_eval import InnovationValuation

@api.route('/peiyukusheet',methods=['POST'])
def peiyukusheet():
    content = json.loads(request.data)
    iv=InnovationValuation(content)
    iv.getsheetanswers()

    return jsonify({'answers':','.join([str(i) for i in iv.sheetanswer])})


