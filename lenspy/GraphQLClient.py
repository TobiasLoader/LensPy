from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from graphql.type import GraphQLSchema
import json

with open('lenspy/schema.graphql','r', encoding = 'utf-16') as f:
    schema_str = f.read()
    print(schema_str[0:10])

class GQLClient:
    def __init__(self,url="https://api-mumbai.lens.dev", token = None):
        # does the client have an access token?
        # if yes - then can write – do mutations (eg. post or change profile)
        # if not - then can only read from lens protocol (eg. read publications)
        # OBTAIN access token by the "login" method in LensPy.py
        if token != None:
            transport = AIOHTTPTransport(url = url, headers = {"Authorization":f"Bearer {token}"})
        else:
            transport = AIOHTTPTransport(url = url)
        # sets up the GraphQL Client
        self.client = Client(transport = transport, schema = schema_str)
        
    def execute_query(self,query):
        print(query)
        # return response from server of query
        return self.client.execute(query)
