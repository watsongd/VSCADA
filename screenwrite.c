#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include "typedefs.h"
#include "serial.h"
#include "cf_packet.h"
#include "show_packet.h"

#include "screenwrite.h"

void writeToScreen(int row, char *message)
{
	//Connect to the display
	// if(Serial_Init("/dev/ttyACM0",115200))
 //    {
	//     printf("Could not open port \"%s\" at \"%d\" baud.\n","/dev/ttyACM0",115200);
 //    }
 //  	else
 //    printf("\"%s\" opened at \"%d\" baud.\n\n","/dev/ttyACM0",115200);

    //Send line 1 to the 635 using command 31
    outgoing_response.command = 31;
    outgoing_response.data[0]=0; //col
    outgoing_response.data[1]=row; //row
    memcpy(&outgoing_response.data[2], message, 20);
    outgoing_response.data_length = 22;  //the col & row position + the 20 char data length
    send_packet();

	//CFA-635 communications protocol only allows
	//one outstanding packet at a time. Wait for the response
	//packet from the CFA-635 before sending another
	//packet.
	int k;
	int timed_out;
	timed_out = 1; //default timed_out is true
	for(k=0; k<=10000; k++)
	if(check_for_packet())
	{
		ShowReceivedPacket();
		timed_out = 0; //set timed_out to false
		break;
	}
	if(timed_out)
	printf("Timed out waiting for a response.\n");
	
	//Disconnect from the display
	// Uninit_Serial();

}

//gcc -Isrc -fPIC $(pkg-config --cflags --libs python3) -c src/screenwrite.c wrapper_screenwrite.c
//gcc -shared -fPIC -o screenwrite.so screenwrite.o wrapper_screenwrite.o src/include/serial.o src/include/show_packet.o src/include/cf_packet.o
