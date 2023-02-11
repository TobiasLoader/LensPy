// import { ethers } from "https://cdn.ethers.io/lib/ethers-5.2.esm.min.js";
// import { ethers } from "./ethers";

let web3;
let accounts;
let connected;
let address;
let profileid;
let login;
let hasprofile;
let hasdefaultprofile;
let myprofileidlist;
let signer;
let provider;

$(document).ready(()=>{
	
	const {ethereum} = window;
	const {Web3} = window;
	
	if (ethereum===undefined){
		notification('Oops', ['The ethereum library didn\'t load correctly','Please refresh the page, this will most likely fix it.','If this occurs repeatedly please make an issue on the LensPy Github repo.'])
	}
	
	web3 = new Web3(ethereum);
	provider = new ethers.providers.Web3Provider(window.ethereum)
	accounts = null;
	connected = false;
	address = window.ethereum.selectedAddress;
	login = false;
	hasprofile = false;
	hasdefaultprofile = false;
	myprofileidlist = [];
	
	initWalletConnection().then(()=>{
		afterConnectTry();
	});
	
	ethereum.on('accountsChanged', async () => {
		address = window.ethereum.selectedAddress;
		if (address==null) accounts = null;
		connected = isConnected();
		console.log(address,connected)
		amendConnectWalletButton();
	});
	
	$('h1 a').attr("href", window.location.origin);
});

// can be overridden in other js files
var initPageLoad = ()=>{console.log('Loaded')};

/// connecting wallet

function isWalletInstalled() {
	return Boolean(window.ethereum);
}

async function connectWallet() {
	accounts = await ethereum.request({method: 'eth_requestAccounts'});
	await provider.send("eth_requestAccounts", []);
	address = ethereum.selectedAddress;
	signer = provider.getSigner();
	console.log(signer)
	connected = isConnected();
	console.log(address,connected)
}

function isConnected(){
	return accounts!=null && accounts.length > 0;
}

async function initWalletConnection() {
	if (address!=null && isWalletInstalled() && !isConnected()) await connectWallet();
	else {
		if (!isWalletInstalled()) console.log('Install MetaMask');
		connected = isConnected();
	}
}

function amendConnectWalletButton(){
	if (connected) {
		console.log("user connected");
		$('#connect-wallet p').text('Wallet Connected!');
		$('#connect-wallet').addClass('done');
	} else {
		console.log("user not connected");
		$('#connect-wallet').removeClass('done');
		$('#connect-wallet p').text('Connect Wallet');
	}
}

function afterConnectTry(){
	amendConnectWalletButton();
	if (isHomePage()) clearContentSections();
	$('#connect-wallet').removeClass('hide');
	$('#login').removeClass('hide');
	$('#search-wrapper').removeClass('hide');
	if (connected) {
		if (isHomePage()) getDefaultProfile();
		$('#login').removeClass('done');
	} else {
		if (isHomePage()) $('#home').removeClass('hide');
	}
}

function isHomePage(){
	return window.location.href===window.location.origin+'/';
}

/// signatures

function signMsg(msg,callback){
	let method = 'eth_sign';
	let prefix = "\x19Ethereum Signed Message:\n" + msg.length;
	let msgHash = web3.utils.sha3(prefix+msg);
	let params = [address,msgHash];
	console.log({method:method,params:params,from:address})
	web3.currentProvider.sendAsync({method:method,params:params,from:address}, function (err, result) {
		console.log(err)
		if (err) notification('Error',[err.message]);
		else callback(result);
	});
}

async function signTypedData(typeddata,callback){
	console.log(typeddata)
	callback(await signer._signTypedData(typeddata['domain'],typeddata['types'],typeddata['value']));
	// OLD METHOD – used domain/types/message/primaryMessage structure
	// however Lens uses - domain/types/value structure used by ethers.js
	
	// let method = 'eth_signTypedData_v4';
	// typeddata['types']['EIP712Domain'] = [
	// 	{ name: 'name', type: 'string' },
	// 	{ name: 'version', type: 'string' },
	// 	{ name: 'chainId', type: 'uint256' },
	// 	{ name: 'verifyingContract', type: 'address' },
	// ];
	// typeddata['message'] = typeddata['value'];
	// delete typeddata['value'];
	// typeddata['primaryType'] = 'EIP712Domain';
	// let msgParams = JSON.stringify(typeddata);
	// let params = [address,msgParams];
	// console.log({method:method,params:params,from:address})
	// web3.currentProvider.sendAsync({method:method,params:params,from:address}, function (err, result) {
	// 	console.log(err)
	// 	if (err) notification('Error',[err.message]);
	// 	else callback(result);
	// });
}


/// fetch requests to server

function json(response) {
	return response.json()
}

