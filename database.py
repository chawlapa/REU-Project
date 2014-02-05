#this will simulate the database connections
import math

'''
    Class Database:
        This class will be used to simulate the database.  the data attribute will hold the data
        The functions provided will be used to help the client retrieve its data
'''
class Database():

    '''  --------init--------
         called when the Database object is created.
         Inputs: a string for the text file
         Output: the Database object
    '''
    def __init__(self,filename=None):
        #self.name = name
        self.data = [] #this will be a 2D matrix
        if filename != None:
            self.populate_data(filename)

    '''  --------get_sum_of_column--------
         returns the total amount of x and y for a certain column
         Inputs: column integer
         Output: a pair of x and y values
         Note: This should only be called from get_coloumn_information
    '''
    def get_sum_of_column(self,column):
        retX = 0
        retY = 0
        for i in range(len(self.data)):
            if self.data[i][len(self.data[0])-1] == 1:
                retX += 1#int(self.data[i][column])
            else:
                retY += 1#int(self.data[i][column])

        return (retX,retY)

    '''  --------get_column_information--------
         Called from the outside to get values for a specific column
         Inputs: a column value.  if a -1 is passed it in, it will get
                 infomration from the entire database
         Output: a pair of x and y values
    '''
    def get_column_information(self,column):
        #if colukmn is -1, then we want to get all of the information
        # else we just get that columns attributes
        x = 0
        y = 0
        if column == -1:
            for i in range(len(self.data[0])-1):
                values = self.get_sum_of_column(i)
                x += values[0]
                y += values[1]
            return (x,y)
        else:
            return self.get_sum_of_column(column)

    '''  --------get_num_of_columns--------
         returns the number of attributes + 1
         Inputs: None
         Output: the number of attributes
         Note: Make sure you take the value and subtract by 1
    '''
    def get_num_of_columns(self):
        return len(self.data[0])

    def get_num_of_rows(self):
        return len(self.data)

    def get_class_of_row(self,row):
        return self.data[row][-1]

    '''  --------populate_data--------
         loads the data into the data attribute from the data file
         Inputs: a string for the text file
         Output: None
    '''
    def populate_data(self,filename):
        try:
            infile = open(filename,'r')
            for line in infile:
                line = line.strip()
                linearr = line.split('\t')
                temp = []
                if len(linearr) > 0:
                    for item in linearr:
                        
                        temp.append(int(item.strip())) #get rid of whitespace
                    self.data.append(temp)
        except Exception as err:
            print(err)

    def add_row(self,row):
        self.data.append(row)

    def get_row(self,row):
        return self.data[row]

    '''  --------print_data--------
         prints the data that is contained in the database
         Inputs: None
         Output: None
    '''
    def print_data(self):
        print('------------')
        for item in self.data:
            print(item)
        print('------------')

'''  --------calculate_entropy--------
     Calculates the entropy from the pair of values
     Inputs: the x and y value
     Output: The entropy as a float
'''
def calculate_entropy(y,z):
    return( ((y)/(y+z))*math.log((y)/(y+z)) + ((z)/(y+z))*math.log((z)/(y+z))) *-1

if __name__ == "__main__":

    #create teh database objects
    d1 = Database("dataset1.txt")
    d2 = Database("dataset2.txt")
    d3 = Database("dataset3.txt")

    d1.print_data()
    d2.print_data()
    d3.print_data()

    databases = [d1,d2,d3]
    #calculate entropy
    sumy = 0
    sumz = 0
    #get all the sumy and sumz
    print(d1.get_num_of_columns())
    for database in databases:
        y,z = database.get_column_information(database.get_num_of_columns()-1)
        sumy += y
        sumz += z
    main_entropy = calculate_entropy(sumy,sumz)
    print("entropy: %f" % main_entropy)

    #first level of entropy
    maxgain = (-1,-1)
    for i in range(d1.get_num_of_columns()-2): #this will go through columns a,b,c,....
        #construct virtual databases
        tempd1 = Database()
        tempd2 = Database()
        temp_databases = [tempd1,tempd2]
        for database in databases:
            for row in range(database.get_num_of_rows()):
                if database.get_class_of_row(row) == 1:
                    tempd1.add_row(database.get_row(row))
                else:
                    tempd2.add_row(database.get_row(row))
        tempd1.print_data()
        tempd2.print_data()
        
        #get entropy of the database
        for tdata in temp_databases:
            #how do we get the entropy when we only have 1s and 0s?
            y,z = tdata.get_column_information(database.get_num_of_columns()-1)
            temp_entropy = calculate_entropy(y, z)
            print("temp_entropy: %f" % temp_entropy)
    

##    #calculate the entropy of D1
##    sumx,sumy = d1.get_column_information(-1)
##    entropy = calculate_entropy(sumx,sumy)
##    print("DATA1: %f" % entropy)
##
##    #Calculate the entropy for each column in the database
##    for i in range(d1.get_num_of_columns()-1):
##        x,y = d1.get_column_information(i)
##        entropy = calculate_entropy(x,y)
##        print("D1 column %i: %f" % (i,entropy))
##
##    #calculate the entropy of D2
##    sumx,sumy = d2.get_column_information(-1)
##    entropy = calculate_entropy(sumx,sumy)
##    print("DATA2: %f" % entropy)
##
##    #Calculate the entropy for each column in the database
##    for i in range(d2.get_num_of_columns()-1):
##        x,y = d2.get_column_information(i)
##        entropy = calculate_entropy(x,y)
##        print("D2 column %i: %f" % (i,entropy))
##
##    #calculate the entropy of D3
##    sumx,sumy = d3.get_column_information(-1)
##    entropy = calculate_entropy(sumx,sumy)
##    print("DATA3: %f" % entropy)
##
##    #Calculate the entropy for each column in the database
##    for i in range(d3.get_num_of_columns()-1):
##        x,y = d3.get_column_information(i)
##        entropy = calculate_entropy(x,y)
##        print("D3 column %i: %f" % (i,entropy))
##
##    #get all the entropy for the entier system
##    sumx = 0
##    sumy = 0
##    databases = [d1,d2,d3]
##    print(d1.get_num_of_columns())
##    for i in range(d1.get_num_of_columns()-1): #<-- this assumes all the databases have the same size
##        tempx = 0
##        tempy = 0
##        for database in databases:
##            x,y = database.get_sum_of_column(i)
##            sumx += x
##            sumy += y
##            tempx += x
##            tempy += y
##        entropy = calculate_entropy(tempx,tempy)
##        print("ALL column %i: %f" % (i,entropy))
##            
##    #Entropy of the entire system
##    entropy = calculate_entropy(sumx,sumy)
##    print("ALL: %f" % entropy)
##
##
##            
##


    
    
