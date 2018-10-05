#include <stdio.h>
int addNumber(int a,int b)
{
	int result;
	result=a+b;
	return result;
}

int main()
{
	int num1,num2,result;
	printf("Enter num1:\n");
	scanf("%d",&num1);
	printf("Enter num2:\n");
	scanf("%d",&num2);
	result=addNumber(num1,num2);
	printf("%d + %d = %d",num1,num2,result);
	return 0;
}
