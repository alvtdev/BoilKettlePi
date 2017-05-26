/******************************************************************************
 * Author: Alvin Thai
 * Date  : 5/21/2017
 *
 * 	Output is a state machine that polls all other state machines for data and
 * outputs them accordingly
 *****************************************************************************/

#include "task.hpp"
#include "output.hpp"
#include <iostream>
#include <fstream>

Output::Output(int ms, Temperature* t, Pressure* p, Sonar* s, 
	Calcgrav* cg, Heater* h) : Task(ms) {
	this->t = t;
	this->p = p;
	this->s = s;
	this->cg = cg;
	this->h = h;
	pollCountMax = (1000/ms);
	outputTimeHours = 0;
	outputTimeMinutes = 0;
	outputTimeSeconds = 0;
}

void Output::poll_Data() {
	temperature = t->get_temperature();
	pressure = p->get_pressure();
	dist = s->get_distance();
	specGravBegin = cg->get_specGravBegin();
	timeLeft = h->get_timeLeft_seconds();
}

void Output::calc_outputTimes() {
	unsigned int tempTimeLeft = h->get_timeLeft_seconds();

	if (tempTimeLeft > 360) {
		outputTimeHours = (tempTimeLeft / 360);
		tempTimeLeft -= (outputTimeHours * 360);
	}
	else {
		outputTimeHours = 0;
	}

	if (tempTimeLeft > 60) {
		outputTimeMinutes = (tempTimeLeft / 60);
		tempTimeLeft -= (outputTimeMinutes * 60);
	}
	else {
		outputTimeMinutes = 0;
	}

	outputTimeSeconds = tempTimeLeft;
}

void Output::output_Data() {
	if (timeLeft > 0) {
		/*
		std::cout << "Total Boil Time: " << h->get_boilTime() << " s \n";
		std::cout << "Timer Time: " << h->get_timerSeconds() << " s \n";
		*/
		std::cout << "Boil Time Left: " << outputTimeHours << " hrs, " 
			<< outputTimeMinutes << " min, " << outputTimeSeconds << " s" << std::endl;
	}
	else if (timeLeft == 0) {
		std::cout << "Boil Status: Finished." << std::endl;
	} 
	else if (timeLeft < 0) {
		//std::cout << "Boil Status: Waiting to start." << std::endl;
	}
	std::cout << "Temperature: " << temperature << " F" << std::endl;
	std::cout << "Pressure: " << pressure << " Pa" << std::endl;
	std::cout << "Distance: " << dist << " cm" << std::endl;
	std::cout << "Density: " << specGravBegin << " g/cm^3" << std::endl;
	std::cout << std::endl;
} 

void Output::output_to_file() {
	ofstream outFile("output.txt");
	if (outFile.is_open()) {
		if (timeLeft > 0) {
			outFile << "Boil Time Left: " << outputTimeHours << " hrs, "  
				<< outputTimeMinutes << " min, " << outputTimeSeconds << " s \n";
		}
		else if (timeLeft == 0) {
			outFile << "Boil Status: Finished \n";
		} 
		else if (timeLeft == -1) {
			outFile << "Boil Status: Waiting to start.\n";
		}
		else if (timeLeft < -5) {
			outFile << "Boil Status: Finished.\n";
		}
		outFile << "Temperature: " << temperature << " F \n";
		outFile << "Pressure: " << pressure << " Pa \n";
		outFile << "Distance: " << dist << " cm \n";
		outFile << "Density: " << specGravBegin << " g/cm^3 \n";
	}
	else {
		std::cout << "Error opening output.txt" << std::endl;
	}
}

int Output::tick_function() {

	/* State transitions */
	switch(state) {
		case INIT:
			state = POLL;
			break;
		case POLL:
			if (pollCount >= pollCountMax-1) {
				pollCount = 0;
				state = OUT;
			}
			else {
				state = POLL;
			}
			break;
		case OUT:
			state = POLL;
			break;
		default: 
			state = INIT;
			break;
	}

	/* State actions */
	switch(state) {
		case INIT:
			break;
		case POLL:
			poll_Data();
			pollCount++;
			break;
		case OUT:
			calc_outputTimes();
			output_Data();
			output_to_file();
			break;
		default:
			break;
	}
	return 0;
}
