//Priya Chawla
//Special Studies (Research)
/**This program:
1) Add 1's from all 3 datasets
2 Add 0's from all 3 datasets
3) Computes total entropy for last column of 1's and 0's for ALL datasets
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

    cout << "Enter the number of datasets: "; //user enters total number of datasets
    cin  >> sets;
    cout << "Ready to compute entropy for " << sets << " datasets.";

    int sumzeros[sets];
    int sumones[sets];



    while (x < sets){
        x++;
        string fileName;

        int cols;
        cout << "Enter the name of the dataset (filename): "; //user enters name of each dataset (loops until all datasets are entered)
        cin  >> fileName;
        cout << "Enter the number of columns of dataset: "; //user enters number of columns per dataset (loops until all datasets are entered)
        cin  >> cols;

        int dataArray[100][cols]; //program can hold up to 100 rows

        ifstream inFile (fileName.c_str());

        if(!inFile)
        {
            cout << "Error! Couldn't read file." << endl;

            return -1;
        }
        int sumy = 0;
        int sumz = 0;
        int row = 0;

        //counts number of 0's and 1's in the last column for each dataset
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

    //calculates entropy for each dataset after each one is inputted
    float total, PY, PZ, lny, lnz, entropy;
    total = sumy + sumz;//adds total number of 1's and 0's
    PY = sumy/total; //divides number of 1's in individual dataset by total
    PZ = sumz/total; //divides number of 0's in individual dataset by total
    lny = log(PY); //calculates total entropy of 0's in dataset
    lnz = log(PZ); //calculates total entropy of 1's in dataset
    entropy = ((PY*lny) + (PZ*lnz)) * -1; //dataset entropy is calculated for individual dataset

    sumzeros[x] = 0;
    sumzeros[x] = sumy; //sums number of zeros for each dataset
    sumones[x] = 0;
    sumones[x] = sumz; //sums number of ones for each dataset

    cout << "total entropy of single dataset: " << entropy << endl; //OUTPUT: individual entropy of dataset

    }
    int i = 0;
    int totalzeros = 0;
    int totalones = 0;

        //computes sum of all 0's and 1's in all datasets
        while(i<sets) {
        i++;
        totalzeros = totalzeros + sumzeros[i]; //counts the total number of 0's
        totalones = totalones + sumones[i]; //counts the total number of 1's
        }

    //calculates entropy for last columns of all datasets
    float finaltotal, PYall, PZall, lnyall, lnzall, entropyall;
    finaltotal = totalzeros + totalones; //adds number of 0's and 1's in all datasets
    PYall = totalzeros/finaltotal; //calculates total number of zeros / total
    PZall = totalones/finaltotal; //calculates total number of ones / total
    lnyall = log(PYall); //calculates total entropy of 0's
    lnzall = log(PZall); //calculates total entropy of 1's
    entropyall = ((PYall*lnyall) + (PZall*lnzall)) * -1; //final entropy is calculated of 0's and 1's in all datasets

    cout << "Total Entropy of all datasets combined = " << entropyall << endl; //OUTPUT: total entropy of all datasets

}
