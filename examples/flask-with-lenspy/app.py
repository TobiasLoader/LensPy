import sys
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
# , request, session, jsonify
sys.path.append('../../')
from lenspy.LensPy import *

app = Flask(__name__)

lp = LensPy()
handle = 'lens'

@app.route("/")
def home():
	return render_template(
		'home.html',
		handle=handle,
		profileId=lp.get_profile_id(handle),
	)


@app.route('/getchallenge',methods=['POST'])
def get_challenge():
	data = json.loads(request.data)
	res = lp.challenge(data['address'])
	return jsonify({'lp_res':res})

@app.route('/setauthenticate',methods=['POST'])
def set_authenticate():
	data = json.loads(request.data)
	res = lp.authenticate(data['address'],data['signature'])
	return jsonify({'lp_res':res})

@app.route('/sendbroadcast',methods=['POST'])
def send_broadcast():
	data = json.loads(request.data)
	res = lp.broadcast(data['broadcastId'],data['signature'])
	return jsonify({'lp_res':res})

@app.route('/getdefaultprofile',methods=['POST'])
def get_default_profile():
	data = json.loads(request.data)
	res = lp.default_profile(data['address'])
	return jsonify({'lp_res':res})

@app.route('/setdefaultprofile',methods=['POST'])
def set_default_profile():
	data = json.loads(request.data)
	res = lp.set_default_profile(data['profileId'])
	return jsonify({'lp_res':res})

@app.route('/getallprofiles',methods=['POST'])
def get_all_profiles():
	data = json.loads(request.data)
	all_profiles = lp.address_profiles(data['address'])['profiles']['items']
	res = [{'handle':p['handle'],'profileId':p['id']} for p in all_profiles]
	return jsonify({'lp_res':res})

@app.route('/createprofile',methods=['POST'])
def create_profile():
	data = json.loads(request.data)
	res = lp.create_profile(data['handle'])
	return jsonify({'lp_res':res})