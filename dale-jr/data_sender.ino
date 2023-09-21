#include <stdio.h>
#include <time.h>

void sendData()
{
    char buffer[128]; // Allocate a buffer to hold the formatted string

    // Format the data into a string
    int len = snprintf(buffer, sizeof(buffer), "{thrust1:%f,thrust2:%f,thrust3:%f,mass:%f,thrust:%f,pressure1:%f,pressure2:%f,temperature:%f}", );
    serial.write(buffer, len);
}
