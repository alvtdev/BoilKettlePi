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

		void start_timer();
		void stop_timer();

		int get_hours();
		int get_minutes();
		int get_seconds();

	private:
		enum States { INIT, OFF, ON } state;
		int hours;
		int minutes;
		int seconds;

		virtual int tick_function();
};

#endif
