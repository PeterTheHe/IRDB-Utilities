# MADE WITH LOVE BY PETER AT IMPERIAL COLLEGE LONDON :) #

import os
import sqlite3

class EmbryoscopeUtils:

    def __init__(self, path, createDirectories = True):
        #init driver
        self.conn = sqlite3.connect(path)
        self.createDirectories = createDirectories

    def extractImage(self, dest, well, timestep, focal, verbose = False):
        #Get single image (from well, timestep and focal)
        rows = self.conn.execute("SELECT Well,Run,Focal,Image FROM IMAGES WHERE Well == ? AND Run == ? AND Focal == ?", \
            (well, timestep, focal))
        self.saveImageRows(rows, dest, verbose)

    def extractImages(self, dest, verbose = False):
        #Get images + sort into folders
        rows = self.conn.execute('SELECT Well,Run,Focal,Image FROM IMAGES')
        self.saveImageRows(rows, dest, verbose)

    def extractImageByTimestep(self, dest, well, timestep, verbose = False):
        #Get single image from well and timestep at all focuses
        rows = self.conn.execute("SELECT Well,Run,Focal,Image FROM IMAGES WHERE Well == ? AND Run == ?", \
            (well, timestep))
        self.saveImageRows(rows, dest, verbose)

    def getParamsByName(self, param):
        #Returns a list of values of all params with this name
        return list(map(lambda x: x[0], self.conn.execute('SELECT Val FROM GENERAL WHERE Par LIKE ?', \
            (param, )).fetchall()))

    def getParamsByType(self, param):
        #Returns a list of tuples of key/values of all params with this type
        return self.conn.execute('SELECT Par,Val FROM GENERAL WHERE Type LIKE ?', \
            (param, )).fetchall()

    def saveImageRows(self, rows, dest, verbose = False):
        #Saves all the rows from a query
        for row in rows:
            #extract data
            well = str(row[0])
            run = str(row[1])
            focal = str(row[2])
            img = row[3]
            
            #Decide where to save
            filename = os.path.join(dest, "{}_{}_{}.jpg".format(well, run, focal))      
            if self.createDirectories:
                dir = os.path.join(dest, well, run)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                filename = os.path.join(dir, focal + '.jpg')

            if verbose:
                print('Extracting to ' + filename)
            #write to file
            f = open(filename, 'wb')
            f.write(img)
            f.close()
        rows.close()

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    # Sample usage
    path = input('Database path: ')
    output = input("Give an EMPTY directory to extract images to: ")
    eu = EmbryoscopeUtils(path, False)
    print('Working on data from PatientIDx ' + str(eu.getParamsByName('PatientIDx')[0]))
    #eu.extractImages(output, True)
    eu.extractImageByTimestep(output, well=3, timestep=2, verbose=True)
