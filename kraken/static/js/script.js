var clock;

$(document).ready(function(){
	init();
});

function init(){
	initClock();
}

function initClock(){
	clock = $('#clock');
	clock.flowtype({
		fontRatio: 6
	});
	setInterval(updateClock, 1000);
}

function updateClock(){
	if(!(clock && clock.length == 1)) return false;

	var d = new Date();

	var hrs = d.getHours(), min = d.getMinutes(), sec = d.getSeconds();

	//Pad zeros when needed 
	min = ( min < 10 ? "0" : "" ) + min;
	sec = ( sec < 10 ? "0" : "" ) + sec;

	//Determine Hours and Minutes
	var tDay = ( hrs < 12 ) ? "AM" : "PM";

	//Convert Military Time
	hrs = ( hrs > 12 ) ? hrs - 12 : hrs;

	// Convert an hours component of "0" to "12"
	hrs = ( hrs == 0 ) ? 12 : hrs;

	// Compose the string for display
	var str = hrs + ":" + min + ":" + sec + " " + tDay;

	// Update the time display
	clock.text(str);

	return true;
}
