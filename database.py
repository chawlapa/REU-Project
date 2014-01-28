#this will simulate the database connections
import math


class Database():
    def __init__(self,filename):
        #self.name = name
        self.data = [] #this will be a 2D matrix
        self.populate_data(filename)

    def get_sum_of_column(self,column):
        retX = 0
        retY = 0
        for i in range(len(self.data)):
            if self.data[i][len(self.data[0])-1] == 1:
                retX += int(self.data[i][column])
            else:
                retY += int(self.data[i][column])

        return (retX,retY)

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

    def get_num_of_columns(self):
        return len(self.data[0])

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

    def print_data(self):
        print('------------')
        for item in self.data:
            print(item)
        print('------------')

def calculate_entropy(y,z):
    return( ((y)/(y+z))*math.log((y)/(y+z)) + ((z)/(y+z))*math.log((z)/(y+z))) *-1

if __name__ == "__main__":

    d1 = Database("dataset1.txt")
    d2 = Database("dataset2.txt")
    d3 = Database("dataset3.txt")

    #calculate entropy
    sumy = 0
    sumz = 0
    #get all the sumy and sumz

    sumx,sumy = d1.get_column_information(-1)
    entropy = calculate_entropy(sumx,sumy)
    print("DATA1: %f" % entropy)

    sumx,sumy = d2.get_column_information(-1)
    entropy = calculate_entropy(sumx,sumy)
    print("DATA2: %f" % entropy)

    sumx,sumy = d3.get_column_information(-1)
    entropy = calculate_entropy(sumx,sumy)
    print("DATA3: %f" % entropy)

    #get all the entropy for the entier system
    sumx = 0
    sumy = 0
    databases = [d1,d2,d3]
    print(d1.get_num_of_columns())
    for i in range(d1.get_num_of_columns()): #<-- this assumes all the databases have the same size
        for database in databases:
            x,y = database.get_sum_of_column(i)
            sumx += x
            sumy += y
            

    entropy = calculate_entropy(sumx,sumy)
    print("ALL: %f" % entropy)

    d1.print_data()
    d2.print_data()
    d3.print_data()
    
