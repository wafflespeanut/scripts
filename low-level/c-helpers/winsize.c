#include <sys/ioctl.h>
#include <stdio.h>
#include <unistd.h>

int main (int argc, char **argv) {
    struct winsize wsize;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &wsize);
    printf("\n(STDOUT_FILENO: %d, TIOCGWINSZ: 0x%x)\n", STDOUT_FILENO, TIOCGWINSZ);
    printf ("(%d lines, %d columns)\n\n", wsize.ws_row, wsize.ws_col);
    return 0;
}
