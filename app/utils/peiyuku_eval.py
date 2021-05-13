import os
import pandas as pd
import json


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

        # 纠错参数
        self.paraerror = 0
        self.checked = 0
        self.paraerrorrecord = []

        # 指标编号
        self.questionindexes = range(11)

        # 读取问卷答案
        self.content = json.loads(data) if type(data) != dict else data
        # 问卷参数，数据类型检查
        self.companyname = self.paramcheck(self.content.get('name'), str)  # 1
        self.industry = self.paramcheck(self.content.get('industry'), str)  # 2
        self.business = self.paramcheck(self.content.get('business'), str)
        self.coreproduct = self.paramcheck(self.content.get('coreproduct'), str)
        self.researchinvest = self.paramcheck(self.content.get('researchinvest'), [float])
        self.income = self.paramcheck(self.content.get('income'), [float])
        self.profit = self.paramcheck(self.content.get('profit'), [float])
        self.researcher = self.paramcheck(self.content.get('researcher'), [int])
        self.employees = self.paramcheck(self.content.get('employees'), [int])
        self.invention_patentumber = self.paramcheck(self.content.get('invention_patentumber'), int)
        self.patentnumber = self.paramcheck(self.content.get('patentnumber'), int)
        self.mainpatents = self.paramcheck(self.content.get('mainpatents'), int)
        self.patentincome = self.paramcheck(self.content.get('patentincome'), float)
        self.mainclients = self.paramcheck(self.content.get('mainclients'), [str])
        self.mainclients_sales_ratio = self.paramcheck(self.content.get('mainclients_sales_ratio'), float)
        self.techlevel = self.paramcheck(self.content.get('techlevel'), int)
        self.techawardlevel = self.paramcheck(self.content.get('techawardlevel'), int)
        self.mainprojectstype = self.paramcheck(self.content.get('mainprojects'), [str])
        self.maintechdescription = self.paramcheck(self.content.get('maintechdescription'), str)

        # 问卷参数变量
        self.questionbase = []
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

        #         self.totalincome = sum(self.income)
        #         #6研发投入金额累计
        #         self.totalresearch = sum(self.researchinvest)
        #         self.questionbase.append(self.totalresearch)
        # 5,6研发投入比例,6研发投入金额累计
        self.getresearchratio()
        # 7 R&D人员占比
        self.researcherratio = round(self.researcher[0] / self.employees[0], 4)
        self.questionbase.append(self.researcherratio)
        self.questiondescription.append('R&D人员占比')

        # 8发明专利比重
        self.inventionratio = round(self.invention_patentumber / self.patentnumber, 4)
        self.questionbase.append(self.inventionratio)
        self.questiondescription.append('发明专利比重')
        # 9  主营业务收入的发明专利 self.mainpatents
        self.questionbase.append(self.mainpatents)
        self.questiondescription.append('主营业务收入的发明专利')
        # 10 技术水平self.techlevel
        self.questionbase.append(self.techlevel)
        self.questiondescription.append('技术水平')
        # 11 大客户营收占比 self.mainclients_sales_ratio
        self.questionbase.append(self.mainclients_sales_ratio)
        self.questiondescription.append('大客户销售额占比')

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

    # 1近一年营业收入
    def getrecentincome(self):
        if self.income is not None and len(self.income) == 4:
            # 19 近一年营业收入
            self.checked += 1
            self.recentincome = self.income[0]
            self.questionbase.append(self.recentincome)
            self.questiondescription.append('近一年营业收入')
        else:
            self.recentincome = 0
            self.paraerror += 1
            self.paraerrorrecord.append('income para problem')

    # 2近三年收入复合增长率
    def getincreaserate(self):
        # 20
        try:
            self.increaserate = round((self.income[0] / self.income[2]) ** (1 / 3) - 1, 4)
            self.checked += 1
            self.questionbase.append(self.increaserate)
            self.questiondescription.append('近三年收入复合增长率')
        except:
            self.increaserate = 0
            self.paraerror += 1
            self.paraerrorrecord.append('收入复合增长率')  # 第二题

    # 3 最近两年净利润累计
    def getrecentprofit(self):
        try:
            self.recentprofit = self.profit[0] + self.profit[1]
            self.checked += 1
            self.questionbase.append(self.recentprofit)
            self.questiondescription.append('最近两年净利润累计')
        except:
            self.recentprofit = 0
            self.paraerror += 1
            self.paraerrorrecord.append('净利润累计')  # 第三题

    # 4最近两年净利润是否均为正
    def getprofitstatus(self):
        if self.profit[0] > 0 and self.profit[1] > 0:
            self.profitstatus = 1
        elif self.profit[0] <= 0 and self.profit[1] <= 0:
            self.profitstatus = 0
        else:
            self.profitstatus = 0.6
        self.questionbase.append(self.profitstatus)
        self.questiondescription.append('最近两年净利润是否均为正')

    # 56研发投入比例
    def getresearchratio(self):
        self.totalresearch = sum(self.researchinvest)
        self.totalincome = sum(self.income)
        self.researchratio = round(self.totalresearch / self.totalincome, 4)

        self.questionbase.append(self.researchratio)
        self.questiondescription.append('研发投入比例')
        self.questionbase.append(self.totalresearch)
        self.questiondescription.append('研发投入金额累计')

    def getpoints(self, data, ranges, base, reverse=False):
        points = 5
        for i in [r * base for r in ranges]:
            if reverse:
                if data > i:
                    points -= 1
            else:
                if data < i:
                    points -= 1
        return points

    def questionvalue(self, index, data):
        ranges = list(self.basedf[[5, 4, 3, 2, 1]].loc[index])
        base = self.basedf.loc[index]['基准']
        power = self.basedf.loc[index]['倍数']
        if index in [10]:
            points = self.getpoints(data, ranges, base, reverse=True)
        else:
            points = self.getpoints(data, ranges, base)
        #         print(self.basedf.loc[index]['三级指标'])
        #         print(' 基准：',base,'\n','范围：',ranges,'\n','倍数：',power)
        #         print(' basepoints:',points,'\n','points:',points*power)
        #         print('inputdata',data)
        return points * power

    def getsheetanswers(self):
        self.sheetanswer = []
        for i in self.questionindexes:
            self.sheetanswer.append(self.questionvalue(i, self.questionbase[i]))
        self.sheetanswerdict={i:self.sheetanswer[i] for i in range(len(self.sheetanswer))}
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



