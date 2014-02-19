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

    '''  --------is_empty--------
         called to make sure the database has data
         Inputs: none
         Output: boolean value if there is data or not
    '''
    def is_empty(self):
        if self.data == []:
            return True
        else:
            return False

    '''  --------get_sum_of_decisions--------
         returns an x and y for a certain column based on the average
         Inputs: column integer and a search criteria list
         Output: a pair of x and y values
         Note: This should only be called from get_coloumn_information
    '''
    def get_sum_of_decisions(self,column,criteria):
        keys = []
        for i in range(len(self.data)):
            if self.data[i][column] not in keys:
                keys.append(self.data[i][column])

        rDict = dict.fromkeys(keys)
        for i in range(len(self.data)):
            #check the criteria on the row
            increment = True
            for j in range(len(criteria)):
                if criteria[j][0] != -1 and criteria[j][0] != self.data[i][j]:
                    increment = False
            if increment:
                if rDict.get(self.data[i][column]) == None:
                    rDict[self.data[i][column]] = 1
                else:
                    rDict[self.data[i][column]] += 1
        return (rDict)

    '''  --------get_sum_of_column--------
         returns an x and y for a certain column based on the average
         Inputs: column integer and a search criteria list
         Output: a pair of x and y values
         Note: This should only be called from get_coloumn_information
    '''
    def get_sum_of_column(self,column,criteria):
        #print("get sum of column: %i" % column)
        #keys = []
        #total = 0
        #records = 0
        
        #print("keys: ", keys)
            
        key1 = '<'
        key2 = '>='
        #measuring_stick = keys[int(len(keys)/2)]
        keys = []
        keys.append(key1)
        keys.append(key2)
        #print("keys: ", keys)

        values = []
        #print("criteria: ", criteria)
        for i in range(len(self.data)):
            #print("data: %f" % self.data[i][column])
            if criteria[column][0] == -1 or (criteria[column][0] == '<' and self.data[i][column] < criteria[column][1]) or (criteria[0] == '>=' and self.data[i][column] >= criteria[column][1]):
                #print("  append the value")
                values.append(self.data[i][column])
        values.sort()
        #print("values: ",values)
        value = values[int(len(values)/2)]
        #print("value: %f" % value)
        rDict = dict.fromkeys(keys)
        for i in range(len(self.data)):
            #check the criteria on the row
            greater_increment = True
            less_increment = True
            
            for j in range(len(criteria)):
                if criteria[j][0] != -1 and criteria[j][0] == '<' and self.data[i][j] >= criteria[j][1]:
                    less_increment = False
                elif criteria[j][0] != -1 and criteria[j][0] == '>=' and self.data[i][j] < criteria[j][1]:
                    greater_increment = False

            if less_increment and self.data[i][column] < value:
                if rDict.get(key1) == None:
                    rDict[key1] = 1
                else:
                    rDict[key1] += 1
            elif greater_increment and self.data[i][column] >= value:
                if rDict.get(key2) == None:
                    rDict[key2] = 1
                else:
                    rDict[key2] += 1
            
        return (rDict)

    '''  --------get_column_information--------
         Called from the outside to get values for a specific column
         Inputs: a column value.  if a -1 is passed it in, it will get
                 infomration from the entire database
                 also need to pass in a search criteria array
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

    '''  --------get_column_unique_ident--------
         returns length of unique keys in a column
         Inputs: column and search criteria
         Output: the length
    '''
    def get_column_unique_ident(self,column,criteria):
        rDict = self.get_sum_of_column(column,criteria)
        return len(rDict)

    '''  --------get_num_of_columns--------
         returns the number of attributes + 1
         Inputs: None
         Output: the number of attributes
         Note: Make sure you take the value and subtract by 1 if you don't want the last column
    '''
    def get_num_of_columns(self):
        return len(self.data[0])

    '''  --------get_num_of_rows--------
         returns the number of rows
         Inputs: None
         Output: the number of rows
    '''
    def get_num_of_rows(self):
        return len(self.data)

    '''  --------get_class_of_row--------
         returns the class of the row
         Inputs: row
         Output: the class
    '''
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
                        
                        temp.append(float(item.strip())) #get rid of whitespace
                    self.data.append(temp)
        except Exception as err:
            print(err)

    '''  --------add_row--------
         add row to the data base
         Inputs: row
         Output: None
    '''
    def add_row(self,row):
        self.data.append(row)

    '''  --------get_class_of_row--------
         returns the row from the database
         Inputs: row number
         Output: the row
    '''
    def get_row(self,row):
        return self.data[row]

    '''  --------get_value_from_database--------
         returns the value from the database
         Inputs: row and column
         Output: the value
    '''
    def get_value_from_database(self,row,column):
        return self.data[row][column]

    def get_values(self,column):
        keys = []
        for i in range(len(self.data)):
            keys.append(self.data[i][column])
        return keys

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

'''------END OF DATABASE CLASS-----------'''




'''  --------calculate_entropy--------
     Calculates the entropy from the pair of values
     Inputs: the x and y value
     Output: The entropy as a float
