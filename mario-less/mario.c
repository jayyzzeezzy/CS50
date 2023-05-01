#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    //continue to ask this question until user cooperates
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    //for each row
    for (int i = 0; i < n; i++)
    {

        //s accounts for how many spaces to print
        //spaces = height - row - 1
        //s < n - i - 1, you don't want to go thru the 8th iteration
        //8th iteration will print 9 hases
        for (int s = 0; s < n - i - 1; s++)
        {
            //print a space
            printf(" ");
        }

        //for each column
        //you want row number = hash number
        //row index starts at 0
        for (int j = 0; j <= i; j++)
        {
            //print a brick
            printf("#");
        }

        //start the next row
        printf("\n");

    }
}