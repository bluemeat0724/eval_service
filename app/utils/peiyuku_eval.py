import os
import pandas as pd
import json
from datetime import datetime


class InnovationValuation:
    def __init__(self, data):
        '''
        参数说明:
        companyname:企业名称
        industry:所属行业
        business:主营简介
        coreproduct:核心产品
        researchinvest:4年研发经费list
        income:4年主营业务收入list
        profit:3年利润list
        researcher:3年研发人员数list
        employees:3年员工总数list
        invention_patentumber：发明专利数
        patentnumber：专利数
        mainpatents：核心专利数
        patentincome：专利收入
        mainclients：大客户list
        mainclients_sales_ratio:大客户销售额占比
        techlevel:技术水平
        techawardlevel:获奖情况int
        mainprojectstype:重大项目情况

        questionbase:问卷参数集合
        questiondescription：问卷参数描述
        questionindexes：问卷index

        recentincome:近一年营业收入
        increaserate:近三年收入复合增长率
        recentprofit:近两年净利润累计
        profitstatus:近两年利润状态
        researchratio：研发投入占比
        totalresearch：研发投入
        researcherratio：研发人员占比
        inventionratio：发明专利占比
        mainpatents：核心专利数
        techlevel：技术水平
        mainclients_sales_ratio:大客户销售额占比

        answersheet():结果df


        '''

        # 读取模型
        self.baseexcel = os.path.join(os.path.dirname(__file__), '科技创新评估.xlsx')
        self.basedf = pd.read_excel(self.baseexcel, sheet_name='points')
        #相关参数
        self.currentyear=datetime.today().year
        self.defaulrecentyear = 2020
        self.yearsfour=[str(i) for i in [self.defaulrecentyear,self.defaulrecentyear-1,self.defaulrecentyear-2,self.defaulrecentyear-3]]
        self.yearspace = 3

        # 纠错参数
        self.paraerror = 0
        self.checked = 0
        self.paraerrorrecord = []

        # 指标编号
        self.questionindexes = range(11)

        # 读取问卷答案
        self.content = json.loads(data) if type(data) != dict else data
        # 问卷参数，数据类型检查
        self.companyname = self.paramcheck(self.content.get('companyname'), str)  # 1
        self.industry = self.paramcheck(self.content.get('industry'), str)  # 2
        self.strategicindustry()
        self.business = self.paramcheck(self.content.get('business'), str)
        self.coreproduct = self.paramcheck(self.content.get('coreproduct'), str)
        self.researchinvest = self.paramcheck(self.content.get('researchinvest'), {'type':float})
        self.income = self.paramcheck(self.content.get('income'), {'type':float})
        self.profit = self.paramcheck(self.content.get('profit'), {'type':float})
        self.researcher = self.paramcheck(self.content.get('researcher'), {'type':int})
        self.employees = self.paramcheck(self.content.get('employees'), {'type':int})
        self.invention_patentumber = self.paramcheck(self.content.get('invention_patentumber'), int)
        self.patentnumber = self.paramcheck(self.content.get('patentnumber'), int)
        self.mainpatents = self.paramcheck(self.content.get('mainpatents'), int)
        self.patentincome = self.paramcheck(self.content.get('patentincome'), float)
        self.mainclients = self.paramcheck(self.content.get('mainclients'), [str])
        self.mainclients_sales_ratio = self.paramcheck(self.content.get('mainclients_sales_ratio'), float)
        self.techlevel = self.paramcheck(self.content.get('techlevel'), str)
        self.techawardlevel = self.paramcheck(self.content.get('techawardlevel'), [str])
        self.mainprojectstype = self.paramcheck(self.content.get('mainprojects'), [str])
        self.maintechdescription = self.paramcheck(self.content.get('maintechdescription'), str)

        # 问卷参数变量
        self.questionbase = {}
        self.questiondescription = []
        # 生成问卷参数
        # 1近一年营业收入
        self.getrecentincome()
        # 2近三年收入复合增长率
        self.getincreaserate()
        # 3最近两年净利润累计
        self.getrecentprofit()
        # 4最近两年净利润是否均为正
        self.getprofitstatus()
        # 5,6研发投入比例,6研发投入金额累计
        self.getresearchratio()
        # 7 当年R&D人员占比
        self.getresearcherratio()
        # 8发明专利比重
        self.inventionratio = round(self.invention_patentumber / self.patentnumber, 4) if self.patentnumber!=0 else 0
        self.questionbase[7]=self.inventionratio
        self.questiondescription.append('发明专利比重')
        # 9  主营业务收入的发明专利 self.mainpatents
        self.questionbase[8]=self.mainpatents
        self.questiondescription.append('主营业务收入的发明专利')
        # 10 技术水平self.techlevel
        self.gettechlevelpoints()
        # self.questionbase[9]=self.techlevel
        # self.questiondescription.append('技术水平')
        # 11 大客户营收占比 self.mainclients_sales_ratio
        self.questionbase[10]=self.mainclients_sales_ratio/100
        self.questiondescription.append('大客户销售额占比')

        #是否软件类企业
        self.softwareindustry = 0

        # 获取答案

    #         self.getsheetanswers()

    def paramcheck(self, p, paratype):
        # 检查参数类型，对list类参数item进行转换
        if type(paratype) == list:
            itemtype = paratype[0]
            try:
                lp = [itemtype(i) for i in p]
                return lp
            except:
                self.paraerror += 1
                self.paraerrorrecord.append(('listtype', p))
                return p
        elif type(paratype) == dict:
            try:
                p={i:paratype['type'](v) for i,v in p.items()}
                return p
            except:
                self.paraerror += 1
                self.paraerrorrecord.append(('dicttype', p))
                return p
        else:
            if not isinstance(p, paratype):
                try:
                    p = paratype(p)
                    self.checked += 1
                    return p
                except:
                    self.paraerror += 1
                    self.paraerrorrecord.append(('type', p))
                return None
            else:
                self.checked += 1
                return p
    #是否战略新兴产业
    def strategicindustry(self):
        strategicindustries=['新一代信息技术产业','高端装备制造','新材料','新能源','节能环保','生物医药','符合科创板定位的其他领域']
        self.indtypeone=self.industry.split('-')[0]
        print(self.indtypeone)
        if self.indtypeone in strategicindustries:
            self.strategic_ind=1
        else:
            self.strategic_ind=0

    # 1近一年营业收入
    def getrecentincome(self):
        if self.income is not None:
            # 19 近一年营业收入
            self.checked += 1
            try:
                self.recentincome = self.income[self.yearsfour[0]]
            except:
                self.recentincome=0
            self.questionbase[0]=self.recentincome
            self.questiondescription.append('近一年营业收入')
        else:
            self.recentincome = 0
            self.paraerror += 1
            self.paraerrorrecord.append('income para problem')

    # 2近三年收入复合增长率
    def getincreaserate(self):
        # 20
        try:
            self.recentincome=self.income[self.yearsfour[0]]
            self.earlyincome=self.income[self.yearsfour[2]]
            self.increaserate = round((self.recentincome / self.earlyincome) ** (1 / 3) - 1, 3) if self.earlyincome!=0 else 0
            self.checked += 1
            self.questionbase[1]=self.increaserate
            self.questiondescription.append('近三年收入复合增长率')
        except:
            self.increaserate = 0
            self.paraerror += 1
            self.paraerrorrecord.append('收入复合增长率')  # 第二题

    # 3 最近两年净利润累计
    def getrecentprofit(self):
        try:
            self.recentprofit = round(self.profit[self.yearsfour[0]] + self.profit[self.yearsfour[1]],4)
            self.checked += 1
            self.questionbase[2]=self.recentprofit
            self.questiondescription.append('最近两年净利润累计')
        except:
            self.recentprofit = 0
            self.paraerror += 1
            self.paraerrorrecord.append('净利润累计')  # 第三题

    # 4最近两年净利润是否均为正
    def getprofitstatus(self):
        try:
            if self.profit[self.yearsfour[0]] > 0 and self.profit[self.yearsfour[1]] > 0:
                self.profitstatus = 5
            elif self.profit[self.yearsfour[0]] <= 0 and self.profit[self.yearsfour[1]] <= 0:
                self.profitstatus = 0
            else:
                self.profitstatus = 3
        except:
            self.profitstatus = 0
        self.questionbase[3]=self.profitstatus
        self.questiondescription.append('最近两年净利润是否均为正')

    # 56 3年研发投入比例
    def getresearchratio(self):
        self.totalresearch = sum([float(self.researchinvest[i]) for i in self.yearsfour[:3]])
        self.totalincome = sum([float(self.income[i]) for i in self.yearsfour[:3]])
        self.researchratio = round(self.totalresearch / self.totalincome, 4) if self.totalincome!=0 else 0

        self.questionbase[4]=self.researchratio
        self.questiondescription.append('研发投入比例')
        self.questionbase[5]=self.totalresearch
        self.questiondescription.append('研发投入金额累计')

    # 7 当年研发人员占比
    def getresearcherratio(self):
        try:
            self.researcherratio= round(self.researcher[self.yearsfour[0]] / self.employees[self.yearsfour[0]], 4) if self.employees[self.yearsfour[0]] != 0 else 0
        except:
            self.researcherratio=0
        self.questionbase[6] = self.researcherratio
        self.questiondescription.append('R&D人员占比')

    # 10技术水平
    def gettechlevelpoints(self):
        points={'国际领先':5,'国际先进':4,'国内领先':3,'国内先进':2,'无':1}
        self.techlevelpoints=points[self.techlevel]
        self.questionbase[9]=self.techlevelpoints
        self.questiondescription.append('技术水平')

    #计算等级
    def getpoints(self, data, ranges, base, reverse=False):
        points = 5
        try:
            for i in [r * base for r in ranges]:
                if reverse:
                    if data > i:
                        points -= 1
                else:
                    if data < i:
                        points -= 1
        except:
            self.paraerror += 1
            self.paraerrorrecord.append('getpointserror')
            points = 0
        return points

    #计算分值
    def questionvalue(self, index, data):
        ranges = list(self.basedf[[5, 4, 3, 2, 1]].loc[index])
        base = self.basedf.loc[index]['基准']
        power = self.basedf.loc[index]['倍数']
        if index in [10]:
            points = self.getpoints(data, ranges, base, reverse=True)
        else:
            points = self.getpoints(data, ranges, base)
        return points * power

    def getsheetanswers(self):
        self.sheetanswer = []
        for i in self.questionindexes:
            self.sheetanswer.append(self.questionvalue(i, self.questionbase[i]))
        self.sheetanswerdict={i:self.sheetanswer[i] for i in range(len(self.sheetanswer))}
        self.total_score=sum(self.sheetanswerdict.values())
        self.operational_score=sum(list(self.sheetanswerdict.values())[0:4])
        self.techinvest_score=sum(list(self.sheetanswerdict.values())[4:7])
        self.research_score=sum(list(self.sheetanswerdict.values())[7:])

        return self.sheetanswerdict

    def answersheet(self):
        self.getsheetanswers()
        answerdf = pd.DataFrame(index=self.questionindexes, data={'answer': self.sheetanswer,
                                                                'basedata': [self.questionbase[i] for i in
                                                                             self.questionindexes],
                                                                'description': [self.questiondescription[i] for i in
                                                                                self.questionindexes]})
        return self.basedf.join(answerdf, how='right')

    def report(self):  # 状态
        print('error:', self.paraerror)
        print('checked:', self.checked)
        print('paraerrorrecord:', self.paraerrorrecord)

    #四项指标（同时符合）
    # 1研发投入
    def getresearchinveststatus(self):
        # self.getresearchratio()
        self.researchinveststatus=[]
        softwares = []
        ##最近3年累计研发投入占最近3年累计营业收入比例5%以上
        if self.researchratio>0.05:
            self.researchinveststatus.append(1)
        else:
            self.researchinveststatus.append(0)
        ##最近3年研发投入金额累计在6000万元以上
        if self.totalresearch>6000:
            self.researchinveststatus.append(1)
        else:
            self.researchinveststatus.append(0)
        ##软件企业最近3年累计研发投入占最近3年累计营业收入比例10%以上
        softwareindustrysub=['人工智能软件开发','互联网与云计算、大数据服务支撑软件开发','新兴软件']
        try:
            if self.industry.split('-')[1] in softwareindustrysub and self.industry.split('-')[0]=='新一代信息技术产业' and self.researchratio>0.1:
                self.researchinveststatus.append(1)
                self.softwareindustry=1
            else:
                self.researchinveststatus.append(0)
        except:
            self.researchinveststatus.append(0)
        if 1 in self.researchinveststatus:
            self.researchinvestrequirement=1
        else:
            self.researchinvestrequirement=0


    #2研发人员
    def getresearchstaffstatus(self):
        # self.getresearcherratio()
        if self.researcherratio>0.1:
            self.researchstaffrequirement = 1
        else:
            self.researchstaffrequirement = 0

    #3主营发明专利
    def getmainpatentstatus(self):
        if self.mainpatents>5:
            self.mainpatentrequirement = 1
        elif self.softwareindustry==1:
            self.mainpatentrequirement = 1
        else:
            self.mainpatentrequirement = 0

    #4营业收入
    def getincomestatus(self):
        # self.getincreaserate()
        self.incomestatus = []
        #最近3年营业收入复合增长率达到20%
        if self.increaserate>0.2:
            self.incomestatus.append(1)
        else:
            self.incomestatus.append(0)
        #最近一年营业收入金额达到3亿元
        # self.getrecentincome()
        if self.recentincome>30000:
            self.incomestatus.append(1)
        else:
            self.incomestatus.append(0)
        if 1 in self.incomestatus:
            self.incomerequriement=1
        else:
            self.incomerequriement = 0

    #4项指标综合
    def getfourrequirementsstatus(self):
        #获取指标数据
        self.getresearchratio()
        self.getresearcherratio()
        self.getincreaserate()
        self.getrecentincome()
        #指标计算1研发2人员3专利4收入
        self.getresearchinveststatus()
        self.getresearchstaffstatus()
        self.getmainpatentstatus()
        self.getincomestatus()
        fourrequirements=[]
        fourrequirements.append(self.researchinvestrequirement)
        fourrequirements.append(self.researchstaffrequirement)
        fourrequirements.append(self.mainpatentrequirement)
        fourrequirements.append(self.incomerequriement)
        if 0 in fourrequirements:
            self.fourqequirementstatus=0
        else:
            self.fourqequirementstatus = 1

    #5个情形
    #1核心技术
    def getcoretechstatus(self):
        if self.techlevel!='无':
            self.techlevelstatus=1
        else:
            self.techlevelstatus=0

    #2获奖情况
    def getawardstatus(self):
        if len(self.techawardlevel)>0:
            self.techawardstatus = 1
        else:
            self.techawardstatus = 0

    #3重大专项
    def getmainprojectstatus(self):
        if len(self.mainprojectstype)>0:
            self.projectstatus = 1
        else:
            self.projectstatus = 0

    #4重点产品
    def getcoreproductstatus(self):
        if len(self.maintechdescription)>0:
            self.coreproductstatus = 1
        else:
            self.coreproductstatus = 0

    #5核心专利数
    def getcorepatentstatus(self):
        if self.mainpatents>50:
            self.corepatentstatus = 1
        else:
            self.corepatentstatus = 0

    def getfiverequirementsstatus(self):
        self.getcoretechstatus()
        self.getawardstatus()
        self.getmainprojectstatus()
        self.getcoreproductstatus()
        self.getcorepatentstatus()

















