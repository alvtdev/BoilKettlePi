#include "task.hpp"
#include "pressure.hpp"
#include <iostream>

Pressure::Pressure(int ms) : Task(ms) {
	pres = 0;
}

double get_pressure() {
	return pres;
}

int Pressure::tick_function() {
	
	/* State transitions */
	switch(state) {
		case INIT:
			state = WAIT;
			break;
		case WAIT:
			state = GP;
			break;
		case GP:
			state = WAIT;
			break;
		default
			state = INIT;
			break;
	}

	/* State actions */
	switch(state) {
		case INIT:
			break;
		case WAIT:
			//test output
			std::cout << "Current State: Wait" << std::endl;
			break;
		case GP:
			std::cout << "Getting Pressure" << std::endl;
			//TODO: Actually get pressure readings
			break;
		default
			break;
	}
}