'''
def calculate_entropy(entropy_dict):
    total = 0
    for key,value in entropy_dict.items():
        if value != None:
            total += value
    entropy = 0
    for key,value in entropy_dict.items():
        if value == None: 
            continue
        entropy += ((value/total)*(math.log(value/total)))
    return (entropy * -1)

'''  --------update_dict--------
     Joins two dictionaries
     Inputs: the x and y value
     Output: The entropy as a float
'''
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

'''  --------get_letter--------
     Gives the letter for the interger given
     Inputs: a value
     Output: a letter
     Note: This will not work for letters abouve 26.  This needs to be fixed
'''
def get_letter(value):
    return chr(value + 65)

'''  --------get_num_of_nodes--------
     Gives the number of nodes that should be spawned from the data set
     Inputs: the databases, column that spawns data and search criteria
     Output: the numebr of nodes
'''
def get_num_of_nodes(databases,column,criteria):
    # this has been changed to always give back 2
    return 2
    #num_of_nodes = 0
    #for database in databases:
        #num = database.get_column_unique_ident(column,criteria)
        #if num > num_of_nodes:
            #num_of_nodes = num
    #return num_of_nodes

'''  --------populate_database--------
     Puts information into a database off of the search criteria
     Inputs: the databases and search criteria
     Output: the database
'''
def populate_database(databases,criteria):
    temp_database = Database('temp_database')
    #print("Criteria: ",criteria)
    for database in databases:
        for row in range(database.get_num_of_rows()):
            bool1 = True
            bool2 = True
            add_row = True
            
            for j in range(len(criteria)):
                #print("criteria[j][0]: %s" % (criteria[j][0]))
                #print("criteria[j][1]: ", criteria[j][1])
                #print("value: %f" % database.get_value_from_database(row,j))
                if criteria[j][0] == -1:
                    continue
                elif criteria[j][0] == '<' and database.get_value_from_database(row,j) < float(criteria[j][1]):
                    continue
                elif criteria[j][0] == '>=' and database.get_value_from_database(row,j) >= float(criteria[j][1]):
                    continue
                else:
                    add_row = False
                #if criteria[j][0] != -1 or criteria[j][0] == '<' and database.get_value_from_database(row,j) >= criteria[j][1]:
                #    bool1 = False
                #elif criteria[j][0] != -1 or criteria[j][0] == '>=' and database.get_value_from_database(row,j) < criteria[j][1]:
                #    bool2 = False
            if add_row:
                temp_database.add_row(database.get_row(row))
    return temp_database

'''  --------populate_temp_databases--------
     Creates all the node databases give the column to spawn and serach criteria
     Inputs: the databases, temp_databases, column to spawn off of and search criteria
     Output: the temporary databases
'''
def populate_temp_databases(databases,temp_databases,column,criteria):
    #this will need to be update to place items nicer
    #print("populating database with this criteria: " , criteria)
    value = get_value_to_sort(databases, column)
    for database in databases:
        for row in range(database.get_num_of_rows()):
            add_greater_row = True
            add_lesser_row = True

            for j in range(len(criteria)):
                if criteria[j][0] != -1 or criteria[j][0] == '<' and database.get_value_from_database(row,j) >= criteria[j][1]:
                    add_lesser_row = False
                if criteria[j][0] != -1 or criteria[j][0] == '>=' and database.get_value_from_database(row,j) < criteria[j][1]:
                    add_greater_row = False

            if add_greater_row and database.get_value_from_database(row,column) >= value:
                temp_databases[1].add_row(database.get_row(row))
            elif add_lesser_row and database.get_value_from_database(row,column) < value:
                temp_databases[0].add_row(database.get_row(row))

    return temp_databases

'''  --------get_answer--------
     Gives the answer to the class of the database
     Inputs: the dictionary containg the database classes
     Output: the answer
