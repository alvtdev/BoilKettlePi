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
	double ptemp = analogRead(2223);
	//perform conversion from voltage reading to pressure value
	//double pvol = (ptemp*5.0)/1024.0; // convert to voltage
//	double ppres = (3.0 * (pvol - 0.47)) * 1000000.0; //convert to voltage in pascals
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
			std::cout << "Pressure: " << pres << " Pa" << std::endl;
			break;
		default:
			break;
	}
}
