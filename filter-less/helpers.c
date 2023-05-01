#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // to go thru each row
    for (int i = 0; i < height; i++)
    {
        // to go thru each column
        for (int j = 0; j < width; j++)
        {
            // convert to floatinig point value
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float blue = image[i][j].rgbtBlue;

            // find the average value
            int average = round((red + green + blue) / 3);
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // go thru each row
    for (int i = 0; i < height; i++)
    {
        // go thru each column
        for (int j = 0; j < width; j++)
        {
            // convert to floating point value
            float originalred = image[i][j].rgbtRed;
            float originalgreen = image[i][j].rgbtGreen;
            float originalblue = image[i][j].rgbtBlue;

            // find the updated pixel value
            int sepiared = round(0.393 * originalred + 0.769 * originalgreen + 0.189 * originalblue);
            int sepiagreen = round(0.349 * originalred + 0.686 * originalgreen + 0.168 * originalblue);
            int sepiablue = round(0.272 * originalred + 0.534 * originalgreen + 0.131 * originalblue);

            // cap pixel value at 255 if value exceeds 255
            if (sepiared > 255)
            {
                sepiared = 255;
            }

            if (sepiagreen > 255)
            {
                sepiagreen = 255;
            }

            if (sepiablue > 255)
            {
                sepiablue = 255;
            }

            image[i][j].rgbtRed = sepiared;
            image[i][j].rgbtGreen = sepiagreen;
            image[i][j].rgbtBlue = sepiablue;

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // go thru each row
    for (int i = 0; i < height; i++)
    {
        // go thru each column
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // make a temp copy of an image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    float totalred, totalgreen, totalblue;
    int count = 0;
    totalred = totalgreen = totalblue = 0.00;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // x for iterating thru rows in the neighbor pixels
            for (int x = i - 1; x <= i + 1; x++)
            {
                // y for iterating thru columns in the neighbor pixels
                for (int y = j - 1; y <= j + 1; y++)
                {

                    // check if you can use the neighboring pixels
                    if (y < width && x < height && y >= 0 && x >= 0)
                    {
                        totalred += temp[x][y].rgbtRed;
                        totalgreen += temp[x][y].rgbtGreen;
                        totalblue += temp[x][y].rgbtBlue;
                        count++;
                    }
                }
            }
            // update the image value
            image[i][j].rgbtRed = round(totalred / count);
            image[i][j].rgbtGreen = round(totalgreen / count);
            image[i][j].rgbtBlue = round(totalblue / count);

            // reset counters
            count = 0;
            totalred = totalgreen = totalblue = 0;
        }
    }
    return;
}
