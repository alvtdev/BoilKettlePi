/******************************************************************************
 * Author: Alvin Thai
 * Date  : 4/27/2017
 * timecout is a state machine that constantly counts upward upon starting
 * execution of a task
 *****************************************************************************/

#ifndef TIMECOUNT_HPP
#define TIMECOUNT_HPP

#include "task.hpp"

class timecount : public Task {
	public:
		timecount(int ms);
		int get_currtime();
	private:
		enum States { INIT, OFF, ON } state;
		int currtime;

		virtual int tick_function();
};

#endif
