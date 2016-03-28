#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include "ikine.cpp"

#define X_SPEED 0.05
#define Y_SPEED 0.05
#define MAX_INT16 32767

using namespace std;

Ikine* ik;
int fd;

typedef struct _js_event {
    uint32_t time;     /* event timestamp in milliseconds */
    int16_t value;    /* value */
    uint8_t type;      /* event type */
    uint8_t number;    /* axis/button number */
} js_event;

js_event e;

int main(){

    ik = new Ikine();
    double x = 50, y = 35, oldX, oldY;
    int16_t stickX, stickY;

    fd = open("/dev/input/js1", O_NONBLOCK);
    while(true){
        if(read(fd, &e, sizeof(e)) > 0){ // if joystick changed
            if(e.type == 0x02){ // if its the joystick
                if(e.number == 0){ // if joystick x
                    stickX = e.value;
                } else if(e.number == 1){ // joystick y
                    stickY = e.value;
                }
            }
        }

        oldX = x;
        oldY = y;

        x += X_SPEED * stickX / MAX_INT16;
        y -= Y_SPEED * stickY / MAX_INT16;

        if(!ik->moveTo(x, y)){
            x = oldX;
            y = oldY;
        }
    }

    return 0;
}