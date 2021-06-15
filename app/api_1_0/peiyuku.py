from app.api_1_0 import api
from flask import request, current_app, send_from_directory, render_template, make_response
import json
from flask import jsonify
import pdfkit
import uuid
import os

from app.utils.peiyuku_eval import InnovationValuation
import base64

from app.models.peiyuku import Answers
from app.models import db



#上传问卷答案，返回问卷编号
@api.route('/peiyukusheet',methods=['POST'])
def peiyukusheet():
    answerdata = request.data.decode()
    with db.auto_commit():
        code = uuid.uuid4().hex
        try:
            name=json.loads(answerdata).get('companyname')
        except:
            name=None
        answer = Answers(answer=answerdata,code=code,name=name)
        db.session.add(answer)
    return jsonify({'code':code})

#查看报告页面
@api.route('/reportview/<code>',methods=['GET','POST'])
def posttest(code):
    #加载答案
    answercode = code
    answer = Answers.query.filter_by(code=answercode).first()
    answerdict=json.loads(answer.answer)
    #计算评分
    iv = InnovationValuation(answerdict)
    iv.getsheetanswers()
    #四项指标
    iv.getfourrequirementsstatus()
    #生成报告

    #符合条件
    successpath = os.path.join(os.path.dirname(__file__), 'success.png')
    # with open(r"app\reportsfolder\success.png", "rb") as f:  # 转为二进制格式
    with open(successpath, "rb") as f:  # 转为二进制格式
        successimage = base64.b64encode(f.read()).decode()
    #存疑
    warningpath = os.path.join(os.path.dirname(__file__), 'warning.png')
    # with open(r"app\reportsfolder\warning.png", "rb") as f:  # 转为二进制格式
    with open(warningpath, "rb") as f:  # 转为二进制格式
        warningimage = base64.b64encode(f.read()).decode()

    return render_template('temp_pdfpage.html',
                           companyname=answerdict.get('companyname'),
                           industry=answerdict.get('industry'),
                           strategicind=iv.strategic_ind,
                           successimage=successimage,
                           warningimage=warningimage,
                           business=answerdict.get('business'),
                           coreproduct=answerdict.get('coreproduct'),
                           total_score=iv.total_score,
                           operational_score = iv.operational_score,
                           techinvest_score = iv.techinvest_score,
                           research_score = iv.research_score,
                           questionbase = iv.questionbase,
                           points = iv.sheetanswerdict,
                           techlevel = iv.techlevel,
                           iv=iv,
                           answercode=answercode
                           )


#下载报告文件
@api.route('/reportfile/<code>')
def getreportfile(code):
    # 加载答案
    answercode = code
    answer = Answers.query.filter_by(code=answercode).first()
    answerdict = json.loads(answer.answer)

    # 计算评分
    iv = InnovationValuation(answerdict)
    iv.getsheetanswers()
    # 四项指标
    iv.getfourrequirementsstatus()

    # 符合条件
    successpath = os.path.join(os.path.dirname(__file__), 'success.png')
    # with open(r"app\reportsfolder\success.png", "rb") as f:  # 转为二进制格式
    with open(successpath, "rb") as f:  # 转为二进制格式
        successimage = base64.b64encode(f.read()).decode()
    # 存疑
    warningpath = os.path.join(os.path.dirname(__file__), 'warning.png')
    # with open(r"app\reportsfolder\warning.png", "rb") as f:  # 转为二进制格式
    with open(warningpath, "rb") as f:  # 转为二进制格式
        warningimage = base64.b64encode(f.read()).decode()



    rendered = render_template('temp_pdfreport.html',
                               companyname=answerdict.get('companyname'),
                               industry=answerdict.get('industry'),
                               strategicind=iv.strategic_ind,
                               successimage=successimage,
                               warningimage=warningimage,
                               business=answerdict.get('business'),
                               coreproduct=answerdict.get('coreproduct'),
                               total_score=iv.total_score,
                               operational_score=iv.operational_score,
                               techinvest_score=iv.techinvest_score,
                               research_score=iv.research_score,
                               questionbase=iv.questionbase,
                               points=iv.sheetanswerdict,
                               techlevel=iv.techlevel,
                               iv=iv
                               )
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdfreport = pdfkit.from_string(rendered,False,options=options)
    #返回下载报告
    response = make_response(pdfreport)
    response.headers['Content-Type'] = 'application/pdf'
    outputfilename='Innovation_eval.pdf'
    response.headers['Content-Disposition'] = 'attachment;filename={}'.format(outputfilename)
    return response


#查看上传的文件
@api.route('/report/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['REPORTS_FOLDER'],
                               filename
                               # as_attachment=True
                               )


