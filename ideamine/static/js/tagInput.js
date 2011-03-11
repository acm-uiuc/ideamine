// sets up a textbox list for inputing tags
// requires an input element with id='id_tags_field'
$(function() { // onload
	// change space delimited to comma delimited
	var existingTags = $("input#id_tags_field").val();
	$("input#id_tags_field").val(existingTags.replace(/ /g, ','));
	
	// sets up textbox list
	var t = new $.TextboxList('input#id_tags_field', {
	    unique: true,
	    plugins: {'autocomplete': {
	    	minLength: 2,
	    	queryRemote: true,
	    	remote: {url: '/tags/suggest'}
	    }}
	});
	
	// reverse the delimitation: comma to space
	$("input#ideaSubmit").click(function() {
		var existingTags = $("input#id_tags_field").val();
		$("input#id_tags_field").val(existingTags.replace(/\b +\b/g, '_'));
		existingTags = $("input#id_tags_field").val();
		$("input#id_tags_field").val(existingTags.replace(/,/g, ' '));
	});
});