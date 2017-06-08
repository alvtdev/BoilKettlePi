/******************************************************************************
 * Author: Nicholas Pelham
 * Date  : 4/27/2017
 * Modified on 5/8 by Alvin Thai
 *****************************************************************************/

#include "task.hpp"
#include "heater.hpp"
#include <wiringPi.h>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>

Heater::Heater(int ms, Temperature* t, Timer* time, Sonar* s, int minutes) : Task(ms) {
    pinMode(6, OUTPUT);
    digitalWrite(6, LOW);
    state = INIT;
    this->t = t;    
    this->time = time;
    this->dist = s;
    temp = t->get_temperature();
    heatflag = -1;
    fullflag = -1;
    boilTimeHrs = 0;
    boilTimeMins = 0;
    boilTimeSeconds = 60*minutes;
    timerSeconds = 0;
    timeLeft = -1;
}

int Heater::get_timeLeft_seconds() {
    return timeLeft;
}

int Heater::calc_timeLeft() {
    timeLeft = boilTimeSeconds - timerSeconds;
    return timeLeft;
}

int Heater::get_boilTime() {
    return boilTimeSeconds;
} 

int Heater::get_timerSeconds() {
    return timerSeconds;
}

int Heater::get_fullStatus() {
    return fullflag; 
}

void Heater::init_boilTime(int hrs, int min, int sec) {
    boilTimeSeconds = sec + 60*min + 3600*hrs;
    return;
}

void Heater::create_boilText() {
    ofstream outfile("boil.txt"); 
    if (outfile.is_open()) {
        outfile << "1";
    }
    //std::cout << "boil.txt created" << std::endl;
    return;
}

int Heater::tick_function() {
    int temptime = 0;
    /* State transitions */
    switch(state) {
        case INIT:
            state = OFF;
            break;
        case OFF:
            //state waits for boil kettle to fill before heating
            if (heatflag != -1) {
                if (dist->get_distance() > BK_MAX_HEIGHT_CM/2) {
                    fullflag = 1;
                    state = HEAT;
                    //std::cout << "state = HEAT" << std::endl;
                }
                else {
                    fullflag = -1;
                    state = OFF;
                    //std::cout << "state = OFF" << std::endl;
                }
            } 
            break;
        case HEAT:
            if (temp >= 75.0) {
                time->start_timer();
                create_boilText();
                state = BOIL;
                //std::cout << "state = BOIL" << std::endl;
            }
            else {
                state = HEAT;
            }
            break;
        case BOIL:
            if (calc_timeLeft() <= 0) { 
                time->stop_timer();
                timeLeft = -10;
                //std::cout << "state = MAINTAIN" << std::endl;
                state = MAINTAIN;
            }
            else {
                state = BOIL;
            }
            break;
        case MAINTAIN:
            break;
        default: 
            state = INIT;
            break;
    }

    /* State actions */
    switch(state) {
        case INIT:
            break;
        case OFF:
            //init_boilTime(1, 0, 10);
            digitalWrite(6, LOW);
            heatflag = 1;
            break;
        case HEAT:
            digitalWrite(6, HIGH);
            temp = t->get_temperature();
            break;
        case BOIL:
            timerSeconds = time->get_seconds();
            temptime = calc_timeLeft();
            /*
            std::cout << "Boil time: " << boilTimeSeconds << std::endl;
            std::cout << "Timer: " << timerSeconds << std::endl;
            std::cout << "Time Left: " << calc_timeLeft() << std::endl << std::endl;
            */
            break;
        case MAINTAIN:
            /*
            if (temp <= 75.0) { 
                //std::cout << "Heater: ON" << std::endl;
                digitalWrite(6, HIGH);
                temp = t->get_temperature();
            }
            else {
                //std::cout << "Heater: OFF" << std::endl;
                digitalWrite(6, LOW);
                temp = t->get_temperature();
            }
            */
            digitalWrite(6, LOW);
            break;
        default:
            break;
    }

    return 0;
}
