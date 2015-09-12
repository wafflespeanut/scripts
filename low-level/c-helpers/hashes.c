#include <stdio.h>

// djb2 (stolen from http://www.cse.yorku.ca/~oz/hash.html)

unsigned long hash(unsigned char *str) {    // 33 & 5381 are magic numbers
    unsigned long hash = 5381;  // some salt
    int ch;

    while (ch = *str++) {
        hash = (hash << 5) + hash + ch;
        hash = hash * 33 ^ ch;
    } return hash;
}
