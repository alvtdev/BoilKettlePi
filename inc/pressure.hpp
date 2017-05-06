/******************************************************************************
 * Author: Alvin Thai
 * Date  : 4/30/2017
 *****************************************************************************/

#ifndef PRESSURE_HPP
#define PRESSURE_HPP

#include "task.hpp"
#include <wiringPi.h>

class Pressure : public Task {
	public: 
		Pressure(int ms);
		double get_pressure();

	private:
		enum States {INIT, WAIT, GP} state; //GP = get pressure
		double pres; //stores pressure value from reading
		double poll_pressure();

		virtual int tick_function();

}; 

#endif
