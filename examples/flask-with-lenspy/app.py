import sys
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
# , request, session, jsonify
sys.path.append('../../')
from lenspy.LensPy import *

app = Flask(__name__)

unauth_lp = LensPy()
auth_lp = {}

@app.route("/")
def home():
	return render_template('home.html',)

@app.route("/<string:handle>")
def profile(handle):
	print('req profile',handle)
	res = unauth_lp.get_profile_by_handle(handle)['profile']
	if res == None:
		return render_template('profile.html',found=False)
	else:
		bio = res['bio']
		print(res['id'])
		if bio:
			bio = res['bio'].replace('\n','')
		return render_template('profile.html',found=True,handle=handle,id=res['id'],bio=bio)


@app.route('/search-profile',methods=['GET'])
def get_search_profiles():
	handle = request.args.get("handle")
	res = unauth_lp.search_profiles(handle)
	profiles = []
	for p in res['search']['items']:
		bio = p['bio']
		if bio:
			bio = p['bio'].replace('\n','')
		if bio and len(bio)>200:
			bio = bio[0:200]
			bio += '...'
		profiles.append({'handle':p['handle'],'id':p['id'],'bio':bio})
	return render_template('search-profile.html',handle=handle,profiles=profiles)

@app.route('/publication/<string:publicationId>',methods=['GET'])
def get_publication(publicationId):
	print(publicationId)
	res = unauth_lp.get_publication(publicationId)['publication']
	# printpretty(res)
	if res == None:
		pub = {'found':False,'id':None,'__typename':None,'profile':{'handle':None,'id':None,'bio':None},'metadata':{'name': None,'content':None,'media': None,'attributes': None},'createdAt':None}
	else:
		pub = {
			'found': True,
			'id': res['id'],
			'__typename': res['__typename'],
			'profile': {
				'handle': res['profile']['handle'],
				'id': res['profile']['id'],
				'bio': res['profile']['bio'],
			},
			'metadata':{
				'name': res['metadata']['name'],
				'content': res['metadata']['content'],
				'media': res['metadata']['media'],
				'attributes': res['metadata']['attributes'],
			},
			'createdAt': res['createdAt']
		}
	return render_template('publication.html',found=pub['found'],id=pub['id'],__typename=pub['__typename'],profile_handle=pub['profile']['handle'],profile_id=pub['profile']['id'],profile_bio=pub['profile']['bio'],metadata_name=pub['metadata']['name'],metadata_content=pub['metadata']['content'],metadata_media=pub['metadata']['media'],metadata_attributes=pub['metadata']['attributes'],createdAt=pub['createdAt'])
	
# POST requests

@app.route('/getchallenge',methods=['POST'])
def get_challenge():
	data = json.loads(request.data)
	res = unauth_lp.challenge(data['address'])
	return jsonify({'lp_res':res})

@app.route('/setauthenticate',methods=['POST'])
def set_authenticate():
	data = json.loads(request.data)
	auth_lp[data['address']] = LensPy()
	res = auth_lp[data['address']].authenticate(data['address'],data['signature'])
	return jsonify({'lp_res':res})

@app.route('/sendbroadcast',methods=['POST'])
def send_broadcast():
	data = json.loads(request.data)
	res = auth_lp[data['address']].broadcast(data['broadcastId'],data['signature'])
	return jsonify({'lp_res':res})

@app.route('/getdefaultprofile',methods=['POST'])
def get_default_profile():
	data = json.loads(request.data)
	res = unauth_lp.default_profile(data['address'])
	return jsonify({'lp_res':res})

@app.route('/setdefaultprofile',methods=['POST'])
def set_default_profile():
	data = json.loads(request.data)
	res = auth_lp[data['address']].set_default_profile(data['profileId'])
	return jsonify({'lp_res':res})

@app.route('/post',methods=['POST'])
def post():
	data = json.loads(request.data)
	res = auth_lp[data['address']].post(data['profileId'],data['contentURI'],data['collectModule'],data['referenceModule'])
	return jsonify({'lp_res':res})

@app.route('/getallprofiles',methods=['POST'])
def get_all_profiles():
	data = json.loads(request.data)
	all_profiles = unauth_lp.address_profiles(data['address'])['profiles']['items']
	res = [{'handle':p['handle'],'profileId':p['id']} for p in all_profiles]
	return jsonify({'lp_res':res})

@app.route('/createprofile',methods=['POST'])
def create_profile():
	data = json.loads(request.data)
	res = unauth_lp.create_profile(data['handle'])
	return jsonify({'lp_res':res})

@app.route('/getpublications',methods=['POST'])
def send_get_publications():
	data = json.loads(request.data)
	res = unauth_lp.get_publications(data['profileId'],'[POST,COMMENT,MIRROR]',50)
	return jsonify({'lp_res':res})

@app.route('/getfollow',methods=['POST'])
def get_follow():
	data = json.loads(request.data)
	res = auth_lp[data['address']].follow(data['profileId'])
	return jsonify({'lp_res':res})

@app.route('/getunfollow',methods=['POST'])
def get_unfollow():
	data = json.loads(request.data)
	res = auth_lp[data['address']].unfollow(data['profileId'])
	return jsonify({'lp_res':res})

@app.route('/getfollowing',methods=['POST'])
def get_following():
	data = json.loads(request.data)
	res = unauth_lp.following(data['address'])['following']['items']
	res = list(map(lambda p: {'handle':p['profile']['handle'],'id':p['profile']['id']},res))
	return jsonify({'lp_res':res})

def printpretty(el):
	_printpretty(el, 0)

def _printpretty(el,indent):
	if isinstance(el, dict):
		for k,v in el.items():
			print('  '*indent + k+':')
			_printpretty(v,indent+1)
	elif isinstance(el, list):
		print('  '*indent + '[')
		for e in el:
			_printpretty(e,indent+1)
		print('  '*indent + ']')
	else:
		print('  '*indent + str(el))