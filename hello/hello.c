#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //prompt user for an answer
    string answer = get_string("What's your name? ");
    printf("Hello, %s\n", answer);
}