def parse_callable_api_from_graphql(graphql_docs_file='lenspy/lens-api.documents.graphql'):
	with open(graphql_docs_file,'r') as f:
		documents_graphql = f.read()
	api_raw_str = {'mutation': [],'query': [],'fragment': [],}
	api_str = {'mutation': {'no_params':[],'one_param':[]},'query': {'no_params':[],'one_param':[]},}
	api_func = {'mutation': {},'query': {},}
	api = {}
	seperate_graphql = []
	fragments = {}
	bracket = 0
	bucket = []
	# for debugging purposes - uncomment q and lines 25-26
	# q = 'fragment MetadataOutputFields'
	for c in documents_graphql:
		if c not in ['\n']:
			bucket.append(c)
		if c == '{':
			bracket += 1
		elif c == '}':
			bracket -= 1
			if bracket==0:
				seperate_graphql.append(''.join(bucket))
				bucket = []
	for graphql_doc in seperate_graphql:
		# if graphql_doc[0:len(q)]==q:
		# 	print(graphql_doc)
		type_graphql = graphql_doc.split(' ')[0]
		api_raw_str[type_graphql].append(graphql_doc)
	for type_graphql in ['mutation','query']:
		for graphql in api_raw_str[type_graphql]:
			head = graphql.split(' ')[1]
			if '$' in head:
				api_str[type_graphql]['one_param'].append(graphql[:graphql.index('(')]+graphql[graphql.index(')')+1:])
			else:
				api_str[type_graphql]['no_params'].append(graphql)
	for frag in api_raw_str['fragment']:
		func_name = frag.split(' ')[1]
		fragments[func_name] = frag
	# print(fragments['MetadataOutputFields'])
	def add_required_fragments(current_x):
		frags = []
		done = False
		while not done:
			repeat = False
			for fkey,fvalue in fragments.items():
				if fkey not in frags and ('...'+fkey) in current_x:
					current_x += '\n' + fvalue
					frags.append(fkey)
					repeat = True
					break
			if not repeat:
				done = True
		return current_x
	def return_graphql_no_params(graphql):
		return lambda: graphql
	def return_graphql_one_param(graphql):
		return lambda request: graphql.replace('$request','{'+request+'}');
	for type_graphql in ['mutation','query']:
		for graphql in api_str[type_graphql]['no_params']:
			func_name = graphql.split(' ')[1]
			with_fragments = add_required_fragments(graphql)
			api_func[type_graphql][func_name] = return_graphql_no_params(with_fragments)
		for graphql in api_str[type_graphql]['one_param']:
			func_name = graphql.split(' ')[1]
			with_fragments = add_required_fragments(graphql)
			api_func[type_graphql][func_name] = return_graphql_one_param(with_fragments)
	for type_graphql in ['mutation','query']:
		for fname,f in api_func[type_graphql].items():
			api[fname] = f
	return api

def print_query_strings(api_query):
	for c in api_query:
		print(c,end='')