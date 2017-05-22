#include "task.hpp"
#include "temperature.hpp"
#include <iostream>
#include <wiringPi.h>
#include "ads1115.h"

Temperature::Temperature(int ms) : Task(ms) {
	state = INIT;
	temperature = 0;
}

double Temperature::get_temperature() {
	return temperature;
}

double Temperature::poll_temperature() {
	double ttemp = analogRead(2222);
	//TODO: perform conversion from voltage reading to temperature value
	ttemp = (((ttemp*4.098)/32767.0) - 0.5)*100.0; // temperature in celsius
	ttemp = ttemp*(9.0/5.0) + 32.0;				// convert celsius to fahrenheit
	return ttemp;
}

int Temperature::tick_function() {
	
	/* State transitions */
	switch(state) {
		case INIT:
			state = WAIT;
			break;
		case WAIT:
			state = GT;
			break;
		case GT:
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
		case GT:
			temperature = poll_temperature();
//			std::cout << "Temperature: " << temperature << " F" <<  endl;
			break;
		default:
			break;
	}
}
