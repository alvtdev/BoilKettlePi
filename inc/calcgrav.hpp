/******************************************************************************
 * Author: Alvin Thai
 * Date  : 5/2/2017
 * Calcgrav is a state machine that obtains pressure and depth readings from
 * the pressure and depth state machines, then uses those values to calculate
 * the specific gravity of the fluid inside the boil kettle
 *****************************************************************************/

#ifndef CALCGRAV_HPP
#define CALCGRAV_HPP

#include "task.hpp"


//TODO: modify class to include depth SM in constructor and as private member
class Calcgrav : public Task {

	public:
		Calcgrav(int ms, Pressure* pres);
		double get_specGravBegin();
		double get_specGravEnd();

	private:
		Pressure* pres;
		//other class pointers needed: depth
		double specGravBegin;
		double specGravEnd;
		enum States { INIT, WAIT, GRAV_BEGIN, GRAV_END } state;

		double calc_specific_gravity();

		virtual int tick_function();
};

#endif
