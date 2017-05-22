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
#include "sonar.hpp"
#include "calcgrav.hpp"
#include "output.hpp"
#include "timer.hpp"
#include "temperature.hpp"
#include "timer.h"
#include <wiringPi.h>
#include "ads1115.h"

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

	//initialize adc
	ads1115Setup(2222, 0x48);

	//T->add_task(new Ping(1000));
	Timer* time = new Timer(1000); 
	T->add_task(time); 

	//T->add_task(new Temperature(1000));
	Temperature* t = new Temperature(500);
	T->add_task(t); 

	//T->add_task(new Pressure(1000));
	Pressure* p = new Pressure(500);
	T->add_task(p);
	
	//T->add_task(new Sonar(1000));
	Sonar* s = new Sonar(500);
	T->add_task(s);

	//T->add_task(new Calcgrav(500, p, s));
	Calcgrav* cg = new Calcgrav(500, p, s);
	T->add_task(cg);

	//T->add_task(new Heater(250, t, time));
	Heater* h = new Heater(250, t, time);
	T->add_task(h);

	Output* o = new Output(100, t, p, s, cg, h);
	T->add_task(o);


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
