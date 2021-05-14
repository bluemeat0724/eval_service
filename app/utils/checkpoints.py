content={'name':'xxxx公司',
'industry':'生物医药',
'business':'alsdjsdlaflasjf;asjd',
'coreproduct':'快乐水',
'researchinvest':['1500',2500,1000,500],
 'income':['18000',7000,6000,5000],
 'profit':['4500',-600,500],
 'researcher':[20,15,10],
 'employees':[80,60,10],
 'invention_patentumber':30,
 'patentnumber':35.6,
 'mainpatents':28,
        'patentincome':23.5,
 'mainclients':['a','b','c'],
 'mainclients_sales_ratio':0.31,
 'techlevel':5,
 'techawardlevel':5,
 'mainprojects':['asdd','dasf'],
}
from app.utils.peiyuku_eval import InnovationValuation

iv=InnovationValuation(content)

print('问卷参数:',iv.questionbase)
iv.getsheetanswers()
print('评分:',iv.sheetanswer)