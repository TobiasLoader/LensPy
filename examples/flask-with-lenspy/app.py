import sys
from flask import Flask, render_template
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