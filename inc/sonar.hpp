/******************************************************************************
 * Author: Alvin Thai
 * Date  : 5/6/2017
 *****************************************************************************/

#ifndef SONAR_HPP
#define SONAR_HPP

#include "task.hpp"
#include <wiringPi.h> 

#define BK_MAX_HEIGHT_CM 27.94

class Sonar : public Task {
	public:
		Sonar(int ms);
		double get_distance();
	private:
		enum States { INIT, WAIT, PING } state;
		
		//variables
		double distCM;
		volatile long startTimeUsec;
		volatile long endTimeUsec;
		int trigger;
		int echo;
		long travelTimeUsec;
		long now;

		//functions
		double poll_distance();
		double calc_distance(volatile long travelTimeUsec);
		virtual int tick_function();
};

#endif
