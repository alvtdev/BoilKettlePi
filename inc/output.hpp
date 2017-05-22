/******************************************************************************
 * Author: Alvin Thai
 * Date  : 5/21/2017
 * 	
 *	Output is a state machine that polls all other state machines for data and
 * outputs them accordingly.
 *****************************************************************************/

#ifndef OUTPUT_HPP
#define OUTPUT_HPP
#include "temperature.hpp"
#include "pressure.hpp"
#include "sonar.hpp"
#include "calcgrav.hpp"
#include "heater.hpp"

#include "task.hpp"

class Output : public Task {
	public:
		Output(int ms, Temperature* t, Pressure* p, Sonar* s, Calcgrav* cg, Heater* h);
	private:
		Temperature* t;
		Pressure* p;
		Sonar* s;
		Calcgrav* cg;
		Heater* h;

		enum States { INIT, POLL, OUT } state;
		double temperature; 	//from temperature SM - get_Temp()
		double pressure;			//from pressure SM		- get_Pressure()
		double dist;					//from sonar SM				- get_Distance()
		double specGravBegin; //from calcgrav SM		- get_specGravBegin()
		int timeLeft;					//from Heater SM			- get_timeLeft_seconds()

		int pollCount; 				//used to suppress output to once per second 
		int pollCountMax;			//or as close as once per second as possible.

		void poll_Data();
		void output_Data();
		void output_to_file();

		virtual int tick_function();
};

#endif
