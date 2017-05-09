/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/27/2017
 *****************************************************************************/

#ifndef HEATER_HPP
#define HEATER_HPP

#include "task.hpp"
#include "temperature.hpp"
#include <wiringPi.h>

class Heater : public Task {
	public:
		Heater(int ms, Temperature* t);
	private:
		enum States { INIT, ON, OFF } state;
		double temp;
		Temperature* t;

		virtual int tick_function();
};

#endif
