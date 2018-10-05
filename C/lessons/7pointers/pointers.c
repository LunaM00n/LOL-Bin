#include <stdio.h>
int main()
{
	int a=5; 
	printf("The value of a:%d\n",a);
	printf("The address of a:%x\n",&a);
	int* p;
	printf("The address of p:%x\n",p);
	p=&a;
	printf("The address of p:%x\n",p);
	printf("The value of *p:%d\n",*p);	

	return 0;
}
