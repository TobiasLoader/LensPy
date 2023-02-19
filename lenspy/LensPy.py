from lenspy.GraphQLClient import GQLClient
from lenspy.parse_graphql import parse_callable_api_from_graphql
from lenspy.helpers import prettify_api_query_str, null_param, fix_abi_encode
from web3.auto import w3
import eth_account.messages
import json
import eth_utils
from eth_abi import encode

## PROFILE
# sortCriteria = ['CREATED_ON','MOST_FOLLOWERS','LATEST_CREATED','MOST_POSTS','MOST_COMMENTS','MOST_MIRRORS','MOST_PUBLICATION','MOST_COLLECTS']

## PUBLICATION
# sortCriteria = ['TOP_COMMENTED','TOP_COLLECTED','TOP_MIRRORED','LATEST','CURATED_PROFILES']
# types = ['POST', 'COMMENT', 'MIRROR']

class LensPy:
	def __init__(self,url="https://api-mumbai.lens.dev"):
		self.network_url = url
		self.reset_client()
		self.api = parse_callable_api_from_graphql('lenspy/lens-api.documents.graphql')
		self.methods_info = {
			'reset_client()':'resets the GQLClient',
			'----- raw calls -----':'',
			'execute_raw_api_call(query_name,req_params_str)':'direct api call of query_name (from lens-api.documents.graphql) with req_params_str as string of requests',
			'execute_raw_graphql_query(graphql)':'takes as input an entire graphql query/mutation as a string – write your own query – only for those who understand graphql queries & lens protocol docs',
			'get_graphql_query_string(query_name)':'returns prettified graphql query string for a given query (including all necessary graphql `fragments`). Can take as input any from the list LensPy.available_raw_api_calls()',
			'----- available calls -----':'',
			'available_raw_api_calls()':'prints a list of all graphql query names accessible from the raw_api_call() method (see lens-api.documents.graphql file for specification)',
			'available_methods(desc_bool)':'prints a list of all methods on the LensPy object (with descriptions if optional parameter \'desc_bool\' is True',
			'----- custom methods -----':'',
			'get_profile_id(handle)':'get lens protocol profile id for a given handle name',
			'login(wallet_public_address,wallet_private_address)':'login to lens with key pair',
			'my_profiles(limit)':'fetches all data on profiles owned by public address used to login',
			'my_profile_handles(limit)':'fetches handles of profiles owned by public address used to login',
			'----- api calls -----':'',
			'authenticate(address,signature)':'authenticate profile (used in login process)',
			'add_reaction(profileId,reaction,publicationId)':'adds a reaction to given publication',
			'broadcast(broadcastId,signature)':'relay transaction if not using a dispatcher',
			'challenge(address)':'request a challenge for authentification of \'address\' from Lens',
			'comment(profileId,publicationId,contentURI,collectModule,referenceModule)':'comment on a specific publication (can specify collect and reference modules)',
			'create_profile(handle)':'creates a new lens protocol profile with given handle',
			'default_profile(address)':'get an Ethereum address\'s default Lens profile (same address can have multiple profiles)',
			'delete_profile(profileId)':'deletes the Lens profile with profileId',
			'explore_profiles(sortCriteria)':'explore profiles by sort criteria',
			'explore_publications(sortCriteria,publicationTypes,limit)':'explore publications by sort criteria given their type (post,mirror,comment)',
			'follow(profileId,followModule)':'returns typed data to allow you to follow a profile with a given profileId (must be authenticated)',
			'follow_broadcast(private_key,profileId,followModule)':'queries for then broadcasts follow typed data (so that you are actually following)',
			'followers(profileId,limit)':'returns list of followers of profileId',
			'following(address,limit)':'returns list of those following address',
			'get_publication(publicationId)':'get a specific publication',
			'get_publications(profileId,publicationTypes,limit)':'get publications of a specific type from a profile',
			'is_followed_by_me(profileId)':'returns a Bool if profileId is followed by the user',
			'is_following(followerProfileId,followedHandle)':'returns a Bool if followerProfileId is following followedHandle',
			'mirror(profileId,publicationId,referenceModule)':'mirror a specific publication (can specify reference module)',
			'ping()':'pings the lens protocol server to check for healthy connection',
			'profile_feed(profileId, limit)':'returns #limit items of feed for profileId',
			'recommended_profiles()':'returns a list of recommended profiles',
			'remove_reaction(profileId,reaction,publicationId)':'remove the reaction from publication',
			'report_publication(publicationId,reason,subreason,additionalComments)':'report - see reasons',
			'search_profiles(handle,limit)':'searches profiles for a given handle (up to limit)',
			'search_publications(handle,limit)':'searches prublications for a given query',
			'unfollow(profileId)':'unfollows the profile with a given profileId'
		}
	
	def reset_client(self):
		self.client = GQLClient(self.network_url)
		self.authorised = False
		self.pub = None
	
	def available_raw_api_calls(self):
		print('\nAVAILABLE RAW API CALLS')
		print('----------')
		for api_call in self.api.keys():
			print(api_call)
		print('----------\n')
	
	def available_methods(self,desc_bool=False):
		print('\nAVAILABLE METHODS')
		print('----------')
		for method,desc in self.methods_info.items():
			print(method)
			if desc_bool:
				print('- '+desc+'\n')
		print('----------\n')
	
	# can use this method to call lesser used graphql queries
	# supply query name and parameters as a string yourself
	
	def execute_raw_api_call(self,query_name,req_params_str=None):
		req = self.api[query_name](req_params_str)
		return self.client.execute_query(req)
	
	def execute_raw_graphql_query(self,graphql):
		return self.client.execute_query(graphql)
	
	def get_graphql_query_string(self,query_name):
		return prettify_api_query_str(self.api[query_name]('X'))
	
	## custom methods for commonly used tasks
	
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

	def login(self,wallet_public_address,wallet_private_address):
		## CAN ONLY USE THIS METHOD IF YOU HAVE ACCESS TO PRIVATE ADDRESS
		
		## You should NOT send users Private Addresses to your web server (flask/django etc.)
		
		## - For web app: 
		##    - Either run LensPy client side (in browser eg. https://pyscript.net/)
		##    - Or implement login in multiple stages (nb. client means web browser)
		##       1. Client sends a request to Web Server to make a Challenge
		##       2. Web server initiates a Challenge query using LensPy (uses Graphql)
		##       3. Web server receives response and sends to Client the Challenge Text
		##       4. Client signs the challenge text (with users private key) and sends to Web Server
		##       5. Web Server uses signature to initiate an Authenticate mutation using LensPy
		##       6. Web Server receives Access Token as response
		##       7. Web Server can store Access Token associated with a Client session
		
		# Examples of implementing the steps above can be found in our web framework demos
		
		# Once logged in:
		# You can perform mutation (write) gql queries as well as standard (read only) queries
		
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
		signable_message = eth_account.messages.encode_defunct(text = challenge_txt)
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
		self.pub = wallet_public_address
	
	def my_profiles(self,limit=10):
		if not self.authorised:
			return 'Not Logged In'
		else:
			# get profile from handle name gql request
			req_str = 'ownedBy: ["{}"],limit: {}'.format(self.pub,limit)
			my_profiles_req = self.api['profiles'](req_str)
			# execute query and save response
			return self.client.execute_query(my_profiles_req)
	
	def my_profile_handles(self,limit=10):
		if not self.authorised:
			return 'Not Logged In'
		else:
			return list(map(lambda p: p['handle'],self.my_profiles(limit)['profiles']['items']))
	
	def address_profiles(self,address,limit=10):
		# get profile from handle name gql request
		req_str = 'ownedBy: ["{}"],limit: {}'.format(address,limit)
		address_profiles_req = self.api['profiles'](req_str)
		# execute query and save response
		return self.client.execute_query(address_profiles_req)
		
	def address_profile_handles(self,limit=10):
		return list(map(lambda p: p['handle'],self.address_profiles(limit)['profiles']['items']))
	
		
	def following_by_id(self,address,limit=10):
		following = self.following(address,limit)
		return list(map(lambda p: p['profile']['id'],following['following']['items']))
	
	## directly from api
	
	def authenticate(self, address, signature):
		req_str = 'address: "{}",signature:"{}"'.format(address,signature)
		auth_query = self.api['authenticate'](req_str)
		auth_res = self.client.execute_query(auth_query)
		access_token = auth_res['authenticate']['accessToken']
		self.client = GQLClient(token = access_token)
		return access_token
	
	def add_reaction(self,profileId,reaction,publicationId):
		req_str = 'profileId:"{}",reaction: "{}",publicationId: "{}"'.format(profileId,reaction,publicationId)
		add_reaction_req = self.api['addReaction'](req_str)
		return self.client.execute_query(add_reaction_req)
	
	def broadcast(self,broadcastId,signature):
		req_str = 'id:"{}",signature: "{}"'.format(broadcastId,signature)
		broadcast_req = self.api['Broadcast'](req_str)
		# print(broadcast_req)
		return self.client.execute_query(broadcast_req)
	
	def challenge(self, address):
		req_str = 'address:"{}"'.format(address)
		challenge_req = self.api['Challenge'](req_str)
		return self.client.execute_query(challenge_req)
		
	def comment(self,profileId,publicationId,contentURI,collectModule=None,referenceModule=None):
		if collectModule==None:
			collectModule = '{ revertCollectModule: true }'
		if referenceModule==None:
			referenceModule = '{ followerOnlyReferenceModule: false }'
		req_str = 'profileId:"{}",publicationId:"{}",contentURI: "{}",collectModule: {},referenceModule: {}'.format(profileId,publicationId,contentURI,collectModule,referenceModule)
		comment_req = self.api['createCommentTypedData'](req_str)
		# print(prettify_api_query_str(post_req))
		return self.client.execute_query(comment_req)
	
	def create_profile(self, handle, profilePictureUri = None, followNFTURI = None, followModule = None):
		req_str = 'handle:"{}",profilePictureUri: {},followNFTURI: {},followModule: {}'.format(handle,null_param(profilePictureUri),null_param(followNFTURI),null_param(followModule))
		create_profile_req = self.api['CreateProfile'](req_str)
		# execute the query to create a new profile & return
		return self.client.execute_query(create_profile_req)
	
	def default_profile(self,address):
		req_str = 'ethereumAddress:"{}"'.format(address)
		default_profile_req = self.api['defaultProfile'](req_str)
		return self.client.execute_query(default_profile_req)
	
	def delete_profile(self,profileId):
		req_str = 'profileId:"{}"'.format(profileId)
		delete_profile_req = self.api['createBurnProfileTypedData'](req_str)
		return self.client.execute_query(delete_profile_req)
		
	def explore_profiles(self,sortCriteria='MOST_FOLLOWERS'):
		# The sortCriteria can be any of the ProfileSortCriteria below.
		# ProfileSortCriteria:
		# -  CREATED_ON, MOST_FOLLOWERS, LATEST_CREATED,
		# -  MOST_POSTS, MOST_COMMENTS, MOST_MIRRORS,
		# -  MOST_PUBLICATION, MOST_COLLECTS
		req_str = 'sortCriteria:{}'.format(sortCriteria)
		explore_profiles_req = self.api['exploreProfiles'](req_str)
		return self.client.execute_query(explore_profiles_req)
	
	def explore_publications(self,sortCriteria='TOP_COMMENTED',publicationTypes='[POST, COMMENT, MIRROR]',limit=10):
		# The sortCriteria can be any of the ProfileSortCriteria below.
		# PublicationSortCriteria:
		# -  TOP_COMMENTED, TOP_COLLECTED, TOP_MIRRORED,
		# -  LATEST, CURATED_PROFILES
		req_str = 'sortCriteria:{}, publicationTypes:{}, limit:{}'.format(sortCriteria,publicationTypes,limit)
		explore_publications_req = self.api['ExplorePublications'](req_str)
		return self.client.execute_query(explore_publications_req)
	
	def follow(self,profileId,followModule=None):
		# Returns follow typed data - this does not mean you follow the profile
		# You must then Broadcast this typed data or use a dispatcher
		req_str = 'follow:[{profile: "'+profileId+'",followModule: '+null_param(followModule)+'}]'
		print(req_str)
		follow_profile_req = self.api['createFollowTypedData'](req_str)
		return self.client.execute_query(follow_profile_req)
	
	def follow_broadcast(self,private_key,profileId,followModule=None):
		req_str = 'follow:[{profile: "'+profileId+'",followModule: '+null_param(followModule)+'}]'
		follow_profile_req = self.api['createFollowTypedData'](req_str)
		follow_profile_res = self.client.execute_query(follow_profile_req)
		broadcast_id = follow_profile_res['createFollowTypedData']['id']
		typed_data = follow_profile_res['createFollowTypedData']['typedData']
		
		#### LENS designed the broadcast typed data response as (domain, types, value)
		## This follows ethers.js implementation of 'signTypedData'.
		## However Python doesn't have an implementation of this form, instead requiring typed data of the form (domain, types, primaryType, message) as implemented by metamask in js and others.
		## Therefore we require modification of the typed data response so that it is in a compatible format to sign. This requires adding the EIP712Domain domain to types, indicating the primaryType and setting message to be the value typed data. Additionally, on the typed data from Lens, the eth_account method 'encode_structured_data' throws an error when it uses 'eth_abi' to encode certain values in the typed data (in this case: the profileIds and datas). The function 'fix_abi_encode' in LensPy helpers.py uses 'eth_utils' to convert the values to a type that eth_abi can encode.
		
		# print('original typed data', typed_data)
		
		##### START MODIFICATION OF TYPED DATA
		
		typed_data['value']['profileIds'] = fix_abi_encode(typed_data['value']['profileIds'],'int')
		typed_data['value']['datas'] = fix_abi_encode(typed_data['value']['datas'],'bytes')
		
		# typed data response from lens doesn't contain EIP712Domain types field
		typed_data['types']['EIP712Domain'] = [
			{"name":"name","type":"string"},
			{"name":"version","type":"string"},
			{"name":"chainId","type":"uint256"},
			{"name":"verifyingContract","type":"address"}
		]
		
		# typed data response from lens doesn't contain primaryType
		typed_data['primaryType'] = 'FollowWithSig'
		
		# typed data response from lens doesn't contain message (written as value instead)
		typed_data['message'] = typed_data['value']
		del typed_data['value']
		
		# print('new typed data', typed_data)
		
		##### END MODIFICATION OF TYPED DATA
		
		## encode the typed data
		encoded_data = eth_account.messages.encode_structured_data(primitive = typed_data)
		# print(encoded_data)
		
		## Sign either using sign_message (uses private address)
		signed_type_data = w3.eth.account.sign_message(encoded_data,private_key).signature.hex()
		# print(signed_type_data)
		
		return self.broadcast(broadcast_id,signed_type_data)
	
	def followers(self,profileId,limit=10):
		req_str = 'profileId:"{}", limit:"{}"'.format(profileId,limit)
		followers_req = self.api['followers'](req_str)
		return self.client.execute_query(followers_req)
	
	def following(self,address,limit=10):
		req_str = 'address:"{}", limit:"{}"'.format(address,limit)
		following_req = self.api['following'](req_str)
		return self.client.execute_query(following_req)
	
	def get_profile_by_handle(self,handle):
		req_str = 'handle:"{}"'.format(handle)
		profile_req = self.api['profile'](req_str)
		return self.client.execute_query(profile_req)
	
	def get_profile_by_id(self,profileId):
		req_str = 'profileId:"{}"'.format(profileId)
		profile_req = self.api['profile'](req_str)
		return self.client.execute_query(profile_req)
	
	def get_publication(self,publicationId):
		req_str = 'publicationId:"{}"'.format(publicationId)
		publication_req = self.api['publication'](req_str)
		return self.client.execute_query(publication_req)
	
	def get_publications(self,profileId,publicationTypes='[POST,COMMENT,MIRROR]',limit=10):
		req_str = 'profileId:"{}",publicationTypes: {},limit: {}'.format(profileId,publicationTypes,limit)
		publications_req = self.api['publications'](req_str)
		# print(prettify_api_query_str(publications_req))
		return self.client.execute_query(publications_req)
	
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
	
	def mirror(self,profileId,publicationId,referenceModule=None):
		if referenceModule==None:
			referenceModule = '{ followerOnlyReferenceModule: false }'
		req_str = 'profileId:"{}",publicationId: "{}",referenceModule: {}'.format(profileId,publicationId,referenceModule)
		mirror_req = self.api['createMirrorTypedData'](req_str)
		# print(prettify_api_query_str(post_req))
		return self.client.execute_query(mirror_req)
	
	def ping(self):
		ping_req = self.api['ping']()
		return self.client.execute_query(ping_req)	
		
	def post(self,profileId,contentURI,collectModule=None,referenceModule=None):
		if collectModule==None:
			collectModule = '{ revertCollectModule: true }'
		if referenceModule==None:
			referenceModule = '{ followerOnlyReferenceModule: false }'
		req_str = 'profileId:"{}",contentURI: "{}",collectModule: {},referenceModule: {}'.format(profileId,contentURI,collectModule,referenceModule)
		post_req = self.api['createPostTypedData'](req_str)
		# print(prettify_api_query_str(post_req))
		return self.client.execute_query(post_req)
	
	def profile_feed(self, profileId, limit=50):
		req_str = 'profileId:"{}", limit:{}'.format(profileId,limit)
		profile_feed_req = self.api['ProfileFeed'](req_str)
		return self.client.execute_query(profile_feed_req)
	
	def recommended_profiles(self):
		recommended_profiles_req = self.api['recommendedProfiles']()
		return self.client.execute_query(recommended_profiles_req)		
	
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
	
	def set_default_profile(self,profileId):
		req_str = 'profileId: "{}"'.format(profileId)
		set_default_profile_req = self.api['createSetDefaultProfileTypedData'](req_str)
		return self.client.execute_query(set_default_profile_req)
		
	def unfollow(self, profileId):
		req_str = 'profile: "{}"'.format(profileId)
		unfollow_profile_req = self.api['createUnfollowTypedData'](req_str)
		return self.client.execute_query(unfollow_profile_req)