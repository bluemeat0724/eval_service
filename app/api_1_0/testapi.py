from app.api_1_0 import api
from flask import request
import json
from flask import jsonify

from pyecharts.charts import Radar
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

from io import BytesIO

from app.utils.peiyuku_eval import InnovationValuation

# @api.route('/radar')
# def point_visualization():
#     schema = [{'name': '发展', 'max': 10},
#               {'name': '盈利', 'max': 10},
#               {'name': '研发', 'max': 10},
#               {'name': '人才', 'max': 10},
#               {'name': '技术储备', 'max': 10}]
#     values = [8, 9, 5, 6, 5, 7]
#     radar = Radar()
#     radar.set_colors(["#4587E7"])
#     radar.add_schema(schema)
#     radar.add('科技创新评估', data=[values], areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
#     img = BytesIO()


