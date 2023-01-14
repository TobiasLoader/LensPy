from lenspy.GraphQLClient import GQLClient
from lenspy.parse_graphql import parse_callable_api_from_graphql
from web3.auto import w3
from eth_account.messages import encode_defunct

class LensPy:
	def __init__(self):
		self.reset_client()
		self.api = parse_callable_api_from_graphql('lenspy/lens-api.documents.graphql')
		self.methods_info = {
			'reset_client()':'resets the GQLClient',
			'raw_api_call(graphql_query,req_params_str)':'direct api call of query (note could be a mutation) with req_params_str as graphql string of requests',
			'available_raw_api_calls()':'prints a list of all graphql queries accessible from the raw_api_call() method (see lens-api.documents.graphql file for specification)',
			'available_methods(desc_bool)':'prints a list of all methods on the LensPy object (with descriptions if optional parameter \'desc_bool\' is True',
			'login(wallet_public_address,wallet_private_address)':'login to lens with key pair',
			'get_profile_id(handle)':'get lens protocol profile id for a given handle name',
			'authenticate(address,signature)':'authenticate profile (used in login process)',
			'add_reaction(profileId,reaction,publicationId)':'adds a reaction to given publication',
			'broadcast(broadcastId,signature)':'relay transaction if not using a dispatcher',
			'challenge(address)':'request a challenge for authentification of \'address\' from Lens',
			'create_profile(handle)':'creates a new lens protocol profile with given handle',
			'follow(profileId)':'follows the profile with a given profileId (must be authenticated)',
			'followers(profileId,limit)':'returns list of followers of profileId',
			'following(address,limit)':'returns list of those following address',
			'is_followed_by_me(profileId)':'returns a Bool if profileId is followed by the user',
			'is_following(followerProfileId,followedHandle)':'returns a Bool if followerProfileId is following followedHandle',
			'ping()':'pings the lens protocol server to check for healthy connection',
			'profile_feed(profileId, limit)':'returns #limit items of feed for profileId',
			'remove_reaction(profileId,reaction,publicationId)':'remove the reaction from publication',
			'report_publication(publicationId,reason,subreason,additionalComments)':'report - see reasons',
			'search_profiles(handle,limit)':'searches profiles for a given handle (up to limit)',
			'search_publications(handle,limit)':'searches prublications for a given query',
			'unfollow(profileId)':'unfollows the profile with a given profileId'
		}
	
	def reset_client(self):
		self.client = GQLClient()
		self.authorised = False
	
	def available_raw_api_calls(self):
		print('\nAVAILABLE RAW API CALLS')
		print('---')
		for api_call in self.api.keys():
			print(api_call)
		print('---\n')
	
	def available_methods(self,desc_bool=False):
		print('\nAVAILABLE METHODS')
		print('---')
		for method,desc in self.methods_info.items():
			print(method)
			if desc_bool:
				print('- '+desc+'\n')
		print('---\n')
	
	# can use this method to call lesser used graphql queries
	# supply query name and parameters as a string yourself
	
	def raw_api_call(self,graphql_query,req_params_str=None):
		req = self.api[graphql_query](req_params_str)
		return self.client.execute_query(req)
	
	def raw_graphql_query(self,graphql):
		return self.client.execute_query(graphql)
	
	## custom methods for commonly used tasks

	def login(self,wallet_public_address,wallet_private_address):
		# if you login (either with this method or manually reproducing challenge/signature/authenticate/access token steps below),
		# then you can use mutation (write) gql queries as well as standard (read only) queries
		self.reset_client()
		# create challenge request
		req_str = "address:"+'"'+wallet_public_address+'"'
		challenge_req = self.api['Challenge'](req_str)
		# challenge response from server
		challenge_res = self.client.execute_query(challenge_req)
		# retrieve text from challenge response
		challenge_txt = challenge_res['challenge']['text']
		# use encode_defunct to create signable message
		# (replace with encode_intended_validator/encode_structured_data sometime)
		signable_message = encode_defunct(text = challenge_txt)
		# using w3 library to sign the message
		signed_message = w3.eth.account.sign_message(signable_message,private_key = wallet_private_address)
		# authenticate gql query
		req_str = 'address: "{}",signature:"{}"'.format(wallet_public_address,signed_message.signature.hex())
		auth_query = self.api['authenticate'](req_str)
		# response from server for authentication request
		auth_res = self.client.execute_query(auth_query)
		# retrieve access token from authentication response
		access_token = auth_res['authenticate']['accessToken']
		# provide client with correct access token
		self.client = GQLClient(token = access_token)
		self.authorised = True
	
	def get_profile_id(self,handle):
		# get profile from handle name gql request
		req_str = 'query: "{}",type: PROFILE,limit: 1'.format(handle)
		get_profile_req = self.api['SearchProfiles'](req_str)
		# execute query and save response
		profile_res = self.client.execute_query(get_profile_req)
		# return id of profile response
		if len(profile_res['search']['items']):
			return profile_res['search']['items'][0]['id']
		else:
			return -1
	
	## directly from api
	
	def authenticate(self, address, signature):
		req_str = 'address: "{}",signature:"{}"'.format(address,signature)
		auth_query = self.api['authenticate'](req_str)
		return self.client.execute_query(auth_query)
	
	def add_reaction(self,profileId,reaction,publicationId):
		req_str = 'profileId:"{}",reaction: "{}",publicationId: "{}"'.format(profileId,reaction,publicationId)
		add_reaction_req = self.api['addReaction'](req_str)
		return self.client.execute_query(add_reaction_req)
	
	def broadcast(self,broadcastId,signature):
		req_str = 'broadcastId:"{}",signature: "{}"'.format(broadcastId,signature)
		broadcast_req = self.api['Broadcast'](req_str)
		return self.client.execute_query(broadcast_req)
	
	def challenge(self, address):
		req_str = 'address:"{}"'.format(address)
		challenge_req = self.api['Challenge'](req_str)
		return self.client.execute_query(challenge_req)
	
	def create_profile(self, handle, profilePictureUri = "null", followNFTURI = "null", followModule = "null"):
		# TODO: allow null params
		#  – shouldn't have double quotes for null but should for any other value.
		
		# create profile gql request
		req_str = 'handle:"{}",profilePictureUri: null,followNFTURI: null,followModule: null'.format(handle,profilePictureUri,followNFTURI,followModule)
		create_profile_req = self.api['CreateProfile'](req_str)
		# execute the query to create a new profile & return
		return self.client.execute_query(create_profile_req)
	
	def default_profile(self,address):
		req_str = 'ethereumAddress:"{}"'.format(address)
		default_profile_req = self.api['defaultProfile'](req_str)
		return self.client.execute_query(default_profile_req)
	
	def follow(self,profileId):
		# not working as is -- need to implement follow module + NFTs
		req_str = 'follow:[{profile: "'+profileId+'",followModule: null}]'
		follow_profile_req = self.api['createFollowTypedData'](req_str)
		return self.client.execute_query(follow_profile_req)
	
	def followers(self,profileId,limit=10):
		req_str = 'profileId:"{}", limit:"{}"'.format(profileId,limit)
		followers_req = self.api['followers'](req_str)
		return self.client.execute_query(followers_req)
	
	def following(self,address,limit=10):
		req_str = 'address:"{}", limit:"{}"'.format(address,limit)
		following_req = self.api['following'](req_str)
		return self.client.execute_query(following_req)
	
	def is_followed_by_me(self,profileId):
		req_str = 'profileId:"{}"'.format(profileId)
		is_followed_by_me_req = self.api['profile'](req_str)
		return self.client.execute_query(is_followed_by_me_req)['profile']['isFollowedByMe']
		
	def is_following(self,followerProfileId,followedHandle):
		req_str = '''query Profile {
		profile(request: { profileId: "'''+followerProfileId+'''" }) {
			isFollowing(who:"'''+followedHandle+'''")
		}}'''
		return self.raw_graphql_query(req_str)
	
	def ping(self):
		ping_req = self.api['ping']()
		return self.client.execute_query(ping_req)	
	
	def profile_feed(self, profileId, limit=50):
		# issue with query field 'isGated' on type 'Post'.
		req_str = 'profileId:"{}", limit:{}'.format(profileId,limit)
		profile_feed_req = self.api['ProfileFeed'](req_str)
		print(profile_feed_req)
		return self.client.execute_query(profile_feed_req)
		
	def remove_reaction(self,profileId,reaction,publicationId):
		req_str = 'profileId:"{}",reaction: "{}",publicationId: "{}"'.format(profileId,reaction,publicationId)
		remove_reaction_req = self.api['removeReaction'](req_str)
		return self.client.execute_query(remove_reaction_req)
	
	def report_publication(self,publicationId,reason,subreason,additionalComments=''):
		# reason: SENSITIVE, ILLEGAL, FRAUD, SPAM
		# subreason:
		#  -- SENSITIVE : NSFW, OFFENSIVE
		#  -- ILLEGAL   : ANIMAL_ABUSE, HUMAN_ABUSE, VIOLENCE, THREAT_INDIVIDUAL, DIRECT_THREAT
		#  -- FRAUD     : SCAM, IMPERSONATION
		#  -- SPAM      : MISLEADING, MISUSE_HASHTAGS, UNRELATED, REPETITIVE, FAKE_ENGAGEMENT, MANIPULATION_ALGO, SOMETHING_ELSE
		
		if reason == 'SENSITVE':
			reasonParam = 'sensitiveReason'
		if reason == 'ILLEGAL':
			reasonParam = 'illegalReason'
		if reason == 'FRAUD':
			reasonParam = 'fraudReason'
		if reason == 'SPAM':
			reasonParam = 'spamReason'
		req_str = 'publicationId: "{}", reason: { {}: { reason: {}, subreason: {} } }, additionalComments:"{}",'.format(publicationId,reasonParam,reason,subreason,additionalComments)
		report_publication_req = self.api['reportPublication'](req_str)
		return self.client.execute_query(report_publication_req)
		
	def search_profiles(self,handle,limit=10):
		req_str = 'query: "{}",type: PROFILE,limit: {}'.format(handle,limit)
		search_profiles_req = self.api['SearchProfiles'](req_str)
		return self.client.execute_query(search_profiles_req)
	
	def search_publications(self,query,limit=10):
		req_str = 'query: "{}",type: PUBLICATION,limit: {}'.format(query,limit)
		search_publications_req = self.api['SearchPublications'](req_str)
		return self.client.execute_query(search_publications_req)
	
	def unfollow(self, profileId):
		req_str = 'profile: "{}"'.format(profileId)
		unfollow_profile_req = self.api['createUnfollowTypedData'](req_str)
		return self.client.execute_query(unfollow_profile_req)

# sortcriteria = ['TOP_COMMENTED','TOP_COLLECTED','TOP_MIRRORED','LATEST','CURATED_PROFILES']
# publicationtypes = ['POST', 'COMMENT', 'MIRROR']