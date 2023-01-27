# as of Jan 2023,

# Lens returns typed data responses for which the python equivalent of using _singTypedData (eth_account.messages.encode_structured_data and w3.eth.sign_typed_data) doesn't work

# The javascript _signTypedData is used by Lens
# See the function 'getSig' in lens-protocol/core repo, in helpers/utils.ts file.

# So here below is a direct python implementation of JS _signTypedData

def sign_typed_data(typed_data, private_key):
	return 'to be written here'
	

# prettify_api_query_str() parses and prettify's the graphql query strings stored in LensPy.api
# it does this in 5 stages, 
# 1. it parses through the string removing unwanted chars (and temporarily replacing them with § characters)
# 2. adds new lines in relevant places (depending on § chars)
# 3. removes excess new lines and spaces
# 4. adds indentation to the lines depending on { and }
# 5. iterates backwards to remove indentation before }
# then it returns the reverse of the output on step 5 which should be the prettified query
def prettify_api_query_str(req_str):
	pretty_req_str_1 = ''
	pretty_req_str_2 = ''
	pretty_req_str_3 = ''
	pretty_req_str_4 = ''
	pretty_req_str_5 = ''
	# stage 1
	pre_c = ''
	for c in req_str:
		if c in ['}'] and pre_c not in ['}','§']:
			pretty_req_str_1 += '\n'
		if c not in ['	']:
			if not (c in [' '] and pre_c in ['{','§']):
				pretty_req_str_1 += c
				pre_c = c
			else:
				pretty_req_str_1 += '§'	
		else:
			pretty_req_str_1 += '§'
		if c in ['{'] or (c in ['}'] and pre_c in ['}']):
			pretty_req_str_1 += '\n'
	# stage 2
	pre_c = ''
	for c in pretty_req_str_1:
		if c not in ['§']:
			pretty_req_str_2 += c
			pre_c = c
		elif pre_c not in ['§','\n']:
			pretty_req_str_2 += '\n'
	# stage 3
	pre_c = ''
	for c in pretty_req_str_2:
		if c not in [' ','\n']:
			pretty_req_str_3 += c
			pre_c = c
		else:
			if c in [' ','\n'] and pre_c not in ['\n']:
				pretty_req_str_3 += c
				pre_c = c
	# stage 4
	indent_level = 0
	for c in pretty_req_str_3:
		if c in ['{']:
			indent_level += 1
			indent_dir = 1
		if c in ['}']:
			indent_level -= 1
			indent_dir = -1
		pretty_req_str_4 += c
		if c in ['\n']:
			pretty_req_str_4 += '	'*indent_level
	# stage 5
	pre_c = ''
	for c in pretty_req_str_4[::-1]:
		if c not in ['	'] or pre_c not in ['}']:
			pretty_req_str_5 += c
		pre_c = c
	return pretty_req_str_5[::-1]