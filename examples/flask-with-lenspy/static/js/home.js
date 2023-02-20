import * as main from "./main.js";

export function getDefaultProfile(){
	main.clearContentSections();
	main.LensPyFetch('/getdefaultprofile',{address:main.ls.address},(data)=>{
		if (data['defaultProfile']==null){
			main.LensPyFetch('/getallprofiles',{address:main.ls.address},(data)=>{
				// console.log(data);
				if (data.length==0) $("#null-profile").removeClass('hide');
				else {
					main.ls.hasprofile = true;
					main.notification('No default profile!',['You have '+data.length+' profiles','but no default one.']);
					buildSetDefaultProfilePage();
				}
			});
		} else {
			console.log(data);
			main.ls.profileid = data['defaultProfile']['id'];
			main.ls.hasprofile = true;
			main.ls.hasdefaultprofile = true;
			$("#my-profile h2#my-profile-name").text(data['defaultProfile']['handle']);
			$("#my-profile p#my-profile-id").text(data['defaultProfile']['id']);
			$("#my-profile").removeClass('hide');
		}
	});
}

function setDefaultProfile(profileId){
	main.LensPyFetch('/setdefaultprofile',{address:main.ls.address,profileId:profileId},(data)=>{
		main.LensPySignThenBroadcast(data['createSetDefaultProfileTypedData']);
	});
}

function postPublication(contentURI=null,collectModule=null,referenceModule=null){
	// you should check out chriscomrie.lens beginners guide below
	if (contentURI==null) contentURI = 'https://arweave.net/9FJ-xFdOr9hRxoS3lezu_ZvRP6ANk_dUpcxQrvD3L_s';
	main.LensPyFetch('/post',{address:main.ls.address,profileId:profileid,contentURI:contentURI,collectModule:collectModule,referenceModule:referenceModule},(data)=>{
		main.LensPySignThenBroadcast(data['createPostTypedData']);
	});
}

function createProfile(handle){
	main.LensPyFetch('/createprofile',{address:main.ls.address,handle:handle}, (data)=>{
		if (data['createProfile']['reason']=='HANDLE_TAKEN'){
			main.notification('Handle Taken',['I\'m sorry that handle has already been taken.','Try another handle name.']);
		} else {
			main.notification('Congrats!',['You now own the handle: '+handle,'','Note: this handle is associated with','--> '+main.ls.address,'','Ethereum address used to connect wallet.']);
			getDefaultProfile();
		}
	});
}


/////// Content Sections

function buildSetDefaultProfileSection(){
	main.clearContentSections();
	$("#set-default-profile").removeClass('hide');
	main.LensPyFetch('/getallprofiles',{address:main.ls.address},(data)=>{
		$("#current-profiles").empty();
		main.ls.myprofileidlist = [];
		for (var profile of data){
			$("#current-profiles").append('<li>'+profile['handle']+' – '+profile['profileId']+'</li>');
			main.ls.myprofileidlist.push(profile['profileId']);
		}
	});
}

///////// jQuery Buttons


$('#options-btn').click(function(){
	main.clearContentSections();
	$("#options").removeClass('hide');
});

$('#post-btn').click(function(){
	main.clearContentSections();
	$("#post").removeClass('hide');
});

$('#following-btn').click(function(){
	main.requiresConnected(()=>{
		main.clearContentSections();
		$("#following").removeClass('hide');
		main.LensPyFetch('/getfollowing',{address:main.ls.address},(data)=>{
			console.log(data)
			$(".following-section").empty();
			for (var fol of data){
				$(".following-section").append('<li>'+fol['handle']+' – '+fol['id']+'</li>');
			}
		});
	})
});

$('#create-profile-btn').click(function(){
	main.clearContentSections();
	$("#create-profile").removeClass('hide');
});

$('#create-profile-send-btn').click(function(){
	main.requiresLogin(()=>{
		let h = $('#create-profile-handle-input').val();
		if (h.length<5){
			main.notification('Handle too short',['Lens handles must have a minimum of 5 characters.']);
		} else if (h.length>31){
			main.notification('Handle too long',['Lens handles must have a maximum of 31 characters.']);
		} else {
			createProfile(h);
		}
	});
});

$('#create-another-profile-btn').click(function(){
	main.clearContentSections();
	$("#create-profile").removeClass('hide');
});

$('#set-default-profile-btn').click(function(){
	buildSetDefaultProfileSection();
});

$('#set-default-profile-send-btn').click(function(){
	main.requiresLogin(()=>{
		let id = $('#set-default-profile-input').val();
		console.log(main.ls.myprofileidlist)
		if (id.length % 2 != 0){
			main.notification('Odd number of charaters!',['Lens profile ids are even in length.']);
		} else if (id.slice(0,2)!='0x'){
			main.notification('Doesn\'t start with 0x',['Lens profile ids start with a 0x.']);
		}  else if (!main.ls.myprofileidlist.includes(id)){
			main.notification('Not your profile!',['The Ethereum address you are logged in with does not own the profile with that id.']);
		} else {
			setDefaultProfile(id);
		}
	});
});

$('#create-post-send-btn').click(function(){
	main.requiresLogin(()=>{
		let contentURI = $('#create-post-contentURI-input').val();
		let collectModule = $('#create-post-collectmodule-input').val();
		let referenceModule = $('#create-post-referencemodule-input').val();
		if (contentURI.length==0) main.notification('Content URI field blank',['The content URI:','ipfs://QmPogtffEF3oAbKERsoR4Ky8aTvLgBF5totp5AuF8YN6vl','is being used instead.','* taken from lens docs']);
		// not passing collect/reference modules yet.
		// let the defaults be used as defined in lenspy
		postPublication(contentURI);
	});
});