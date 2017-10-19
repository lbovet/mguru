#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/input.h>

#define MOUSEFILE "/dev/input/mouse1\0"
//
int main()
{
    int fd;
    struct input_event ie;
    unsigned char *ptr = (unsigned char*)&ie;
    //
    unsigned char button,bLeft,bMiddle,bRight;
    char x,y;                                                            // the relX , relY datas
    int absolute_x,absolute_y;
    char latch=0;

    if((fd = open(MOUSEFILE, O_RDONLY | O_NONBLOCK )) == -1)
    {
        printf("NonBlocking %s open ERROR\n",MOUSEFILE);
        exit(EXIT_FAILURE);
    }

    while(1)
    {
        usleep(50000);
        if(read(fd, &ie, sizeof(struct input_event))!=-1) {
            //
            button=ptr[0] & 0x7;
            bLeft = button & 0x1;
            bMiddle = ( button & 0x4 ) > 0;
            bRight = ( button & 0x2 ) > 0;
            if (button) {
                if(!latch) {
                  printf("%d\n", button);
                  fflush(stdout);
                }
                latch=1;
            } else {
              latch=0;
            }
        }
    }
    close(fd);
return 0;
}
