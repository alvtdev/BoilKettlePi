#include "task.hpp"
#include "pressure.hpp"
#include <iostream>
#include <wiringPi.h>
#include "ads1115.h"

Pressure::Pressure(int ms) : Task(ms) {
	state = INIT;
	pres = 0;
}

double Pressure::get_pressure() {
	return pres;
}

double Pressure::poll_pressure() {
	double ptemp = analogRead(2222);
	//TODO: perform conversion from voltage reading to pressure value
	return ptemp;
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
			pres = poll_pressure();
			std::cout << "Pressure: " << pres << endl;
			break;
		default:
			break;
	}
}
