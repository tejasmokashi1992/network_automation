#!/usr/bin/python3
import re
import json
import yaml
from flask import (Flask,request,send_file,jsonify,abort,Response,url_for,render_template,render_template_string)
from flask import make_response
from waitress import serve
from nor_rack_detail_template import check_tag
from nor_command_send import command_send
from logging import FileHandler, WARNING, INFO, DEBUG
from datetime import datetime as dt
import logging

app = Flask(__name__)

#file_handler = FileHandler('errorlog.txt')
#file_handler.setLevel(INFO)
#app.logger.info(dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f"))
#app.logger.addHandler(file_handler)
logging.basicConfig(filename="errorlog.txt", format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s', level='WARNING')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vlantagform', methods=['GET','POST'])
def vlantag_form():
    return render_template('vlan_tag_form.html')

@app.route('/outputvlantag', methods=['GET','POST'])
def output_vlantag():
    RACK_NUM = request.args.get('rack_num')
    RU_NUM = request.args.get('ru_num')

    VLAN_TAG,status_code=check_tag(RACK_NUM, RU_NUM)

    return render_template('output_vlantag.html', VLAN_TAG=VLAN_TAG)

@app.route('/commandsform', methods=['GET','POST'])
def commands_form():
    with open(r'inventory/hosts_list.yaml') as file:
        hosts_list = yaml.full_load(file)
    return render_template('commands.html', hosts_list=hosts_list)

@app.route('/commandsout', methods=['GET','POST'])
def commands_out():
    COMMAND = request.form.get('command')
    DEVICE_NAME = request.form.get('device_name')
    output=command_send(COMMAND, DEVICE_NAME)
    return render_template('commands_out.html', output=output)
    #return render_template_string(output)
    #return redirect(url_for("internal_error"))
    #abort(400, 'wrong command syntax or unauthorised use of command')

@app.route('/checkrandom', methods=['GET','POST'])
def check_random():
    return "hello, This page is left for future use";
    #junos = nr.filter(F(platform="junos"))
    #junos = nr.filter(F(name="TOR_1"))
    #r = nr.run(task=napalm_get, getters=["facts"])
    #os = junos.run(task=audit, num_workers=20)
    #return render_template('check_random.html', example=get_facts_result)
    #return to_json(r)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=9092)
    #serve(app, host='127.0.0.1', port=9092)
