from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from graphql.type import GraphQLSchema
import json

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
        
    def execute_query(self,query):
        self.client.close_sync()
        return self.client.execute(gql(query))