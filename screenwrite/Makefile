IDIR =../include
DIR=/usr/local/Cellar/python/3.6.4_3/Frameworks/Python.framework/Versions/3.6/include/python3.6m
CC=gcc
CFLAGS=-I$(IDIR)

ODIR=obj
LDIR =../lib

LIBS_DIR=/usr/local/opt/python/Frameworks/Python.framework/Versions/3.6/lib/python3.6/config-3.6m-darwin
LIBS=-lpython3.6m

_DEPS =cf_packet.h show_packet.h serial.h typedefs.h screenwrite.h 
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ =cf_packet.o show_packet.o serial.o typedefs.o screenwrite.o wrapper_screenwrite.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

screenwrite: $(OBJ)
	gcc -shared $^ $(CFLAGS) -L$(LIBS_DIR) $(LIBS) -o $@

hellomake: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 
