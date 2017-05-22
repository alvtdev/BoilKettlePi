#include "task.hpp"
#include "timer.hpp"
#include <iostream>

Timer::Timer(int ms) : Task(1000) {
	state = INIT;
	hours = 0;
	minutes = 0;
	seconds = -1;
}

void Timer::start_timer() {
	hours = 0;
	minutes = 0;
	seconds = 0;
}

void Timer::stop_timer() {
	seconds = -1;
}

int Timer::get_hours() { 
	return hours;
}

int Timer::get_minutes() { 
	return minutes;
}

int Timer::get_seconds() { 
	return seconds;
}
int Timer::tick_function() {
	
	/* State transitions */
	switch(state) {
		case INIT:
			state = OFF;
			break;
		case OFF:
			if (seconds == -1) {
				state = OFF;
			}
			else {
				state = ON;
			}
			break;
		case ON:
			if (seconds != -1) {
				state = ON;
			}
			else {
				state = OFF;
			}
			break;
		default:
			state = INIT;
			break;
	};

	/* State actions */
	switch(state) {
		case INIT:
			break;
		case OFF:
			break;
		case ON:
			//std::cout << seconds++ << std::endl;
			seconds++;
			if ((seconds % 60) == 0) {
				minutes++;
			}
			if ((minutes % 60) == 0) {
				hours++;
			}
			break;
		default:
			break;
	};

	return 0;
}
