# MakefileTesting
##Link I'm Trying to Emulate:
https://github.com/UiO-INF3331/code-snippets/tree/master/mixed/c-api
##Main Page:
https://github.com/UiO-INF3331/student-resources-16/blob/master/lectures/07_mixed_programming_swig.ipynb
##Youtube Video: 
https://www.youtube.com/watch?v=J-iVTLp6M9I

```
gcc -Isrc -fPIC $(pkg-config --cflags --libs python3) -c cf_packet.c screenwrite.c serial.c show_packet.c wrapper_screenwrite.c
gcc -shared -fPIC -o screenwrite.so cf_packet.o screenwrite.o serial.o show_packet.o wrapper_screenwrite.o
```

##Find Port (Linux):
ls -l /dev/serial/by-id

##Run Code:
python3 test.py