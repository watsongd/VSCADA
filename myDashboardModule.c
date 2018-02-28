#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include "typedefs.h"
#include "serial.h"
#include "cf_packet.h"
#include "show_packet.h"

static PyObject* py_writeToScreen(PyObject* self, PyObject* args)
{
	//store the args
	int col;
	int row;
	char *message;

	//get the args
	PyArg_ParseTuple(args, "iis", &col, &row, &message);

    //Send line 1 to the 635 using command 31
    outgoing_response.command = 31;
    outgoing_response.data[0]=col; //col
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

	return Py_BuildValue("Success");
}

/*
 * Bind Python function names to our C functions
 */
static PyMethodDef myModule_methods[] = {
  {"writeToScreen", py_writeToScreen, METH_VARARGS},,
  {NULL, NULL}
};

/*
 * Python calls this to let us initialize our module
 */
void initmyModule()
{
  (void) Py_InitModule("myModule", myModule_methods);
}
