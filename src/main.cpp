/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/26/2017
 *
 *   This main file is meant to be as minimal as possible. All state machine 
 * definitions can be found in their appropriate header and source files. 
 * Initialization of a state machine is handled within the constructor of 
 * each class.
 *****************************************************************************/

#include "task.hpp"
#include "ping.hpp"
#include "heater.hpp"
#include "pump.hpp"
#include "pressure.hpp"
#include "timecount.hpp"
#include "timer.h"

int main(void) {
	extern int timer_flag;
	TaskList * T = new TaskList();

	if(wiringPiSetup())
		return 1;

	/* Add new tasks here */
	/* T->add_task(new Task(period_ms)); */

	/* For tasks that rely on other tasks:
	 *
	 * Pressure p = new Pressure(period); 
	 * T->add_task(p); 
	 * T->add_task(new CalcGrav(period, &p)) ; 
	 */


	T->add_task(new Ping(1000));
	//T->add_task(new timecount(1000)); 
	T->add_task(new Heater(500));
	T->add_task(new Pump(3000));

//	Pressure p* = new Pressure(1000);
	T->add_task(new Pressure(1000));


	if(timer_init(T->get_period_ms()))
		return 1;

	for(;;) {
		T->tick();
		while(!timer_flag)
			;
		timer_flag = 0;
	}

	return 1;
}
