// import { ethers } from "https://cdn.ethers.io/lib/ethers-5.2.esm.min.js";

let web3;
let accounts;
let connected;
let address;
let login;
let hasprofile;
let hasdefaultprofile;
let myprofileidlist;

$(document).ready(()=>{
	
	const {ethereum} = window;
	const {Web3} = window;
	
	if (ethereum===undefined){
		notification('Oops', ['The ethereum library didn\'t load correctly','Please refresh the page, this will most likely fix it.','If this occurs repeatedly please make an issue on the LensPy Github repo.'])
	}
	
	web3 = new Web3(ethereum);
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
	address = ethereum.selectedAddress;
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

function signTypedData(typeddata,callback){
	let method = 'eth_signTypedData_v4';
	console.log(typeddata)
	typeddata['types']['EIP712Domain'] = [
		{ name: 'name', type: 'string' },
		{ name: 'version', type: 'string' },
		{ name: 'chainId', type: 'uint256' },
		{ name: 'verifyingContract', type: 'address' },
	];
	typeddata['message'] = typeddata['value'];
	delete typeddata['value'];
	typeddata['primaryType'] = 'EIP712Domain';
	let msgParams = JSON.stringify(typeddata);
	let params = [address,msgParams];
	console.log({method:method,params:params,from:address})
	web3.currentProvider.sendAsync({method:method,params:params,from:address}, function (err, result) {
		console.log(err)
		if (err) notification('Error',[err.message]);
		else callback(result);
	});
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
		callback(data);
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
		// console.log(data);
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
			hasprofile = true;
			hasdefaultprofile = true;
			$("#my-profile h2#my-profile-name").text(data['defaultProfile']['handle']);
			$("#my-profile").removeClass('hide');
		}
	});
}

function setDefaultProfile(profileId){
	LensPyFetch('/setdefaultprofile',{address:address,profileId:profileId},(data)=>{
		// console.log(data);
		console.log('set default profile',profileId);
		signTypedData(data['createSetDefaultProfileTypedData']['typedData'],(sig)=>{
			let broadcastId = data['createSetDefaultProfileTypedData']['id'];
			let signature = sig.result;
			LensPyBroadcast(broadcastId,signature,(res)=>{
				console.log(res);
				if (res['broadcast']['reason']=="WRONG_WALLET_SIGNED") notification('Signature Incorrect!',['Oops the signature is incorrect. Please try again.']);
			})
		})
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