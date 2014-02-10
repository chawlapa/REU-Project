#this will simulate the database connections
import math
import sys
import copy


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
    def __init__(self,name,filename=None):
        #self.name = name
        self.data = [] #this will be a 2D matrix
        if filename != None:
            self.populate_data(filename)
        self.name = name

    def is_empty(self):
        if self.data == []:
            return True
        else:
            return False

    '''  --------get_sum_of_column--------
         returns the total amount of x and y for a certain column
         Inputs: column integer
         Output: a pair of x and y values
         Note: This should only be called from get_coloumn_information
    '''
    def get_sum_of_column(self,column,criteria):
        keys = []
        #self.print_data()
        for i in range(len(self.data)):
            #print("self.data[%i][%i]: %i" % (i,column,self.data[i][column]))
            if self.data[i][column] not in keys:
                keys.append(self.data[i][column])

        rDict = dict.fromkeys(keys)
        #print("rDict before: ",rDict)
        for i in range(len(self.data)):
            #check the criteria on the row
            increment = True
            for j in range(len(criteria)):
                #print("criteria[%i]: %i" % (j,criteria[j]))
                #print("self.data[%i][%i]: %i" % (i,j,self.data[i][j]))
                if criteria[j] != -1 and criteria[j] != self.data[i][j]:
                    increment = False
        #            print('criteria: ',criteria)
        #            print("row: %i | column: %i" % (i,j))
            if increment:
                if rDict.get(self.data[i][column]) == None:
                    rDict[self.data[i][column]] = 1
                else:
                    rDict[self.data[i][column]] += 1
        #print("rDict after: ",rDict)
        return (rDict)

    '''  --------get_column_information--------
         Called from the outside to get values for a specific column
         Inputs: a column value.  if a -1 is passed it in, it will get
                 infomration from the entire database
         Output: a pair of x and y values
    '''
    def get_column_information(self,column,criteria):
        #if column is -1, then we want to get all of the information
        # else we just get that columns attributes
        rDict = None
        
        if column == -1:
            for i in range(len(self.data[0])-1):
                temp_dict = self.get_sum_of_column(i,criteria)
                if rDict == None:
                    rDict = temp_dict
                else:
                    for key,value in temp_dict.items():
                        rDict[key] += value
            return (rDict)
        else:
            return self.get_sum_of_column(column,criteria)

    def get_column_unique_ident(self,column,criteria):
        rDict = self.get_sum_of_column(column,criteria)
        return len(rDict)

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

    def get_value_from_database(self,row,column):
        return self.data[row][column]

    '''  --------print_data--------
         prints the data that is contained in the database
         Inputs: None
         Output: None
    '''
    def print_data(self):
        print('-----%s------' % self.name)
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
    #print("entropy_dict: ",entropy_dict)
    for key,value in entropy_dict.items():
        if value != None:
            total += value
    entropy = 0
    for key,value in entropy_dict.items():
        if value == None:
            #print("skipping value: ",value) 
            continue
        entropy += ((value/total)*(math.log(value/total)))
    
    #return( ((x)/(x+y+z))*math.log((x)/(x+y+z)) + ((y)/(x+y+z))*math.log((y)/(x+y+z)) + ((z)/(x+y+z))*math.log((z)/(x+y+z))) *-
    return (entropy * -1)

def update_dict(rDict,temp_dict):
    if rDict == None:
        return temp_dict
    else:
        for key,value in temp_dict.items():
            if key not in rDict:
                rDict[key] = value
            elif rDict[key] == None:
                rDict[key] = value
            elif value != None:
                rDict[key] += value
        return rDict

def get_letter(value):
    return chr(value + 65)

def get_num_of_nodes(databases,column,criteria):
    num_of_nodes = 0
    for database in databases:
        num = database.get_column_unique_ident(column,criteria)
        if num > num_of_nodes:
            num_of_nodes = num
    return num_of_nodes

def populate_database(databases,criteria):
    temp_database = Database('temp_database')
    for database in databases:
        for row in range(database.get_num_of_rows()):
            #print(database.get_row(row))
            add_row = True
            for j in range(len(criteria)):
                #print("criteria[j] != -1: ",criteria[j] != -1)
                if criteria[j] != -1 and criteria[j] != database.get_value_from_database(row,j):
                #    print("passing")
                    add_row = False
                    break
            if add_row:
                #print("adding: ",database.get_row(row))
                temp_database.add_row(database.get_row(row))
    return temp_database

