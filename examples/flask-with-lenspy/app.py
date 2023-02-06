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

@app.route('/getprofile',methods=['POST'])
def get_profile():
	data = json.loads(request.data)
	print(data)
	res = lp.address_profile_handles(data['address'])
	if (len(res)==0):
		res = false
	else:
		res = res[0]
	return jsonify({'lp_res':res})

@app.route('/getchallenge',methods=['POST'])
def get_challenge():
	data = json.loads(request.data)
	print(data)
	res = lp.challenge(data['address'])
	return jsonify({'lp_res':res})

@app.route('/setauthenticate',methods=['POST'])
def set_authenticate():
	data = json.loads(request.data)
	print(data)
	res = lp.authenticate(data['address'],data['signature'])
	return jsonify({'lp_res':res})

@app.route('/createprofile',methods=['POST'])
def create_profile():
	data = json.loads(request.data)
	print(data)
	res = lp.create_profile(data['handle'])
	return jsonify({'lp_res':res})