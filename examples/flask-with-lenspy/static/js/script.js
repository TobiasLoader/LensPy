const {ethereum} = window;
let accounts = null;
let connected = false;
let address = window.ethereum.selectedAddress;

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
		$('#connect-wallet').addClass('connected');
	} else {
		console.log("user not connected");
		$('#connect-wallet').removeClass('connected');
		$('#connect-wallet p').text('Connect Wallet');
	}
}

ethereum.on('accountsChanged', async () => {
	address = window.ethereum.selectedAddress;
	if (address==null) accounts = null;
	connected = isConnected();
	console.log(address,connected)
	amendConnectWalletButton();
});

$(document).ready(()=>{
	initWalletConnection().then(()=>{
		amendConnectWalletButton();
		$('#connect-wallet').removeClass('hide');
		if (connected) getProfile();
	});
});

function json(response) {
	return response.json()
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
		// console.log(data);
		if (data['lp_res']['defaultProfile']==null){
			$("#null-profile").removeClass('hide');
		}
	}).catch(function (error) {
		console.log('Request failed', error);
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
	});
}


// jQuery buttons:

$('#connect-wallet').click(function(){
	if (!connected) {
		connectWallet().then((v)=>{
			amendConnectWalletButton();
			getProfile();
		});
	}
});

$('#create-profile-btn').click(function(){
	$("#null-profile").addClass('hide');
	$("#create-profile").removeClass('hide');
});

$('#create-profile-send-btn').click(function(){
	createProfile($('#create-profile-handle-input').val(), (data)=>{
		console.log(data);
		if (data['createProfile']['reason']=='HANDLE_TAKEN'){
			console.log('HANDLE_TAKEN');
		}
	});
});