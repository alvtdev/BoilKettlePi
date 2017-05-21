/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/27/2017
 * Modified on 5/8 by Alvin Thai
 *****************************************************************************/

#include "task.hpp"
#include "heater.hpp"
#include <wiringPi.h>
#include <iostream>

Heater::Heater(int ms, Temperature* t, timecount* time) : Task(ms) {
	pinMode(6, OUTPUT);
	digitalWrite(6, LOW);
	state = INIT;
	this->t = t;	
	this->time = time;
	temp = t->get_temperature();
	heatflag = -1;
	boilTimeSeconds = 30;
	timerSeconds = 0;
}

int Heater::tick_function() {

	/* State transitions */
	switch(state) {
		case INIT:
			state = OFF;
			break;
		case OFF:
			if (heatflag != -1) {
				state = HEAT;
				std::cout << "state = HEAT" << std::endl;
			} 
			break;
		case HEAT:
			if (temp >= 75.0) {
				time->start_timer();
				state = BOIL;
				std::cout << "state = BOIL" << std::endl;
			}
			break;
		case BOIL:
			if (boilTimeSeconds - timerSeconds <= 0) { 
				time->stop_timer();
				std::cout << "state = MAINTAIN" << std::endl;
				state = MAINTAIN;
			}
			break;
		case MAINTAIN:
			break;
		default: 
			state = INIT;
			break;
	}

	/* State actions */
	switch(state) {
		case INIT:
			break;
		case OFF:
			digitalWrite(6, LOW);
			heatflag = 1;
			break;
		case HEAT:
			digitalWrite(6, HIGH);
			temp = t->get_temperature();
			break;
		case BOIL:
			timerSeconds = time->get_seconds();
			std::cout << "Time Left: " << (boilTimeSeconds - timerSeconds) << std::endl;
		case MAINTAIN:
			if (temp <= 75.0) { 
				std::cout << "Heater: ON" << std::endl;
				digitalWrite(6, HIGH);
				temp = t->get_temperature();
			}
			else {
				std::cout << "Heater: OFF" << std::endl;
				digitalWrite(6, LOW);
				temp = t->get_temperature();
			}
			break;
		default:
			break;
	}

	return 0;
}
