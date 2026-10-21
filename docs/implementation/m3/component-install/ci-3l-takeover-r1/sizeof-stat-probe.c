#include <stdio.h>
#include <sys/stat.h>
int main(void) { printf("%zu\n", sizeof(struct stat)); return 0; }
