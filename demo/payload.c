#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
int main()
{
    FILE* ptr;
    char ch;
 
    ptr = fopen("/etc/passwd", "r");
 
    if (NULL == ptr) {
        printf("file can't be opened \n");
    }
 
    // Printing what is written in file
    // character by character using loop.
    do {
        ch = fgetc(ptr);
        printf("%c", ch);
    } while (ch != EOF);
 
    fclose(ptr);
    return 0;
}
