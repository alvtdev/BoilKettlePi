/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/27/2017
 *****************************************************************************/

#ifndef HEATER_HPP
#define HEATER_HPP

#include "task.hpp"
#include "timer.hpp"
#include "temperature.hpp"
#include <wiringPi.h>

class Heater : public Task {
	public:
		Heater(int ms, Temperature* t, Timer* time);
		int get_timeLeft_seconds();
		int get_boilTime();
		int get_timerSeconds();

	private:
		enum States { INIT, OFF, HEAT, BOIL, MAINTAIN } state;
		int calc_timeLeft();
		double temp;
		int boilTimeSeconds;
		int timerSeconds;
		int timeLeft;
		Temperature* t;
		Timer* time;
		int heatflag;

		virtual int tick_function();
};

#endif
