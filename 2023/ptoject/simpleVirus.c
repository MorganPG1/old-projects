#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
int main()
{   
    char a[50];
    fgets(a, sizeof(a), stdin);

    while (1==1)
    {
        MessageBox(NULL, "pranked","get prank ", 0x00000014L);
    }
}