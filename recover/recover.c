#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;



int main(int argc, char *argv[])
{
    // check for input. user should have typed in the name of file
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // open up the file user type in
    FILE *input = fopen(argv[1], "r");

    // handles the case where file cannot be opened
    if (input == NULL)
    {
        printf("Could not open file\n");
        return 2;
    }

    // store blocks of 512 bytes in an array
    unsigned char buffer[512];

    // counter for number of images generated
    int counter = 0;

    // pointer for the output file which is recovered images
    FILE *output = NULL;

    char *filename = malloc(8 * sizeof(char));

    //  read thru the blocks of 512 bytes
    while (fread(buffer, sizeof(char), 512, input))
    {
        // check the start of byte to see if it is JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close the previous JPEG file when you find a new JPEG file
            if (counter > 0)
            {
                fclose(output);
            }

            // create filenames for JPEG files
            sprintf(filename, "%03i.jpg", counter);

            // open output and write in it
            output = fopen(filename, "w");

            // count number of JPEG images found
            counter++;

        }

        // check if oupt has been used for valid input
        if (output != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output);
        }

    }

    free(filename);
    fclose(output);
    fclose(input);

    return 0;
}