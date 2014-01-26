$(document).ready(function(){
	init();
});

function init(){
	$('#clock').krakenClock({
		snooze_class : 'btn btn-default',
		stop_class : 'btn btn-default',
		alarmStopped : function(data){
			console.log(data);
			$.post('/grades/create/', data)
			.success(function(res){
				$('#clock').prepend('<div class="grade-res">' + res + "</div>");
				setTimeout(function(){
					$('#clock .grade-res').remove();
				}, 100000);
			})
			.error(function(err){
				console.log(err);
			});
		},
		alarmStarted : function(){
			return false; //TODO
			$.post('/grades/create/', data)
			.success(function(res){
				$('#clock').append(res);
			})
			.error(function(err){
				console.log(err);
			});
		}
	});
}
