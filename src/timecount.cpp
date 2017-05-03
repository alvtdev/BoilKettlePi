#include "task.hpp"
#include "timecount.hpp"
#include <iostream>

timecount::timecount(int ms) : Task(ms) {
	currtime = 0;
}

int timecount::get_currtime() { 
	return currtime;
}

int timecount::tick_function() {
	
	/* State transitions */
	switch(state) {
		case INIT:
			state = OFF;
			break;
		case OFF:
			state = ON;
			break;
		case ON:
			state = OFF;
			break;
		default:
			state = INIT;
			break;
	};

	/* State actions */
	switch(state) {
		case INIT:
			currtime = 0;
			break;
		case OFF:
			break;
		case ON:
			std::cout << currtime++ << std::endl;
			break;
		default:
			break;
	};

	return 0;
}
