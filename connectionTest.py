# Steps before running python below:
# gcc -dynamiclib -I/usr/include/python3.6/ -lpython3.6 -o myModule.dylib myModule.c
# mv myModule.dylib myModule.so 
from myModule import *

print writeToScreen()

