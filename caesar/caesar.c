#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

// function to check only digits
bool only_digits(string s);

// function to shift letters
char rotate(char c, int z);

int main(int argc, string argv[])
{
    // when user put more than 1 key or no key
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // when user put in letters for key
    else if (only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // change string to int
    // use variable convert to hold the value
    int convert = atoi(argv[1]);

    // do this when user do cooperate
    string text = get_string("plain text: ");

    char cipherchar = 's';
    // print out user input
    printf("ciphertext: ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        cipherchar = rotate(text[i], convert);
        printf("%c", cipherchar);
    }
    printf("\n");
    return 0;
}


// define how only digits work
bool only_digits(string s)
{
    bool tf = true;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isdigit(s[i]))
        {
            tf = true;
        }
        else if (isdigit(s[i]) == 0)
        {
            tf = false;
        }
    }
    return tf;
}

// define the rotate function
char rotate(char c, int z)
{
    // shift ascii index to zero index
    // for capital letters
    int shift = 0;
    if (isalpha(c) && isupper(c))
    {
        shift = c - 'A';
        shift = (shift + z) % 26;
        shift += 'A';
    }
    // for lower case letters
    else if (isalpha(c) && islower(c))
    {
        shift = c - 'a';
        shift = (shift + z) % 26;
        shift += 'a';
    }
    // for special characters
    else
    {
        shift = c;
    }
    return shift;
}
