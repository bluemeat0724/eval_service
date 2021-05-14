import jinja2
import pdfkit

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "pdftest_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(name='波波')
with open('testreport.html','w',encoding='utf8') as f:
    f.write(outputText)

options={'enable-local-file-access':True,'load-error-handling':'skip','load-media-error-handling':'skip'}
config=pdfkit.configuration(wkhtmltopdf=r'E:\SynologyDrive\python\mypython\tool\wkhtmltopdf\bin\wkhtmltopdf.exe')

pdfkit.from_string(outputText,'testreport.pdf',configuration=config ,options=options)