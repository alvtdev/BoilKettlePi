/******************************************************************************
 * Author: Alvin Thai
 * Date  : 4/30/2017
 *****************************************************************************/

#ifndef PRESSURE_HPP
#define PRESSURE_HPP

#include "task.hpp"

class Pressure : public Task {
	public: 
		Pressure(int ms);

	private:
		enum States {INIT, WAIT, GP} state; //GP = get pressure
		double pres; //stores pressure value from reading

		virtual int tick_function();

}; 

#endif
