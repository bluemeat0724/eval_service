import jinja2
import pdfkit

from pyecharts.charts import Radar
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot



templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "pdftest_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
#
# schema=[{'name': '发展', 'max': 10},
#  {'name': '盈利', 'max': 10},
#  {'name': '研发', 'max': 10},
#  {'name': '人才', 'max': 10},
#  {'name': '技术储备', 'max': 10}]
# values=[8, 2, 9, 10, 5]
# titles = ['发展', '盈利', '研发', '人才', '技术储备']
#
# radar=Radar()
# radar.set_colors(["#4587E7"])
# radar.add_schema(schema)
# radar.add('科技创新评估',data=[values],areastyle_opts=opts.AreaStyleOpts(opacity=0.8))
# imagename = 'image.png'
# make_snapshot(snapshot, radar.render(), imagename)
#
#
#
# outputText = template.render(name='波波',pngimage=imagename)
# with open('testreport.html','w',encoding='utf8') as f:
#     f.write(outputText)
options={'enable-local-file-access':True,
         'load-error-handling':'skip',
         'load-media-error-handling':'skip',
         'javascript-delay':'5000','no-stop-slow-scripts': None,}
#
# # config=pdfkit.configuration(wkhtmltopdf=r'E:\SynologyDrive\python\mypython\tool\wkhtmltopdf\bin\wkhtmltopdf.exe')
#
# # pdfkit.from_string(outputText,'testreport.pdf',
# #                    # configuration=config ,
# #                    options=options)

pdfkit.from_file(r'E:\projects\eval_service\app\reportsfolder\ec89540f8833407aa2746a142b82f5a3.html','testreport.pdf',
                 options=options
                 )