import * as home from "./home.js";

// let ls be local state
export let ls = {
	// wallet
	web3: null,
	accounts: null,
	provider: null,
	signer: null,
	// session
	address: null,
	connected: null,
	login: null,
	// user
	profileid: null,
	hasprofile: null,
	hasdefaultprofile: null,
	myprofileidlist: null
}

$(document).ready(()=>{
	
	const {ethereum} = window;
	const {Web3} = window;
	
	if (ethereum===undefined){
		notification('Oops', ['The ethereum library didn\'t load correctly','Please refresh the page, this will most likely fix it.','If this occurs repeatedly please make an issue on the LensPy Github repo.'])
	}
	
	// init local wallet state
	ls.web3 = new Web3(ethereum);
	ls.provider = new ethers.providers.Web3Provider(window.ethereum)
	ls.accounts = null;
	
	// init local session state
	ls.address = window.ethereum.selectedAddress;
	ls.connected = false;
	ls.login = false;
	
	// init local user state
	ls.hasprofile = false;
	ls.hasdefaultprofile = false;
	ls.myprofileidlist = [];
	
	initWalletConnection().then(()=>{
		afterConnectTry();
	});
	
	ethereum.on('accountsChanged', async () => {
		ls.address = window.ethereum.selectedAddress;
		if (address==null) ls.accounts = null;
		ls.connected = isConnected();
		// console.log(address,connected)
		amendConnectWalletButton();
	});
	
	$('h1 a').attr("href", window.location.origin);
});

/// connecting wallet

function isWalletInstalled() {
	return Boolean(window.ethereum);
}

async function connectWallet() {
	ls.accounts = await ethereum.request({method: 'eth_requestAccounts'});
	await ls.provider.send("eth_requestAccounts", []);
	ls.address = ethereum.selectedAddress;
	ls.signer = ls.provider.getSigner();
	// console.log(signer)
	ls.connected = isConnected();
	// console.log(address,connected)
}

function isConnected(){
	return ls.accounts!=null && ls.accounts.length > 0;
}

async function initWalletConnection() {
	if (ls.address!=null && isWalletInstalled() && !isConnected()) await connectWallet();
	else {
		if (!isWalletInstalled()) console.log('Install MetaMask');
		ls.connected = isConnected();
	}
}

function amendConnectWalletButton(){
	if (ls.connected) {
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
	if (ls.connected) {
		if (isHomePage()) home.getDefaultProfile();
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
	let msgHash = ls.web3.utils.sha3(prefix+msg);
	let params = [ls.address,msgHash];
	console.log({method:method,params:params,from:ls.address})
	ls.web3.currentProvider.sendAsync({method:method,params:params,from:ls.address}, function (err, result) {
		console.log(err)
		if (err) notification('Error',[err.message]);
		else callback(result);
	});
}

async function signTypedData(typeddata,callback){
	console.log(typeddata)
	callback(await ls.signer._signTypedData(typeddata['domain'],typeddata['types'],typeddata['value']));
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
	LensPyFetch('/sendbroadcast',{address:ls.address,broadcastId:broadcastId,signature:signature},(data)=>{
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

export function LensPySignThenBroadcast(data_res){
	signTypedData(data_res['typedData'],(sig)=>{
		let broadcastId = data_res['id'];
		let signature = sig;
		LensPyBroadcast(broadcastId,signature,(res)=>{
			console.log(res);
		})
	});
}

export function requiresConnected(func,argsArray=[]){
	if (ls.connected) func.apply(this,argsArray);
	else notification('Not connected wallet!',['You need to connect your wallet to proceed.']);
}

export function requiresLogin(func,argsArray=[]){
	if (ls.login){
		func.apply(this,argsArray);
	} else {
		if (ls.connected) notification('Not logged in!',['The following action is a mutation and you need to be authenticated to perform it. You have connected your wallet but not logged in with LensPy.']);
		else notification('Not connected your wallet or logged in!',['You need to connect your wallet and then login.']);
	}
}

function loginChallengeAuthenticate(){
	LensPyFetch('/getchallenge',{address:ls.address},(res)=>{
		let signableTxt = res['challenge']['text']
		notification('Sign the Challenge text',['Your wallet should allow you to sign.']);
		signMsg(signableTxt, (result)=>{
			let signature = result.result;
			notification('Successfull Signature',['Signature = '+signature.slice(0,7)+'...'+signature.slice(-7)]);
			LensPyFetch('/setauthenticate',{address:ls.address,signature:signature},(res)=>{
				notification('Successfull Authentication',['Access Token = '+res.slice(0,7)+'...'+res.slice(-7)]);
				$('#login').addClass('done');
				ls.login = true;
			});
		});
	});
}


// content sections

export function clearContentSections(){
	$(".content-section").addClass('hide');
}

// jQuery buttons:

$('.back-button').click(function(){
	clearContentSections();
	if (ls.hasprofile && ls.hasdefaultprofile) home.getDefaultProfile();
	if (ls.hasprofile && !ls.hasdefaultprofile) buildSetDefaultProfileSection();
	if (!ls.hasprofile && !ls.hasdefaultprofile) $("#create-profile").removeClass('hide');
});

$('#connect-wallet').click(function(){
	if (ls.connected) {
		notification('Already connected!',['You have already connected your wallet!']);
	}
	else {
		connectWallet().then((v)=>{
			afterConnectTry();
		});
	}
});

$('#login').click(function(){
	if (!ls.connected) notification('Need to connect your wallet.',['Logging in requires you to have connected your wallet.','If you do not have one, I would suggest getting MetaMask.']);
	else if (ls.login) notification('Already logged in!',['You have already logged in!']);
	else loginChallengeAuthenticate();
});

$('#search-profile-input').on('keypress',function(e) {
	if (e.which === 13) {
		let handleSearchQuery = $(this).val();
		window.location.href = window.location.origin+'/search-profile?handle='+handleSearchQuery;
	}
})

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