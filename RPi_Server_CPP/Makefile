#Name: Makefile
#Author: John Board
#Date: 10/02/2016
#Description: Makefile for QUT Air Hockey Table

#Compiler and Linker variables
CC = g++
CFLAGS = -c -std=c++11
LDFLAGS =

#List of sources
SOURCES = cvChromaticityTest.cpp
OBJECTS = $(SOURCES:.cpp=.o)

CFLAGS += `pkg-config --cflags opencv`
LDFLAGS += `pkg-config --libs opencv`

#Name of output executable
EXECUTABLE=program

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@ $(LDFLAGS)

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm $(OBJECTS) $(EXECUTABLE)
