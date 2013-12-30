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
				$('#clock').append(res);
			})
			.error(function(err){
				console.log(err);
			});
		}
	});
}
