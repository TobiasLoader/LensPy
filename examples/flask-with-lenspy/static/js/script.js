const {ethereum} = window;
const {Web3} = window;
var web3 = new Web3(ethereum);
let accounts = null;
let connected = false;
let address = window.ethereum.selectedAddress;
let login = false;

/// connecting wallet

$(document).ready(()=>{
	initWalletConnection().then(()=>{
		afterConnectTry();
	});
});

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
		$('#connect-wallet p').text('Connected!');
		$('#connect-wallet').addClass('done');
	} else {
		console.log("user not connected");
		$('#connect-wallet').removeClass('done');
		$('#connect-wallet p').text('Connect Wallet');
	}
}

function afterConnectTry(){
	amendConnectWalletButton();
	$('#connect-wallet').removeClass('hide');
	if (connected) {
		getProfile();
		$('#login').removeClass('hide');
	}
}

ethereum.on('accountsChanged', async () => {
	address = window.ethereum.selectedAddress;
	if (address==null) accounts = null;
	connected = isConnected();
	console.log(address,connected)
	amendConnectWalletButton();
});

/// useful functions

function notification(title,txt_array){
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

/// fetch requests to server

function json(response) {
	return response.json()
}

function getChallenge(callback){
	fetch('/getchallenge', {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
		},
		body: JSON.stringify({
			address:address
		})
	}).then(json).then(function (data) {
		callback(data['lp_res']);
	}).catch(function (error) {
		console.log('Request failed', error);
		notification('Request failed',[error]);
	});
}

function setAuthenticate(signature,callback){
	fetch('/setauthenticate', {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
		},
		body: JSON.stringify({
			address:address,
			signature:signature,
		})
	}).then(json).then(function (data) {
		callback(data['lp_res']);
	}).catch(function (error) {
		console.log('Request failed', error);
		notification('Request failed',[error]);
	});
}

function getProfile(){
	fetch('/getprofile', {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
		},
		body: JSON.stringify({
			address:address
		})
	}).then(json).then(function (data) {
		console.log(data);
		if (!data['lp_res']){
			$("#null-profile").removeClass('hide');
		} else {
			$("#view-profile h2").text('Hi '+ data['lp_res']+'!');
			$("#view-profile").removeClass('hide');
		}
	}).catch(function (error) {
		console.log('Request failed', error);
		notification('Request failed',[error]);
	});
}

function createProfile(handle,callback){
	fetch('/createprofile', {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
		},
		body: JSON.stringify({
			handle:handle
		})
	}).then(json).then(function (data) {
		callback(data['lp_res']);
	}).catch(function (error) {
		console.log('Request failed', error);
		notification('Request failed',[error]);
	});
}

// jQuery buttons:

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
	else {
		getChallenge((res)=>{
			let signableTxt = res['challenge']['text']
			notification('Sign the Challenge text',['Your wallet should allow you to sign.']);
			let method = 'eth_sign';
			console.log(signableTxt)
			let prefix = "\x19Ethereum Signed Message:\n" + signableTxt.length;
			let msgHash = web3.utils.sha3(prefix+signableTxt);
			let params = [address,msgHash];
			web3.currentProvider.sendAsync({method,params,from: address}, function (err, result) {
				if (err) {
					notification('Error',[err.message]);
					return null;
				}
				let signature = result.result;
				notification('Successfull Signature',['Signature = '+signature.slice(0,7)+'...'+signature.slice(-7)]);
				setAuthenticate(signature,(res)=>{
					notification('Successfull Authentication',['Access Token = '+res.slice(0,7)+'...'+res.slice(-7)]);
					$('#login').addClass('done');
					login = true;
				});
			});
		});
	}
});

$('#create-profile-btn').click(function(){
	$("#null-profile").addClass('hide');
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
			createProfile(h, (data)=>{
				console.log(data);
				if (data['createProfile']['reason']=='HANDLE_TAKEN'){
					notification('Handle Taken',['I\'m sorry that handle has already been taken.','Try another handle name.']);
				} else {
					notification('Congrats!',['You now own the handle: '+h,'','Note: this handle is associated with','--> '+address,'','Ethereum address used to connect wallet.']);
					getProfile();
				}
			});
		}
		
	} else {
		if (connected) notification('Not logged in!',['The following action is a mutation and you need to be authenticated to perform it. You have connected your wallet but not logged in with LensPy.']);
		else notification('Not connected your wallet or logged in!',['You need to connect your wallet and login.']);
	}
});