#include <stdio.h>

void hello();
int add(int x,int y);

int main(void)
{
	hello();
        printf("%d",add(2,3));
        printf("\n");
	return 0;
}

void hello()
{
	printf("HELLO WORLD!\n");
    printf("Hello everyone!\n");
	
}

int add(int x,int y){
   return x+y;
}

