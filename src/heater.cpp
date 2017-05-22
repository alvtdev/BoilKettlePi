/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/27/2017
 * Modified on 5/8 by Alvin Thai
 *****************************************************************************/

#include "task.hpp"
#include "heater.hpp"
#include <wiringPi.h>
#include <iostream>

Heater::Heater(int ms, Temperature* t, Timer* time) : Task(ms) {
	pinMode(6, OUTPUT);
	digitalWrite(6, LOW);
	state = INIT;
	this->t = t;	
	this->time = time;
	temp = t->get_temperature();
	heatflag = -1;
	boilTimeSeconds = 30;
	timerSeconds = 0;
	timeLeft = -1;
	printcount = 0;
}

int Heater::get_timeLeft_seconds() {
	return timeLeft;
}

int Heater::calc_timeLeft() {
	timeLeft = boilTimeSeconds - timerSeconds;
	return timeLeft;
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
			else {
				state = HEAT;
			}
			break;
		case BOIL:
			if (calc_timeLeft() <= 0) { 
				time->stop_timer();
				timeLeft = -1;
				std::cout << "state = MAINTAIN" << std::endl;
				state = MAINTAIN;
			}
			else {
				state = BOIL;
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
			printcount++; //used to suppress output
			if (printcount >= 4) {
//				std::cout << "Time Left: " << (boilTimeSeconds - timerSeconds) << std::endl;
				printcount = 0;
			}
			break;
		case MAINTAIN:
			if (temp <= 75.0) { 
				//std::cout << "Heater: ON" << std::endl;
				digitalWrite(6, HIGH);
				temp = t->get_temperature();
			}
			else {
				//std::cout << "Heater: OFF" << std::endl;
				digitalWrite(6, LOW);
				temp = t->get_temperature();
			}
			break;
		default:
			break;
	}

	return 0;
}
