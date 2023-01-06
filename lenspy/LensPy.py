from GraphQLClient import GQLClient
from queries import *
from gql import gql
from web3.auto import w3
from eth_account.messages import encode_defunct
import random

pub = "0xb8CE9ab6943e0eCED004cDe8e3bBed6568B2Fa01"
pri = "0x348ce564d427a3311b6536bbcff9390d69395b06ed6c486954e971d960fe8709"

def listtostr(l):
	s = '['
	for el in l:
		s += el + ','
	s = s[:-1] + ']'
	return s

class LensPy:
	def __init__(self):
		self.reset_client()
	
	def reset_client(self):
		self.client = GQLClient()
		self.authorised = False
	
	def login(self,wallet_public_address,wallet_private_address):
		# if you login (either with this method or manually reproducing challenge/signature/authenticate/access token steps below),
		# then you can use mutation (write) gql queries as well as standard (read only) queries
		self.reset_client()
		# create challenge request
		challenge = gql(Challenge("address:"+'"'+wallet_public_address+'"'))
		print(challenge)
		# challenge response from server
		challenge_res = self.client.execute_query(challenge)
		print(challenge_res)
		# retrieve text from challenge response
		challenge_txt = challenge_res['challenge']['text']
		# use encode_defunct to create signable message
		# (replace with encode_intended_validator/encode_structured_data sometime)
		signable_message = encode_defunct(text = challenge_txt)
		# using w3 library to sign the message
		signed_message = w3.eth.account.sign_message(signable_message,private_key = wallet_private_address)
		# authenticate gql query
		auth_query = gql(authenticate("address:"+'"'+wallet_public_address+'",'+'signature:'+'"'+signed_message.signature.hex()+'"'))
		# response from server for authentication request
		auth_res = self.client .execute_query(auth_query)
		# retrieve access token from authentication response
		access_token = auth_res['authenticate']['accessToken']
		# provide client with correct access token
		self.client = GQLClient(token = access_token)
		self.authorised = True
	
	def getProfileId(self,handle):
		# get profile from handle name gql request
		get_profile_req = gql(SearchProfiles('query: "{}",type: PROFILE,limit: 1'.format(handle)))
		# execute query and save response
		profile_res = self.client.execute_query(get_profile_req)
		# return id of profile response
		return profile_res['search']['items'][0]['id']
	
	def createProfile(self,handle, profilePictureUri = "null", followNFTURI = "null", followModule = "null"):
		# TODO: allow null params
		#  – shouldn't have double quotes for null but should for any other value.
		
		# create profile gql request
		create_profile_req = createProfile('handle:"{}",profilePictureUri: null,followNFTURI: null,followModule: null'.format(handle,profilePictureUri,followNFTURI,followModule))
		# execute the query to create a new profile
		self.client.execute_query(create_profile_req)
		# not strictly necessary – return the profile id of profile just created
		# this serves also as a check that the above profile creation was successful 
		return self.getProfileId(handle)
	
	def follow(self,profileId):
		# create follow gql query 
		follow_profile_req = gql(createFollowTypedData('profile: "{}"'.format(profileId)))
		self.client.execute_query(follow_query)

lp = LensPy()
lp.login(pub,pri)
# lp.getProfileId('tobblit')
# l.login('','','')

# sortcriteria = ['TOP_COMMENTED','TOP_COLLECTED','TOP_MIRRORED','LATEST','CURATED_PROFILES']
# publicationtypes = ['POST', 'COMMENT', 'MIRROR']