/*
 * =====================================================================================
 *
 *       Filename:  RSA.c
 *
 *    Description:  RSA.c
 *
 *        Version:  1.0
 *        Created:  03/01/2016 09:15:31 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

void generateRandomNumber(int num[])
{
    int i;

    for(i = 0; i < 128; i++)
    {
        num[i] = rand() % 2;
    }
}

void viewRandomNumber(int num[], int length)
{
    int i;
    int oct = 0;

    printf("Bin: ");

    for(i = length-1; i >= 0; i--)
    {
        printf("%d", num[i]);
    }

    printf("\n");
}

int * mul(int num1[], int length_1, int num2[], int length_2)
{
    int i, j;
    int length = length_1 + length_2;
    int * res = (int *)calloc(length, sizeof(int));
    int carry = 0;

    for(i = 0; i < length; i++)
    {
        res[i] = 0;
    }

    for(i = 0; i < 128; i++)
    {
        for(j = 0; j < 128; j++)
        {
             res[i+j] += num1[i] * num2[j];
        }
    }

    for(i = 0; i < length; i++)
    {
        res[i] = (res[i] + carry) % 2;
        carry = (res[i] + carry) / 2;
    }

    return res;
}

int main()
{
    time_t t;
    int p[128];
    int q[128];
    int * e;

    srand((unsigned) time(&t));

    generateRandomNumber(p);
    generateRandomNumber(q);

    viewRandomNumber(p, 128);
    viewRandomNumber(q, 128);

    e = mul(p, 128, q, 128);

    viewRandomNumber(e, 256);

    return 0;
}
