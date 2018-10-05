#include <stdio.h>
int main()
{
	int a=4; //4 bytes on momery
	char b='A'; // 1 byte
	char string[]="I m string"; //char string
	float c=1.5; //real number 4 bytes
	double d=1.55555555; //real number 8 bytes
	
	//unsgined for hloding positive value
	//signed for holding both postive and negative

	printf("The value of a : %d , The size of int : %d\n",a,sizeof(a));
	printf("The value of b : %c , The size of char : %d\n",b,sizeof(b));
	printf("The value of string : %s , The size of string : %d\n",string,sizeof(string));
	printf("The value of c : %f , The size of float : %d\n",c,sizeof(c));
	printf("THe value of d : %f , The size of double : %d\n",d,sizeof(d));
	return 0;
}
