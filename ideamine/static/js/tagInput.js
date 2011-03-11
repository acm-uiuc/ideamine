$(function() { // onload
	// sets up a textbox list for inputing tags
	// requires an input element with id='id_tags'
	var t = new $.TextboxList('input#id_tags', {
	    bitsOptions: {editable: {addKeys: [32]}}, // 32 = space key code
	    unique: true,
	    plugins: {autocomplete: {
	    	minLength: 2,
	    	queryRemote: true,
	    	remote: {url: 'URL_GOES_HERE.php'} // REPLACE URL WITH A VALID ONE
	    }}
	});
	
	// expects existing input to be placed in the input box (space delimited)
	if ($("input#id_tags").text()) {
		var existingTags = $("input#id_tags").text().split(' ');
		for (var i = 0; i < existingTags.length; i++) {
		    t.add(existingTags[i]);
		}
	}
});