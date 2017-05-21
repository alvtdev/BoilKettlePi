/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/27/2017
 *****************************************************************************/

#ifndef HEATER_HPP
#define HEATER_HPP

#include "task.hpp"
#include "timecount.hpp"
#include "temperature.hpp"
#include <wiringPi.h>

class Heater : public Task {
	public:
		Heater(int ms, Temperature* t, timecount* time);

	private:
		enum States { INIT, OFF, HEAT, BOIL, MAINTAIN } state;
		double temp;
		int boilTimeSeconds;
		int timerSeconds;
		Temperature* t;
		timecount* time;
		int heatflag;

		virtual int tick_function();
};

#endif
