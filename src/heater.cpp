/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/27/2017
 * Modified on 5/8 by Alvin Thai
 *****************************************************************************/

#include "task.hpp"
#include "heater.hpp"
#include <wiringPi.h>
#include <iostream>

Heater::Heater(int ms, Temperature* t) : Task(ms) {
	pinMode(6, OUTPUT);
	digitalWrite(6, LOW);
	state = INIT;
	this->t = t;	
	temp = t->get_temperature();
}

int Heater::tick_function() {

	/* State transitions */
	switch(state) {
		case INIT:
			if (temp <= 75.0) { 
				std::cout << "Heater: ON" << std::endl;
				state = ON;
			}
			else {
				std::cout << "Heater: OFF" << std::endl;
				state = OFF;
			}
			break;
		case ON:
			if (temp > 75.0) {
				std::cout << "Heater: OFF" << std::endl;
				state = OFF;
			}
			break;
		case OFF:
			if (temp <= 75.0) { 
				std::cout << "Heater: ON" << std::endl;
				state = ON;
			}
			break;
		default: 
			state = INIT;
			break;
	}

	/* State actions */
	switch(state) {
		case INIT:
			digitalWrite(6, LOW);
			temp = t->get_temperature();
			break;
		case ON:
			digitalWrite(6, HIGH);
			temp = t->get_temperature();
			break;
		case OFF:
			digitalWrite(6, LOW);
			temp = t->get_temperature();
			break;
		default:
			break;
	}

	return 0;
}