def populate_temp_databases(databases,temp_databases,column,criteria):
    #this will need to be update to place items nicer
    for database in databases:
        for row in range(database.get_num_of_rows()):
            add_row = True
            #print("criteria: ", criteria)
            for j in range(len(criteria)):
                #print("criteria[%i]: %i" % (j,criteria[j]))
                #print("database.get_value_from_database(%i,%i): %i" % (row,j,database.get_value_from_database(row,j)))
                if criteria[j] != -1 and criteria[j] != database.get_value_from_database(row,j) and j != column:
                    #print("passing...")
                    add_row = False
                    break
                    
            if add_row:
                #print("adding: ", database.get_row(row))
                if database.get_value_from_database(row,column) == 1:
                    temp_databases[0].add_row(database.get_row(row))
                elif database.get_value_from_database(row,column) == 2:
                    temp_databases[1].add_row(database.get_row(row))
                elif database.get_value_from_database(row,column) == 3:
                    temp_databases[2].add_row(database.get_row(row))
    #for tdata in temp_databases:
    #    tdata.print_data()
    return temp_databases

def get_answer(dictionary):
    if 1 in dictionary:
        return "Yes"
    elif 0 in dictionary:
        return "No"
#sorted_columns is a binary array.  if 1 don't touch, it has been sorted
#          if it is a 0 then it hasn't been sorted
def create_databases(criteria, databases, sorted_columns, main_entropy,path):#databases,columns,master_databases,total_records,sorted_columns):
    #we want to check the last values give our search tree criteria
    #more to come
    classes = None

    temp_database = populate_database(databases,criteria)
    if temp_database.is_empty():
        print("There are no items in the database witht the currect search criteria ", criteria)
        print("Path: %s" % path)
        return
    
    classes = temp_database.get_column_information(temp_database.get_num_of_columns() -1, criteria)
    if len(classes) < 2:
        print("Path: %s ANSWER: %s" % (path,get_answer(classes)))
        return
    
    #get the best attribute to split off of
    best_column = select_next_best_attribute(databases, sorted_columns, main_entropy, criteria)
    print("BEST_COLUMN: %i" % (best_column))

    if best_column == -1:
        #if there are no more splits to occure we return
        print("can't determine an answer off of the current seach criteria ", criteria)
        print("Path: %s" % path)
        return

    temp_sorted_columns = copy.deepcopy(sorted_columns)
    temp_sorted_columns[best_column] = 1
    
    #we need to split the tree node and call again
    #get the number of nodes that we need
    num_of_nodes = get_num_of_nodes(databases,best_column,criteria)

    temp_databases = []
    
    for i in range(num_of_nodes):
        temp_databases.append(Database('temp_d%i'%i))
    
    #put the correct information in here
    temp_databases = populate_temp_databases(databases,temp_databases,best_column,criteria)
    for i in range(len(temp_databases)):
        print('\n--------------')
          
        path += ("Column: %s Attribute: %i -> " % (get_letter(best_column),i+1))
        print("When Column %s = %i" % (get_letter(best_column),i+1))
      
        print("going to option %i on columns %s" %(i+1,get_letter(best_column)))
        
        temp_criteria = copy.deepcopy(criteria)
        temp_criteria[best_column] = i+1
        
        create_databases(temp_criteria,databases,temp_sorted_columns,main_entropy,path)
    
def select_next_best_attribute(databases,selected_columns,main_entropy,criteria):

    maxgain = [-1,-1]

    #print(selected_columns)
    
    for i in range(databases[0].get_num_of_columns()-1):
        if selected_columns[i] == 1:
            continue
        entropy_dict = None
        results = []
        
        for database in databases:
            temp_dict = database.get_column_information(i, criteria)
            entropy_dict = update_dict(entropy_dict,temp_dict)
        ratio = float(database.get_num_of_rows()/total_records)
        temp_entropy = calculate_entropy(entropy_dict)
        results.append(temp_entropy*ratio)
        weighted_avg = 0
        for items in results:
            weighted_avg += items
        if maxgain[1] < weighted_avg - main_entropy and weighted_avg > 0:
            maxgain[0] = i
            maxgain[1] = weighted_avg - main_entropy
   
    return maxgain[0]

if __name__ == "__main__":

    #create the database objects
    d1 = Database("d1","dataset1.txt")
    d2 = Database("d2","dataset2.txt")
    d3 = Database("d3","dataset3.txt")

    d1.print_data()
    d2.print_data()
    d3.print_data()

    databases = [d1,d2,d3]

    sorted_columns = []
    for i in range(d1.get_num_of_columns()-1):
        sorted_columns.append(-1)
    #print(sorted_columns)
    
    #calculate entropy
    entropy_dict = None
    #get all the sumy and sumz
    #print(d1.get_num_of_columns())
    total_records = 0
    for database in databases:
        total_records += database.get_num_of_rows()
        temp_dict = database.get_column_information(database.get_num_of_columns()-1,sorted_columns)
        entropy_dict = update_dict(entropy_dict,temp_dict)
    main_entropy = calculate_entropy(entropy_dict)
    print("main entropy: %f" % main_entropy)
    
    create_databases(copy.deepcopy(sorted_columns),databases,sorted_columns, main_entropy, "")
 
