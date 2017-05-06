#include "task.hpp"
#include "temperature.hpp"
#include <iostream>
#include <wiringPi.h>
#include "ads1115.h"

Temperature::Temperature(int ms) : Task(ms) {
	pres = 0;
}

double Temperature::get_temperature() {
	return temperature;
}

double Temperature::poll_temperature() {
	double ttemp = analogRead(2222);
	//TODO: perform conversion from voltage reading to temperature value
	return ttemp;
}

int Temperature::tick_function() {
	
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
		default:
			state = INIT;
			break;
	}

	/* State actions */
	switch(state) {
		case INIT:
			break;
		case WAIT:
			//test output
			break;
		case GP:
			temperature = poll_temperature();
			std::cout << "Temperature: " << pres << std::endl;
			break;
		default:
			break;
	}
}
