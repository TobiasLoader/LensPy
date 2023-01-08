from GraphQLClient import GQLClient
from parse_graphql import parse_callable_api_from_graphql
from web3.auto import w3
from eth_account.messages import encode_defunct

class LensPy:
	def __init__(self):
		self.reset_client()
		self.api = parse_callable_api_from_graphql('lenspy/lens-api.documents.graphql')
	
	def reset_client(self):
		self.client = GQLClient()
		self.authorised = False
	
	def available_api_calls(self):
		print('\n---')
		for api_call in self.api.keys():
			print(api_call)
		print('---\n')
	
	## custom methods for commonly used tasks
	
	def login(self,wallet_public_address,wallet_private_address):
		# if you login (either with this method or manually reproducing challenge/signature/authenticate/access token steps below),
		# then you can use mutation (write) gql queries as well as standard (read only) queries
		self.reset_client()
		# create challenge request
		challenge = self.api['Challenge']("address:"+'"'+wallet_public_address+'"')
		# challenge response from server
		challenge_res = self.client.execute_query(challenge)
		# retrieve text from challenge response
		challenge_txt = challenge_res['challenge']['text']
		# use encode_defunct to create signable message
		# (replace with encode_intended_validator/encode_structured_data sometime)
		signable_message = encode_defunct(text = challenge_txt)
		# using w3 library to sign the message
		signed_message = w3.eth.account.sign_message(signable_message,private_key = wallet_private_address)
		# authenticate gql query
		auth_query = self.api['authenticate']("address:"+'"'+wallet_public_address+'",'+'signature:'+'"'+signed_message.signature.hex()+'"')
		# response from server for authentication request
		auth_res = self.client.execute_query(auth_query)
		# retrieve access token from authentication response
		access_token = auth_res['authenticate']['accessToken']
		# provide client with correct access token
		self.client = GQLClient(token = access_token)
		self.authorised = True
	
	def getProfileId(self,handle):
		# get profile from handle name gql request
		get_profile_req = self.api['SearchProfiles']('query: "{}",type: PROFILE,limit: 1'.format(handle))
		# execute query and save response
		profile_res = self.client.execute_query(get_profile_req)
		# return id of profile response
		if len(profile_res['search']['items']):
			return profile_res['search']['items'][0]['id']
		else:
			return -1
	
	def createProfile(self, handle, profilePictureUri = "null", followNFTURI = "null", followModule = "null"):
		# TODO: allow null params
		#  – shouldn't have double quotes for null but should for any other value.
		
		# create profile gql request
		create_profile_req = self.api['CreateProfile']('handle:"{}",profilePictureUri: null,followNFTURI: null,followModule: null'.format(handle,profilePictureUri,followNFTURI,followModule))
		# execute the query to create a new profile & return
		return self.client.execute_query(create_profile_req)
	
	## directly from api
		
	def addReaction(self,profileId,reaction,publicationId):
		add_reaction_req = self.api['addReaction']('profileId:"{}",reaction: "{}",publicationId: "{}"'.format(profileId,reaction,publicationId))
		self.client.execute_query(add_reaction_req)
	
	def follow(self,profileId):
		follow_profile_req = self.api['createFollowTypedData']('profile: "{}"'.format(profileId))
		return self.client.execute_query(follow_query)
	
	def ping(self):
		ping_req = self.api['ping']()
		return self.client.execute_query(ping_req)

# sortcriteria = ['TOP_COMMENTED','TOP_COLLECTED','TOP_MIRRORED','LATEST','CURATED_PROFILES']
# publicationtypes = ['POST', 'COMMENT', 'MIRROR']