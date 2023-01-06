# from GraphQLClient import client
# from queries import *
# from gql import gql
# from web3.auto import w3
# from eth_account.messages import encode_defunct
# import logging
# logging.basicConfig(level=logging.DEBUG)
# 
# unauthorised_client = client()
# # print(client.client.schema)
# wallet_private_address = ''
# 
# wallet_public_address = '0x7CFFc134A864bc05A1Dcf73966E5bF6a20E8F6A3'
# 
# chAllenge = gql(Challenge("address:"+'"'+wallet_public_address+'"'))
# print(chAllenge)
# # print("mutation:"+"'"+chAllenge+"'")
# # x = client.execute_query("query:"+"'"+chAllenge+"'")
# challengeres = unauthorised_client.execute_query(chAllenge)
# txt = challengeres['challenge']['text']
# 
# message = encode_defunct(text = txt)
# signed_message = w3.eth.account.sign_message(message,private_key = wallet_private_address)
# # print(signed_message.signature.hex())
# # passphrase = 'hurry fiction expect volume begin juice known sister athlete seat lizard miss'
# 
# 
# 
# 
# # result = web3.eth.sign(
# #     wallet_public_address,
# #     text = txt
# # )
# # print(result)
# 
# 
# # query = gql(
# #     """
# #     query ping {
# #     ping
# #     }
# #     """
# # )
# 
# aUthenticate = gql(authenticate("address:"+'"'+wallet_public_address+'",'+'signature:'+'"'+signed_message.signature.hex()+'"'))
# print(aUthenticate)
# x = unauthorised_client.execute_query(aUthenticate)
# access_token = x['authenticate']['accessToken']
# 
# authorised_client = client(token = access_token)
# 
# 
# 
# cREatepRofILe = gql(createProfile('handle:"tobysarcasm6",profilePictureUri: "https://www.google.com/url?sa=i&url=https%3A%2F%2Fuk.linkedin.com%2Fin%2Ftobiasloader&psig=AOvVaw3ie0tA4cNhIGS7THlaW0lb&ust=1668403437074000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCOCk66K1qvsCFQAAAAAdAAAAABAE",followNFTURI: null,followModule: null'))
# 
# x = authorised_client.execute_query(query = cREatepRofILe)
# # profile = x['createProfile']['txHash']
# 
# pRofIle = gql(
#     """
#     query SearchProfiles {
#   search(request: {
#     query: "toby",
#     type: PROFILE,
#     limit: 5
#   }) {
#     ... on ProfileSearchResult {
#       __typename
#       items {
#         ... on Profile {
#           handle
#           id
#         }
#       }
#       
#     }
#   }
# }
# 
# """
# )
# y = authorised_client.execute_query(query = pRofIle)
# print(y)

