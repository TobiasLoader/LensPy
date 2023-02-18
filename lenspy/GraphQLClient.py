from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from graphql.type import GraphQLSchema
import json
import time

with open('lenspy/lens-api.schema.graphql','r', encoding = 'utf-16') as f:
    schema_str = f.read()
    # print(schema_str)

class GQLClient:
    def __init__(self,url="https://api-mumbai.lens.dev", token = None):
        # does the client have an access token?
        # if yes - then can write – do mutations (eg. post or change profile)
        # if not - then can only read from lens protocol (eg. read publications)
        # OBTAIN access token by the "login" method in LensPy.py
        self.url = url
        if token != None:
            transport = RequestsHTTPTransport(url = url, headers = {"Authorization":f"Bearer {token}"})
        else:
            transport = RequestsHTTPTransport(url = url)
        # sets up the GraphQL Client
        self.client = Client(transport = transport, schema = schema_str)
        self.executing_query = False
    
    # TODO: rewrite execute query – maybe add async queue if client is in use already?
    def execute_query(self,query):
        if not self.executing_query:
            # print('EXECUTING QUERY',query[0:20])
            self.executing_query = True
            result = self.client.execute(gql(query))
            self.executing_query = False
            return result
        else:
            start_wait_time = time.time()
            # print('WAIT QUERY',query[0:20])
            while True:
                if not self.executing_query:
                    return self.execute_query(query)
                if time.time()-start_wait_time>1:
                    print('Timeout – time elapsed waiting for previous graphql call to execute')
                    return None