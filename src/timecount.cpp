#include "task.hpp"
#include "timecount.hpp"
#include <iostream>

timecount::timecount(int ms) : Task(1000) {
	state = INIT;
	hours = 0;
	minutes = 0;
	seconds = -1;
}

void timecount::start_timer() {
	hours = 0;
	minutes = 0;
	seconds = 0;
}

void timecount::stop_timer() {
	seconds = -1;
}

int timecount::get_hours() { 
	return hours;
}

int timecount::get_minutes() { 
	return minutes;
}

int timecount::get_seconds() { 
	return seconds;
}
int timecount::tick_function() {
	
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
			std::cout << seconds++ << std::endl;
			//seconds++;
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
