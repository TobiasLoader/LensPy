from lenspy.LensPy import LensPy

# these are random key pair from docs at 
# https://web3js.readthedocs.io/en/v1.2.11/web3-eth-accounts.html

pub = "0xb8CE9ab6943e0eCED004cDe8e3bBed6568B2Fa01"
pri = "0x348ce564d427a3311b6536bbcff9390d69395b06ed6c486954e971d960fe8709"


lp = LensPy()
lp.login(pub,pri)
# print(lp.my_profiles())
# print(lp.my_profile_handles())
# lp.available_methods()
# lp.available_methods(True)
lp.available_raw_api_calls()
# print(lp.create_profile('tobblit3'))
print('tobblit profile id: ',lp.get_profile_id('tobblit'))
print('tobblit2 profile id: ',lp.get_profile_id('tobblit2'))
# print(lp.follow("0x619d"))
print(lp.follow_broadcast("0x619d",pri))
# print(lp.follow("0x01"))
# print(lp.follower_nft_owned_token_ids())
print('1 followed by me: ', lp.is_followed_by_me("0x01"))
print('# tobblit2 followers', len(lp.followers("0x61d1")['followers']['items']))
# print('# 1 followers', len(lp.followers("0x01")['followers']['items']))
print('who Im following: ', lp.following(pub))
# print('is 0x619d following 0x01: ', lp.is_following('0x619d', '0x01'))
# print('my default profile: ', lp.default_profile(pub))
# print(lp.unfollow("0x01"))
print(lp.profile_feed("0x619d",10))
print(lp.ping())