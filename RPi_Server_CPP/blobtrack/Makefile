#Name: Makefile
#Author: John Board
#Date: 10/02/2016
#Description: Makefile for QUT Air Hockey Table

#Compiler and Linker variables
CC = g++
CFLAGS = -c -std=c++11 -pthread
LDFLAGS = -L./opencvblobslib/library -lopencvblobslib -lpthread

#List of sources
SOURCES = blobtrack.cpp
OBJECTS = $(SOURCES:.cpp=.o)

CFLAGS += `pkg-config --cflags opencv`
LDFLAGS += `pkg-config --libs opencv`

#Name of output executable
EXECUTABLE=blobtrack

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@ $(LDFLAGS)

.cpp.o:
	$(CC) $(SOURCES) $(CFLAGS) -o $@

clean:
	rm $(OBJECTS) $(EXECUTABLE)
