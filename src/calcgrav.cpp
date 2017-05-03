/******************************************************************************
 * Author: Alvin Thai
 * Date  : 5/2/2017
 * Calcgrav is a state machine that obtains pressure and depth readings from
 * the pressure and depth state machines, then uses those values to calculate
 * the specific gravity of the fluid inside the boil kettle
 *****************************************************************************/

#include "task.hpp"
#include "ping.hpp"
#include "calcgrav.hpp"
#include <iostream>

//TODO: modify constructor to include depth(sonar) SM 
//			change h assignmend in calc_specific_gravity to call
//				get_depth function from depth SM
//			proper transitions between WAIT and GRAV_BEGIN/END
//				^do this after implementing timing

Calcgrav::Calcgrav(int ms, Pressure* pres) : Task(ms) {
	this->pres = pres; 
	specGravBegin = 0;
	specGravEnd = 0;
}

double Calcgrav::get_specGravBegin() {
	return specGravBegin;
}

double Calcgrav::get_specGravEnd() {
	return specGravEnd;
}

double Calcgrav::calc_specific_gravity() {
	double g = 9.81; // m per s^2
	double p = pres->get_pressure(); 
	double h = 0; 

	return p/(g*h);
}

int Calcgrav::tick_function() {

	/* State transitions */
	switch(state) {
		case INIT:
			state = WAIT;
			break;
		case WAIT:
			/*transition to GRAV_BEGIN vs GRAV_END depends on time
			 * GRAV_BEGIN occurs before boiling, and saves result to specGravBegin
			 * GRAV_END occurs after boiling, and saves result to specGravEnd
			 * TODO: properly implement this (done when timer is set)
			 */
			state = GRAV_BEGIN;
			break;
		case GRAV_BEGIN:
			state = WAIT;
			break;
		case GRAV_END:
			break;
		default:
			break;
	}

	/* State actions */
	switch(state) {
		case INIT:
			break;
		case WAIT:
			break;
		case GRAV_BEGIN:
			specGravBegin = calc_specific_gravity();
			break;
		case GRAV_END:
			specGravEnd = calc_specific_gravity();
			break;
		default:
			break;
	}

	return 0;
}
