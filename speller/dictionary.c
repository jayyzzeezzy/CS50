// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// declare variables
unsigned int word_count;
unsigned int hash_bucket;
unsigned int hash_value;


// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // use the hash function to get a hash value
    hash_value = hash(word);

    // set up cursor pointing at the start of the hash table
    node *cursor = table[hash_value];

    // compare word to dictionary by using a loop
    // conditional: as long as linked list is not at the end/NULL
    while (cursor != NULL)
    {

        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned long total_ascii = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        // draw inspirations from youtube
        total_ascii += tolower(word[i]);
    }
    return total_ascii % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // open up the dictionary
    FILE *file = fopen(dictionary, "r");

    // return NULL if file cannot be opened
    if (file == NULL)
    {
        printf("File cannot be opened %s\n", dictionary);
        return false;
    }
    // declare variable called word
    char word[LENGTH + 1];

    //read each word inside the dictionary until we reach the end of file -   EOF
    while (fscanf(file, "%s", word) != EOF)
    {
        // give memory for each valid word
        node *n = malloc(sizeof(node));
        // exit out if malloc returns NULL
        if (n == NULL)
        {
            return false;
        }

        // copy word into node
        strcpy(n->word, word);
        // call on the hash function to determine which bucket to put the word into
        hash_bucket = hash(word);
        n->next = table[hash_bucket];
        table[hash_bucket] = n;
        word_count++;
    }
    fclose(file);
    return true;

}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // iterate each of buckets inside the hash table
    for (int i = 0; i < N; i++)
    {
        // set up cursor to point at the beginning of each linked list
        node *cursor = table[i];
        // if cursor is not NULL then free
        while (cursor != NULL)
        {
            // make a tmp variable to keep track of the current location in linked list
            node *tmp = cursor;
            // move cursor to the next location inside linked list
            cursor = cursor->next;
            // free memory at tmp location
            free(tmp);
        }

        // when you hit the last bucket of the array and no more nodes inside the linked list
        if (cursor == NULL && i == N - 1)
        {
            return true;
        }
    }

    return false;
}
