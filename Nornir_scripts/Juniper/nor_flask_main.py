#!/usr/bin/python3
from nornir import InitNornir
from nornir.plugins.tasks.files import write_file
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import re
import json
from flask import (Flask,request,send_file,jsonify,abort,Response,url_for,render_template)
from flask import make_response
from waitress import serve
from nor_rack_detail_template import check_tag

nr = InitNornir(
    inventory={
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        }
    }
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('01-index.html')

@app.route('/fillup_form', methods=['GET','POST'])
def fillup_form():
    return render_template('01-vlan_tag_form.html')

@app.route('/output', methods=['GET','POST'])
def output():
    RACK_NUM = request.args.get('rack_num')
    RU_NUM = request.args.get('ru_num')

    VLAN_TAG,status_code=check_tag(RACK_NUM, RU_NUM)

    return render_template('01-output.html', VLAN_TAG=VLAN_TAG)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('01-404.html'), 404


if __name__ == '__main__':
    #app.run(debug=True,host="127.0.0.1",port=9092)
    serve(app, host='127.0.0.1', port=9092)
