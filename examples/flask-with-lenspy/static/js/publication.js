import * as script from "./script.js";

$(document).ready(()=>{
	if (found){
		console.log(pub)
		$("#view-publication #publication-title").html(pub.metadata.name);
		$("#view-publication #publication-txtcontent").html(pub.metadata.content);
		$("#view-publication h2#profile-name").html('<a href='+window.location.origin+'/'+pub.profile.handle+'>'+pub.profile.handle+'</a>');
		for (var attr of pub.metadata.attributes){
			$('#view-publication #publication-bottomrow').append('<p class="pub-attr subtitle">'+attr['value']+'</p>')
		}
		var hasonevid = false;
		for (var m of pub.metadata.media){
			if (!hasonevid && m.original.mimeType=='video/mp4'){
				$('#view-publication #publication-vidcontent').append('<video controls="" autoplay="" name="media" class="pub-video"><source src="'+m.original.url+'" type="video/mp4"></video>');
				hasonevid = true;
			} else if (m.original.mimeType=='image/jpeg' || m.original.mimeType=='image/png'){
				$('#view-publication #publication-vidcontent').append('<img src="'+m.original.url+'" type="'+m.original.mimeType+'" class="pub-img">')
			}
		}
		// profile
		$("#view-publication p#profile-id").html(pub.profile.id);
		$("#view-publication #profile-subtitle").html(pub.profile.bio);
		$("#view-publication").removeClass('hide');
		$("#profile-row").removeClass('hide');
		$("#publication-right").removeClass('hide');
	} else {
		$("#no-publication-found").removeClass('hide');
	}
});

$('#collect-publication').click(()=>{
	script.notification('Collect', ['TODO: collect this publication']);
});

$('#mirror-publication').click(()=>{
	script.notification('Mirror', ['TODO: mirror this publication']);
});