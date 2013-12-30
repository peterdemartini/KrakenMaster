(function($) {
	$.fn.krakenClock = function(options) {

		var defaults = {
			stop_text : "I'm Awake",
			stop_class : "",
			snooze: true,
			snooze_text : "SNOOZE",
			snooze_class : '',
			snooze_delay : 1, // In Minutes TODO - make better
			time_class : '',
			alarm_time : '06:00', // In Hours:Minutes
			audio_src : '/static/audio/alarm.mp3',
			flow_type : {
				fontRatio : 6
			},
			alarmStopped : function(data){
			},
		}

		var clock = this;

		clock.settings = {}
		clock.intervals = {
			time : false,
			alarm : false,
			alarm_css : false,
		};
		clock.audio;
		clock.audio_loaded = false;
		clock.date;
		clock.orgbk;
		clock.active = false;
		clock.real_alarm_time = '06:00';
		clock.start_time = false;
		clock.end_time = false;
		clock.snooze_count = 0;

		var init = function() {
			clock.settings = $.extend({}, defaults, options);
			
			clock.real_alarm_time = clock.settings.alarm_time;
			
			clock.start_time = Math.round( new Date().getTime() / 1000 );

			initClock();
		}

		//Public Functions
		clock.stop = function() {
			if(clock.intervals.time)
				clearInterval(clock.intervals.time)
			if(clock.intervals.alarm)
				clearInterval(clock.intervals.alarm);
			clock.find('.stop').fadeOut('fast');
			clock.find('.snooze').fadeOut('fast');
			stopAlarm();
			clock.audio.stop();
			clock.end_time = Math.round( new Date().getTime() / 1000 );
		}

		//Private Functions
		var initClock = function() {
			clock.flowtype(clock.settings.flow_type);
			//Initial Clock
			updateClock(true);

			//Set Interval
			clock.intervals.time = setInterval(updateClock, 1000);
		}

		var updateClock = function(init){
			if(typeof init === undefined) init = false;

			if(!(clock && clock.length == 1)) return false;

			clock.date = new Date();

			var hrs = clock.date.getHours(), min = clock.date.getMinutes(), sec = clock.date.getSeconds();

			//Pad zeros when nseeded 
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

			if(init){
				// Update the time display
				clock.html(
					"<div class='time " + clock.settings.time_class + "'>" +
					str +
					'</div>' +
					"<div class='snooze " + clock.settings.snooze_class + "' style='display: none;'>" + 
					clock.settings.snooze_text + 
					"</div>" + 
					"<div class='stop " + clock.settings.stop_class + "' style='display: none;'>" + 
					clock.settings.stop_text + 
					"</div>" 
				);
				
				loadAudio();
				//startAlarm(); // This is for testing
				clock.intervals.alarm = setInterval(setAlarm, 1000);

				clock.find('.snooze').unbind('click');
				clock.find('.snooze').click(function(){
					setSnooze();
				});

				clock.find('.stop').unbind('click');
				clock.find('.stop').click(function(){
					clock.end_time = Math.round( new Date().getTime() / 1000 );
					if(clock.intervals.alarm)
						clearInterval(clock.intervals.alarm);
					clock.find('.stop').fadeOut('fast');
					stopAlarm();
					data = {
						start : clock.start_time,
						end : clock.end_time,
						snooze_count : clock.snooze_count
					}
					clock.settings.alarmStopped(data);
				});

			}else{
				clock.find('.time').text(str);
			}


			return true;
		}

		var loadAudio = function(){
			clock.append('<audio class="audio"></audio>');
			clock.audio = clock.find('.audio');
			clock.audio.attr('src', clock.settings.audio_src);
			clock.audio.attr('loop', true);
			clock.audio_loaded = true;
		}

		var setSnooze = function(){
			stopAlarm();
			clock.snooze_count++;
			var a = clock.real_alarm_time.split(':');
			var hrs = clock.date.getHours();
			var new_min = (parseInt(clock.date.getMinutes()) + parseInt(clock.settings.snooze_delay));
			if(new_min > 60){
				remain = new_min % 60;
				hrs = hrs + ((new_min - remain) / 60);
				new_min = remain;
			}
			new_min = ( new_min < 10 ? "0" : "" ) + new_min;

			hrs = ( hrs < 10 ? "0" : "" ) + hrs;

			clock.real_alarm_time = hrs  + ':' + new_min;
			console.log(clock.real_alarm_time);
		}

		var setAlarm = function(){
			if(clock.active) return false;
			var a = clock.real_alarm_time.split(':'); // Split into [Hours, Minutes]
			var hrs = clock.date.getHours(), min = clock.date.getMinutes(), sec = clock.date.getSeconds();
			//Pad zeros when nseeded 
			min = ( min < 10 ? "0" : "" ) + min;
			hrs = ( hrs < 10 ? "0" : "" ) + hrs;
			c = (hrs + ':' + min);
			if(clock.real_alarm_time === c) startAlarm();
		}

		var startAlarm = function(){
			clock.active = true;
			if(clock.audio_loaded)
				clock.audio.trigger('play');
			clock.orgbk = clock.css('background-color');
			clock.css('background-color', 'rgb(255, 0, 0)');
			
			clock.intervals.alarm_css = setInterval(function(){
				if(clock.css('background-color') !== clock.orgbk)
					clock.css('background-color', clock.orgbk);
				else
					clock.css('background-color', 'rgb(255, 0, 0)');
			}, 1000);

			clock.find('.snooze').fadeIn('fast');
			clock.find('.stop').fadeIn('fast');
		}

		var stopAlarm = function(){
			clock.active = false;
			if(clock.audio_loaded)
				clock.audio.trigger('pause');
			if(clock.intervals.alarm_css)
				clearInterval(clock.intervals.alarm_css);
			clock.find('.snooze').fadeOut('fast');
			clock.css('background-color', clock.orgbk);
			clock.real_alarm_time = clock.settings.alarm_time;
		}

		init();

	}
})(jQuery);
