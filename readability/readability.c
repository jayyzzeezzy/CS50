#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int cal_grade_level(int x, int y, int z);

int main(void)
{

    // ask user to type a text
    string text = get_string("Text: ");

    // print user input
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        printf("%c", text[i]);
    }
    printf("\n");

    // use the count letters function
    int letter = count_letters(text);
    printf("%i letters\n", letter);

    // use the count words function
    int word = count_words(text);
    printf("%i words\n", word);

    // use the count sentences function
    int sentence = count_sentences(text);
    printf("%i sentences\n", sentence);

    // use the cal grade level function
    int grade = cal_grade_level(letter, sentence, word);
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }


}


// define how count letters function work
int count_letters(string text)
{
    int letter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letter++;
        }

    }
    return letter;
}


// define how count words function work
int count_words(string text)
{
    int word = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        {
            word++;
        }
    }
    return word;
}


// define how count sentences work
int count_sentences(string text)
{
    int sentence = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentence++;
        }
    }
    return sentence;
}


// define how calculate grade level work
int cal_grade_level(int x, int y, int z)
{

    float l = (float) x / z * 100;

    float s = (float) y / z * 100;

    float index = 0.0588 * l - 0.296 * s - 15.8;

    return round(index);
}