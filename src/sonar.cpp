/******************************************************************************
 * Author: Alvin Thai
 * Date  : 5/6/2017
 *
 *  State machine for HC-SR04 sonar sensor
 *****************************************************************************/

#include "task.hpp"
#include "sonar.hpp"
#include <iostream>
#include <wiringPi.h>

//trig = GPIO 18 (1)
//echo = GPIO 17 (0)
Sonar::Sonar(int ms) : Task(ms) {
	state = INIT;
	distCM = 0;
	trigger = 1;
	echo = 0;
	pinMode(trigger, OUTPUT);
	pinMode(echo, INPUT);
	digitalWrite(trigger, LOW);
	delay(500);
}

double Sonar::get_distance() {
	return distCM;
}

double Sonar::poll_distance() {
	delay(10);

	digitalWrite(trigger, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigger, LOW);

	now = micros();

	while(digitalRead(echo) == LOW && micros()-now < 30000); // 30000 ms timeout

	startTimeUsec = micros();
	while(digitalRead(echo) == HIGH);
	endTimeUsec = micros();

	travelTimeUsec = endTimeUsec - startTimeUsec;
	double distInCM = 100*((travelTimeUsec/1000000.0) * 340.29)/2;
	return distInCM;
}

int Sonar::tick_function() {

	/* State transitions */
	switch(state) {
		case INIT:
			state = WAIT;
			break;
		case WAIT:
			state = PING;
			break;
		case PING:
			state = WAIT;
			break;
		default: 
			state = INIT;
			break;
	}

	/* State actions */
	switch(state) {
		case INIT:
			distCM = 0;
			trigger = 1;
			echo = 0;
			pinMode(trigger, OUTPUT);
			pinMode(echo, INPUT);
			digitalWrite(trigger, LOW);
			delay(500);
			break;
		case WAIT:
			break;
		case PING:
			distCM = poll_distance();
			std::cout << "Distance: " << distCM << " cm" << endl;
			break;
		default:
			break;
	}
	return 0;
}