export function LensPyFetch(endpoint,bodyobj,callback){
	fetch(endpoint, {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
		},
		body: JSON.stringify(bodyobj)
	}).then(json).then(function (data) {
		callback(data['lp_res']);
	}).catch(function (error) {
		console.log('Request failed', error);
		notification('Request failed',[error]);
	});
}

export function LensPyBroadcast(broadcastId,signature,callback){
	LensPyFetch('/sendbroadcast',{address:address,broadcastId:broadcastId,signature:signature},(data)=>{
		let reason = data['broadcast']['reason'];
		if (reason=="REJECTED") notification('Signature [REJECTED]!',['Oops the typed data signature is incorrect, it was rejected.','Please try again.']);
		else if (reason=="EXPIRED") notification('Signature [EXPIRED]!',['Oops the signature is incorrect, the data has expired.','Please try again.']);
		else if (reason=="WRONG_WALLET_SIGNED") notification('Signature [WRONG_WALLET_SIGNED]!',['Oops the signature is incorrect, the wrong wallet signed or the data was formatted incorrectly.','Please try again.']);
		else if (reason=="NOT_ALLOWED") notification('Signature [NOT_ALLOWED]!',['Oops the signature is incorrect, the signature was not allowed.','Please try again.']);
		else {
			notification('🎉 Success!',['The typed data from your request was correctly signed and it has been "Broadcast" by Lens Protocol to the chain.']);
			callback(data);
		}
	});
}

function loginChallengeAuthenticate(){
	LensPyFetch('/getchallenge',{address:address},(res)=>{
		let signableTxt = res['challenge']['text']
		notification('Sign the Challenge text',['Your wallet should allow you to sign.']);
		signMsg(signableTxt, (result)=>{
			let signature = result.result;
			notification('Successfull Signature',['Signature = '+signature.slice(0,7)+'...'+signature.slice(-7)]);
			LensPyFetch('/setauthenticate',{address:address,signature:signature},(res)=>{
				notification('Successfull Authentication',['Access Token = '+res.slice(0,7)+'...'+res.slice(-7)]);
				$('#login').addClass('done');
				login = true;
			});
		});
	});
}

function getDefaultProfile(){
	clearContentSections();
	LensPyFetch('/getdefaultprofile',{address:address},(data)=>{
		if (data['defaultProfile']==null){
			getAllProfiles((data)=>{
				// console.log(data);
				if (data.length==0) $("#null-profile").removeClass('hide');
				else {
					hasprofile = true;
					notification('No default profile!',['You have '+data.length+' profiles','but no default one.']);
					buildSetDefaultProfilePage();
				}
			});
		} else {
			profileid = data['defaultProfile']['id'];
			hasprofile = true;
			hasdefaultprofile = true;
			$("#my-profile h2#my-profile-name").text(data['defaultProfile']['handle']);
			$("#my-profile").removeClass('hide');
		}
	});
}

function setDefaultProfile(profileId){
	LensPyFetch('/setdefaultprofile',{address:address,profileId:profileId},(data)=>{
		signTypedData(data['createSetDefaultProfileTypedData']['typedData'],(sig)=>{
			let broadcastId = data['createSetDefaultProfileTypedData']['id'];
			let signature = sig;
			LensPyBroadcast(broadcastId,signature,(res)=>{
				console.log(res);
			});
		});
	});
}

function postPublication(contentURI=null,collectModule=null,referenceModule=null){
	// you should check out chriscomrie.lens beginners guide below
	if (contentURI==null) contentURI = 'https://arweave.net/9FJ-xFdOr9hRxoS3lezu_ZvRP6ANk_dUpcxQrvD3L_s';
	LensPyFetch('/post',{address:address,profileId:profileid,contentURI:contentURI,collectModule:collectModule,referenceModule:referenceModule},(data)=>{
		signTypedData(data['createPostTypedData']['typedData'],(sig)=>{
			let broadcastId = data['createPostTypedData']['id'];
			let signature = sig;
			LensPyBroadcast(broadcastId,signature,(res)=>{
				console.log(res);
			})
		});
	});
}

function getAllProfiles(callback){
	LensPyFetch('/getallprofiles',{address:address},callback);
}

function createProfile(handle){
	LensPyFetch('/createprofile',{address:address,handle:handle}, (data)=>{
		if (data['createProfile']['reason']=='HANDLE_TAKEN'){
			notification('Handle Taken',['I\'m sorry that handle has already been taken.','Try another handle name.']);
		} else {
			notification('Congrats!',['You now own the handle: '+handle,'','Note: this handle is associated with','--> '+address,'','Ethereum address used to connect wallet.']);
			getDefaultProfile();
		}
	});
}

// build content sections

function clearContentSections(){
	$(".content-section").addClass('hide');
}