'''
def get_answer(dictionary):
    if 1 in dictionary:
        return "Yes"
    elif 0 in dictionary:
        return "No"
    
def get_value_to_sort(databases,column):
    master_keys = []
    for database in databases:
        keys = database.get_values(column)
        for key in keys:
            master_keys.append(key)
    master_keys.sort()
    return master_keys[int(len(master_keys)/2)]
        

'''  --------id3_distributed--------
     recursive function that splits the databases and does the heavy lifting
     Inputs: the search criteria, the databases, the list to keep track of which columns have been spawned, the
             main_entropy, and the search path
     Output: None
'''
def id3_distributed(criteria, databases, sorted_columns, main_entropy,path):#databases,columns,master_databases,total_records,sorted_columns):
    #we want to check the last values give our search tree criteria
    #more to come
    classes = None

    temp_database = populate_database(databases,criteria)
    #temp_database.print_data()
    if temp_database.is_empty():
        print("There are no items in the database witht the currect search criteria ", criteria)
        print("Path: %s" % path)
        return
    
    classes = temp_database.get_sum_of_decisions(temp_database.get_num_of_columns() -1, criteria)
    
    if classes == None:
        print("ERROR THE CLASS IS NONE")
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

        temp_path = copy.deepcopy(path)
        temp_path += ("Column: %s Attribute: %i -> " % (get_letter(best_column),i+1))
        
        
        
        temp_criteria = copy.deepcopy(criteria)
        value = get_value_to_sort(databases,best_column)
        #print("value: %f" % value)
        if i == 0:
            temp_criteria[best_column][0] = '<'
            temp_criteria[best_column][1] = value
        elif i ==1:
            temp_criteria[best_column][0] = '>='
            temp_criteria[best_column][1] = value
        #print("temp_criteria: ",temp_criteria)
        print("When Column %s = %s%f" % (get_letter(best_column),temp_criteria[best_column][0],temp_criteria[best_column][1]))
      
        print("going to option %i on columns %s" %(i+1,get_letter(best_column)))
            
        id3_distributed(temp_criteria,databases,temp_sorted_columns,main_entropy,temp_path)

'''  --------select_next_best_attribute--------
     gives the best attribute that you should sort off of given parameters
     Inputs: the databses, list of columns that you can spawn off of, the main entropy, and the search criteria
     Output: the column to spawn off of
'''    
def select_next_best_attribute(databases,selected_columns,main_entropy,criteria):

    maxgain = [-1,-1]
    #print("Selecting next best attribute")
    #print("Selected Columns: ",selected_columns)
    
    for i in range(databases[0].get_num_of_columns()-1):
        #print("Column: %i" % i)
        if selected_columns[i] == 1:
            continue
        entropy_dict = None
        results = []
        
        for database in databases:
            temp_dict = database.get_column_information(i, criteria)
            #print("  temp_dict ", temp_dict)
            entropy_dict = update_dict(entropy_dict,temp_dict)
            #print("  entropy_dict ", entropy_dict)
        ratio = float(database.get_num_of_rows()/total_records)
        temp_entropy = calculate_entropy(entropy_dict)
        #print(temp_entropy)
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
    d1 = Database("s1","seed1.txt")
    d2 = Database("s2","seed2.txt")
    d3 = Database("s3","seed3.txt")

    #show all of the information in the databases
    d1.print_data()
    d2.print_data()
    d3.print_data()

    #put the databases in a list
    databases = [d1,d2,d3]

    #create a list that keeps track of which columns have been selected to splpit off of
    sorted_columns = []
    criteria = []
    for i in range(d1.get_num_of_columns()-1):
        sorted_columns.append(-1)
        criteria.append([-1,None])
    
    #calculate entropy
    entropy_dict = None
    total_records = 0
    for database in databases:
        total_records += database.get_num_of_rows()
        temp_dict = database.get_sum_of_decisions(database.get_num_of_columns()-1,criteria)
        print("  temp_dict ", temp_dict)
        entropy_dict = update_dict(entropy_dict,temp_dict)
        print("  entropy_dict ", entropy_dict)
    main_entropy = calculate_entropy(entropy_dict)
    print("main entropy: %f" % main_entropy)



    #split that databases to make a decision tree
    id3_distributed(criteria,databases,sorted_columns, main_entropy, "")
 
