# 问卷接口(测试)

## 传输问卷答案   
http://10.20.21.35:8889/peiyukusheet   
返回问卷编号
```json
{
    "code": "2fcd4968d8c44622b5ac12f226ff7ed3"
}
```
post data   
格式 json  
样例数据顺序同问卷   
16 生产技术水平 techlevel 从高到低，5，4，3，2，1（无）   
17 所获奖项  techawardlevel 5，4，3，2（无）  
    
样例数据
```json
{
    "companyname": "百事可乐",
    "industry": "生物医药",
    "business": "alsdjsdlaflasjf;asjd",
    "coreproduct": "快乐水",
    "researchinvest": [
        "1500",
        2500,
        1000,
        500
    ],
    "income": [
        "18000",
        7000,
        6000,
        5000
    ],
    "profit": [
        "4500",
        -600,
        500
    ],
    "researcher": [
        20,
        15,
        10
    ],
    "employees": [
        80,
        60,
        10
    ],
    "invention_patentumber": 30,
    "patentnumber": 35.6,
    "mainpatents": 28,
    "patentincome": 23.5,
    "mainclients": [
        "a",
        "b",
        "c"
    ],
    "mainclients_sales_ratio": 0.31,
    "techlevel": 5,
    "techawardlevel": 5,
    "mainprojects": [
        "asdd",
        "dasf"
    ],
    "maintechdescription": "XXXXXX"
}
```

##打开报告页面
参数 code
http://10.20.21.35:8889/reportview/code

example
http://10.20.21.35:8889/reportview/393b1f5f14dc43c4a47c670dd7ae6fa0
##下载pdf报告
http://10.20.21.35:8889/reportfile/code   
example
http://10.20.21.35:8889/reportfile/393b1f5f14dc43c4a47c670dd7ae6fa0