function buildSetDefaultProfileSection(){
	clearContentSections();
	$("#set-default-profile").removeClass('hide');
	LensPyFetch('/getallprofiles',{address:address},(data)=>{
		$("#current-profiles").empty();
		myprofileidlist = [];
		for (var profile of data){
			$("#current-profiles").append('<li>'+profile['handle']+' – '+profile['profileId']+'</li>');
			myprofileidlist.push(profile['profileId']);
		}
	});
}

// jQuery buttons:

$('.back-button').click(function(){
	clearContentSections();
	if (hasprofile && hasdefaultprofile) getDefaultProfile();
	if (hasprofile && !hasdefaultprofile) {
		buildSetDefaultProfileSection();
	}
	if (!hasprofile && !hasdefaultprofile) $("#create-profile").removeClass('hide');
});

$('#connect-wallet').click(function(){
	if (connected) notification('Already connected!',['You have already connected your wallet!']);
	else {
		connectWallet().then((v)=>{
			afterConnectTry();
		});
	}
});

$('#login').click(function(){
	if (!connected) notification('Need to connect your wallet.',['Logging in requires you to have connected your wallet.','If you do not have one, I would suggest getting MetaMask.']);
	else if (login) notification('Already logged in!',['You have already logged in!']);
	else loginChallengeAuthenticate();
});

$('#search-profile-input').on('keypress',function(e) {
	if (e.which === 13) {
		let handleSearchQuery = $(this).val();
		window.location.href = window.location.origin+'/search-profile?handle='+handleSearchQuery;
	}
})

$('#options-btn').click(function(){
	clearContentSections();
	$("#options").removeClass('hide');
});

$('#post-btn').click(function(){
	clearContentSections();
	$("#post").removeClass('hide');
});

$('#create-post-send-btn').click(function(){
	if (login){
		let contentURI = $('#create-post-contentURI-input').val();
		let collectModule = $('#create-post-collectmodule-input').val();
		let referenceModule = $('#create-post-referencemodule-input').val();
		if (contentURI.length==0) notification('Content URI field blank',['The content URI:','ipfs://QmPogtffEF3oAbKERsoR4Ky8aTvLgBF5totp5AuF8YN6vl','is being used instead.','* taken from lens docs']);
		// not passing collect/reference modules yet.
		// let the defaults be used as defined in lenspy
		postPublication(contentURI);
	} else {
		if (connected) notification('Not logged in!',['The following action is a mutation and you need to be authenticated to perform it. You have connected your wallet but not logged in with LensPy.']);
		else notification('Not connected your wallet or logged in!',['You need to connect your wallet and then login.']);
	}
});

$('#create-profile-btn').click(function(){
	clearContentSections();
	$("#create-profile").removeClass('hide');
});

$('#create-profile-send-btn').click(function(){
	if (login){
		let h = $('#create-profile-handle-input').val();
		if (h.length<5){
			notification('Handle too short',['Lens handles must have a minimum of 5 characters.']);
		} else if (h.length>31){
			notification('Handle too long',['Lens handles must have a maximum of 31 characters.']);
		} else {
			createProfile(h);
		}
	} else {
		if (connected) notification('Not logged in!',['The following action is a mutation and you need to be authenticated to perform it. You have connected your wallet but not logged in with LensPy.']);
		else notification('Not connected your wallet or logged in!',['You need to connect your wallet and login.']);
	}
});

$('#create-another-profile-btn').click(function(){
	clearContentSections();
	$("#create-profile").removeClass('hide');
});

$('#set-default-profile-btn').click(function(){
	buildSetDefaultProfileSection();
});

$('#set-default-profile-send-btn').click(function(){
	if (login){
		let id = $('#set-default-profile-input').val();
		console.log(myprofileidlist)
		if (id.length % 2 != 0){
			notification('Odd number of charaters!',['Lens profile ids are even in length.']);
		} else if (id.slice(0,2)!='0x'){
			notification('Doesn\'t start with 0x',['Lens profile ids start with a 0x.']);
		}  else if (!myprofileidlist.includes(id)){
			notification('Not your profile!',['The Ethereum address you are logged in with does not own the profile with that id.']);
		} else {
			setDefaultProfile(id);
		}
	} else {
		if (connected) notification('Not logged in!',['The following action is a mutation and you need to be authenticated to perform it. You have connected your wallet but not logged in with LensPy.']);
		else notification('Not connected your wallet or logged in!',['You need to connect your wallet and then login.']);
	}
});

/// useful functions

export function notification(title,txt_array){
	$('#notification #notif-title').empty();
	$('#notification #notif-desc').empty();
	$('#notification #notif-title').text(title);
	for (var txt of txt_array){
		$('#notification #notif-desc').append('<p>'+txt+'</p>');
	}
	$('#notif-wrapper').removeClass('hide');
}

$('#notification #notif-cross').click(function(){
	$('#notif-wrapper').addClass('hide');
});