/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/27/2017
 *****************************************************************************/

#ifndef HEATER_HPP
#define HEATER_HPP

#include "task.hpp"
#include "sonar.hpp"
#include "timer.hpp"
#include "temperature.hpp"
#include <wiringPi.h>

class Heater : public Task {
	public:
		Heater(int ms, Temperature* t, Timer* time, Sonar* s, int minutes);
		int get_timeLeft_seconds();
		int get_boilTime();
		int get_timerSeconds();
		int get_fullStatus();

	private:
		enum States { INIT, OFF, HEAT, BOIL, MAINTAIN } state;
		int calc_timeLeft();
		void init_boilTime(int hrs, int min, int sec); //helper function for testing hard-coded boiltimes
		void create_boilText();
		double temp;
		int boilTimeHrs;
		int boilTimeMins;
		int boilTimeSeconds;
		int timerSeconds;
		int timeLeft;
		Sonar* dist;
		Temperature* t;
		Timer* time;
		int heatflag;
		int fullflag;

		virtual int tick_function();
};

#endif
