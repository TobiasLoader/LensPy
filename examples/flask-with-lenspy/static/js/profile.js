import * as main from "./main.js";

$(document).ready(()=>{
	if (profile.found){
		$("#view-profile h2#profile-name").html(profile.handle);
		$("#view-profile p#profile-id").html(profile.profileId);
		$("#view-profile #profile-subtitle").html(profile.bio);
		$("#view-profile").removeClass('hide');
		main.LensPyFetch('/getpublications',{profileId:profile.profileId},(data)=>{
			let publications = data['publications']['items'];
			console.log(publications)
			if (publications.length>0){
				$("#publication-list").empty();
				for (var p of publications){
					let pubresult = $('<div class="pub-result"></div>');
					let pubresulttoprow = $('<div class="pub-result-toprow"></div>')
					let pubresultcontentrow = $('<div class="pub-result-contentrow"></div>')
					let pubresultcontentblock = $('<div class="pub-result-contentblock"></div>')
					let pubresultbottomrow = $('<div class="pub-result-bottomrow"></div>')
					let pubresulttitle = $('<div class="pub-result-title"></div>')
					pubresulttitle.append('<p class="pub-result-typename subtitle">'+p['__typename']+'</p>');
					let name = p['metadata']['name'];
					if (name.length>30){
						name = name.substring(0,30);
						name += '...';
					}
					pubresulttitle.append('<h3><a href="'+window.location.origin+'/publication/'+p['id']+'">'+name+'</a></h3>');
					pubresulttitle.append('<p class="subtitle">'+p['id']+'</p>');
					pubresulttoprow.append(pubresulttitle);
					pubresulttoprow.append('<p class="pub-result-createdat">'+p['createdAt'].substring(0, 10)+'</p>');
					pubresult.append(pubresulttoprow);
					// if (p['metadata']['description']!=null) pubresultcontentblock.append('<p class="pub-result-desc">'+p['metadata']['description']+'</p>');
					if (p['metadata']['content']!=null) pubresultcontentblock.append('<p class="pub-result-content">'+p['metadata']['content']+'</p>');
					pubresultcontentrow.append(pubresultcontentblock);
					pubresultcontentrow.append('<p class="pub-result-appId subtitle">'+p['appId']+'</p>');
					pubresult.append(pubresultcontentrow);
					for (var attr of p['metadata']['attributes']){
						pubresultbottomrow.append('<p class="pub-result-attr subtitle">'+attr['value']+'</p>')
					}
					pubresult.append(pubresultbottomrow);
					$("#publication-list").append(pubresult);
				}
				$("#publication-list").removeClass('hide');
			} else {
				$("#no-publications-found").removeClass('hide');
			}
		});
	} else {
		$("#no-profile-found").removeClass('hide');
	}
});

$('#follow-profile').click(()=>{
	main.requiresLogin(()=>{
		main.LensPyFetch('/getfollow',{address:main.ls.address,profileId:profile.profileId},(data)=>{
			main.LensPySignThenBroadcast(data['createFollowTypedData']);
		});
	})
});

$('#unfollow-profile').click(()=>{
	main.requiresLogin(()=>{
		main.LensPyFetch('/getunfollow',{address:main.ls.address,profileId:profile.profileId},(data)=>{
			main.LensPySignThenBroadcast(data['createUnfollowTypedData']);
		});
	})
});