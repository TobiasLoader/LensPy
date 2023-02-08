
$(document).ready(()=>{
	$('#profile-search').removeClass('hide');
	if (profiles.length===0){
		$('#profile-search h2.search-section-title').html('Ooops');
		$("#profile-search .search-results").html('<p>Sorry, there are no results for this handle.</p>');
	} else {
		let profilelist = $('<div></div>');
		for (var p of profiles){
			let searchresult = $('<div class="search-result"></div>');
			let searchresulttitle = $('<div class="search-result-title"></div>')
			searchresulttitle.append('<h3><a href="'+window.location.origin+'/'+p['handle']+'">'+p['handle']+'</a></h3>');
			searchresulttitle.append('<p>'+p['id']+'</p>');
			searchresult.append(searchresulttitle);
			if (p['bio']!=null) searchresult.append('<p class="search-result-bio">'+p['bio']+'</p>');
			profilelist.append(searchresult);
		}
		$('#profile-search h2.search-section-title').html('Search Results: '+handle);
		$("#profile-search .search-results").html(profilelist);
	}
	$('#profile-search').removeClass('hide');
});