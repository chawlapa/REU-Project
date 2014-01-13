//Priya Chawla
//Special Studies (Research)
/**This program:
1) Reads in file
2) Dynamically stores data into array
3) Counts for number of Y and Z
4) Calculates entropy AFTER splitting
 **/

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <cstring>
#include <string>
#include <math.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <vector>
#include <sstream>


using namespace std;



int main()
{
    int sets;
    int x = 0;

    cout << "Enter the number of datasets: ";
    cin  >> sets;
    cout << "Ready to compute entropy for " << sets << " datasets.";

    while (x < sets){
        x++;
        string fileName;

        int cols;
        cout << "Enter the name of the dataset (filename): ";
        cin  >> fileName;
        cout << "Enter the number of columns of data: ";
        cin  >> cols;

        int dataArray[100][cols];

        ifstream inFile (fileName.c_str());

        if(!inFile)
        {
            cout << "Error! Couldn't read file." << endl;

            return -1;
        }
        int sumy = 0;
        int sumz = 0;
        int row = 0;

        while (!inFile.eof())//read a full line into the buffer array
        {
            for( int col = 0; col < cols;col++)
            {
                inFile >> dataArray[row][col];

                if (col == cols-1) {if (dataArray[row][col] == 0) sumy++;
                if (dataArray[row][col] == 1) sumz++;}
            }
            row++;
        }
    float total, PY, PZ, lny, lnz, entropy;

    total = sumy + sumz;
    PY = sumy/total;
    PZ = sumz/total;
    lny = log(PY);
    lnz = log(PZ);
    entropy = ((PY*lny) + (PZ*lnz)) * -1;

    cout << "entropy: " << entropy << endl;

    }
}
