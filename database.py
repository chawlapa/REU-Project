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
        keys = []
        for i in range(len(self.data)):
            if self.data[i][column] not in keys:
                keys.append(self.data[i][column])

        rDict = dict.fromkeys(keys)

        for i in range(len(self.data)):
            if rDict.get(self.data[i][column]) == None:
                rDict[self.data[i][column]] = 1
            else:
                rDict[self.data[i][column]] += 1

        return (rDict)

    '''  --------get_column_information--------
         Called from the outside to get values for a specific column
         Inputs: a column value.  if a -1 is passed it in, it will get
                 infomration from the entire database
         Output: a pair of x and y values
    '''
    def get_column_information(self,column):
        #if colukmn is -1, then we want to get all of the information
        # else we just get that columns attributes
        rDict = None
        
        if column == -1:
            for i in range(len(self.data[0])-1):
                temp_dict = self.get_sum_of_column(i)
                if rDict == None:
                    rDict = temp_dict
                else:
                    for key,value in temp_dict.items():
                        rDict[key] += value
            return (rDict)
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
def calculate_entropy(entropy_dict):
    total = 0
    for key,value in entropy_dict.items():
        total += value
    entropy = 0
    for key,value in entropy_dict.items():
        entropy += ((value/total)*(math.log(value/total)))
    
    #return( ((x)/(x+y+z))*math.log((x)/(x+y+z)) + ((y)/(x+y+z))*math.log((y)/(x+y+z)) + ((z)/(x+y+z))*math.log((z)/(x+y+z))) *-
    return (entropy * -1)

def update_dict(rDict,temp_dict):
    if rDict == None:
        return temp_dict
    else:
        for key,value in temp_dict.items():
            rDict[key] += value
        return rDict

def get_letter(value):
    return chr(value + 65)


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
    entropy_dict = None
    #get all the sumy and sumz
    print(d1.get_num_of_columns())
    for database in databases:
        temp_dict = database.get_column_information(database.get_num_of_columns()-1)
        entropy_dict = update_dict(entropy_dict,temp_dict)
    main_entropy = calculate_entropy(entropy_dict)
    print("entropy: %f" % main_entropy)

    #first level of entropy
    maxgain = [-1,-1]
    for i in range(d1.get_num_of_columns()-1): #this will go through columns a,b,c,....
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
        #tempd1.print_data()
        #tempd2.print_data()
        
        #get entropy of the database
        entropy_dict = None
        results = []
        total_records = tempd1.get_num_of_rows() + tempd2.get_num_of_rows()
        
        for tdata in temp_databases:
            #how do we get the entropy when we only have 1s and 0s?
            temp_dict = tdata.get_column_information(i)
            entropy_dict = update_dict(entropy_dict,temp_dict)
            temp_entropy = calculate_entropy(entropy_dict)
            ratio = float(tdata.get_num_of_rows()/total_records)
            results.append(temp_entropy*ratio)
        weighted_avg = 0
        for items in results:
            weighted_avg += items
        if maxgain[1] < weighted_avg-main_entropy:
            maxgain[0] = i
            maxgain[1] = weighted_avg-main_entropy
        #print("weighted average -main entropy for column %i: %f" % (i,weighted_avg))
        print("The gain for column %s:  %f\n"% (get_letter(i),weighted_avg-main_entropy))
print("column %s give the maxgain: %f" % (get_letter(maxgain[0]),maxgain[1]))

        
    

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


    
    
