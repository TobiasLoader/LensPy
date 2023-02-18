# import ecdsa
from web3.auto import w3
# import eth_abi
import eth_utils

## data types for eg. profileIds provided by Lens broadcast response
## are not always compatible with 'eth_abi' conversions in 'encode_structured_data'
## so in those cases:
## use 'fix_abi_encode' to modify the input to 'encode_structured_data'
## (this uses eth_utils.to_<type> function)
## eg. Lens returns => profileId: '0x619d' with type 'uint256'
##   this throws error because 'eth_abi' cannot convert '0x619d' to 'uint256'
##   so 'fix_abi_encode' converts '0x619d' to '24989'
##   then 'encode_structured_data' can use 'eth_abi' to convert '24989' to 'uint256'

def fix_abi_encode(els,type):
	if type=='int':
		return map(lambda v: eth_utils.to_int(hexstr=v), els)
	elif type=='bytes':
		return map(lambda v: eth_utils.to_bytes(hexstr=v), els)

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


# allow passing python None as a parameter to the methods in LensPy as opposed to null
def null_param(param):
	if param==None:
		return 'null'
	return '"'+param+'"'



## LEGACY

# def sign_typed_data(typed_data, private_key):
# 	print(typed_data)
# 	schema = []
# 	names = []
# 	types = []
# 	values = []
# 	for type_name,type_data in typed_data['types'].items():
# 		for el in type_data:
# 			schema.append(el['type'] + ' ' + el['name'])
# 			names.append(el['name'])
# 			types.append(el['type'])
# 	i = 0
# 	while i<len(names):
# 		for value_name,value in typed_data['value'].items():
# 			if value_name==names[i]:
# 				# if value_name=='profileIds':
# 					# decoded_hex = [decode_hex(v) for v in value]
# 					# print(decoded_hex)
# 					# encoded_uint256 = eth_abi.decode('uint256', decoded_hex)
# 					# print(encoded_uint256)
# 					# values.append(encoded_uint256)
# 				# else:
# 				values.append(value)
# 				i += 1
# 			if len(values)==len(names):
# 				break
# 	print(schema)
# 	print(types)
# 	print(values)
# 	schema_hash = w3.solidityKeccak(["string" for i in range(len(schema))],schema)
# 	values_hash = w3.solidityKeccak(types,values)
# 	signature_hash = w3.solidityKeccak(["bytes32", "bytes32"],[schema_hash, values_hash])
# 	signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
# 	return signing_key.sign(signature_hash)