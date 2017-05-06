/******************************************************************************
 * Author: Alvin Thai
 * Date  : 4/30/2017
 * State machine that polls for temperature
 *****************************************************************************/

#ifndef TEMPERATURE_HPP
#define TEMPERATURE_HPP

#include "task.hpp"
#include <wiringPi.h>

class Temperature : public Task {
	public: 
		Temperature(int ms);
		double get_temperature();

	private:
		enum States {INIT, WAIT, GT} state; //GT = get temperature
		double temperature; //stores temperature value from reading
		double poll_temperature();

		virtual int tick_function();

}; 

#endif
