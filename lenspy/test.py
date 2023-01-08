from LensPy import LensPy

# these are random key pair from docs at 
# https://web3js.readthedocs.io/en/v1.2.11/web3-eth-accounts.html

pub = "0xb8CE9ab6943e0eCED004cDe8e3bBed6568B2Fa01"
pri = "0x348ce564d427a3311b6536bbcff9390d69395b06ed6c486954e971d960fe8709"


lp = LensPy()
lp.login(pub,pri)
lp.available_api_calls()
print(lp.createProfile('tobblit'))
print('tobblit profile id: ',lp.getProfileId('tobblit'))
print(lp.ping())