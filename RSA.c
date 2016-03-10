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

/*
 * =====================================================================================
 *    Function: generateRandomNumber
 *
 * Description: generate a 128 bits binary integer number
 *
 *  Parameters: int num[]    array of integer
 *
 *              int length   the length of the random binary nubmer
 *
 *      Return: void
 *
 * =====================================================================================
 */
void generateRandomNumber(int num[], int length)
{
    int i;

    for(i = 0; i < length; i++)
    {
        num[i] = rand() % 2;
    }
}

/*
 * =====================================================================================
 *    Function: viewRandomeNumber
 * 
 * Description: display binary number on screen
 *
 *  Parameters: int num[]    binary number as integer number
 *             
 *             int length   the length of binary number
 *
 *      Return: void
 * 
 * =====================================================================================
 */

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

/*
 * =====================================================================================
 *    Function: mul
 * 
 * Description: calculate the result of two binary number
 *
 *  Parameters: int num1[]       the first binary number
 *
 *              int length_1     the lenght of first binary number
 *
 *              int num2[]       the second binary number
 *
 *              int length_2     the lenght of second binary number
 *   
 *              int * length_res the lenght of result
 *
 *      Return: res              the result of multiple                
 *
 * =====================================================================================
 */
int * mul(int num1[], int length_1, int num2[], int length_2, int * length_res)
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

    * length_res = length;

    return res;
}

int main()
{
    time_t t;
    int length_p = 3;
    int length_q = 3;
    int p[length_p];
    int q[length_q];
    int * e;
    int length_e;

    srand((unsigned) time(&t));

    generateRandomNumber(p, length_p);
    generateRandomNumber(q, length_q);

    viewRandomNumber(p, length_p);
    viewRandomNumber(q, length_q);

    e = mul(p, length_p, q, length_q, &length_e);

    viewRandomNumber(e, length_e);

    return 0;
}
