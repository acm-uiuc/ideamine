$(function() { // onload
	// sets up a textbox list for inputing tags
	// requires an input element with id='id_tags_field'
	var t = new $.TextboxList('input#id_tags_field', {
	    bitsOptions: {editable: {addKeys: [32]}}, // 32 = space key code
	    unique: true,
	    plugins: {autocomplete: {
	    	minLength: 2,
	    	queryRemote: true,
	    	remote: {url: '/tags/suggest'}
	    }}
	});
	
	// expects existing input to be placed in the input box (space delimited)
	if ($("input#id_tags_field").text()) {
		var existingTags = $("input#id_tags_field").text().split(' ');
		for (var i = 0; i < existingTags.length; i++) {
		    t.add(existingTags[i]);
		}
	}
	
	$("button#ideaSubmit").click(function() {
		
	});
});