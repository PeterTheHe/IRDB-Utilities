# MADE WITH LOVE BY PETER AT IMPERIAL COLLEGE LONDON :) #

import os
import sqlite3


class EmbryoscopeDB:

    def __init__(self, path, create_directories=True):
        # init connection
        self.conn = sqlite3.connect(path)
        # should we create a folder structure for the output or just dump them all in the same folder
        self.create_directories = create_directories

    """ Get single image (from well, timestep and focal) """

    def extract_image(self, dest, well, timestep, focal, verbose=False):
        rows = self.conn.execute("SELECT Well,Run,Focal,Image FROM IMAGES WHERE Well == ? AND Run == ? AND Focal == ?",
                                 (well, timestep, focal))
        self.save_image_rows(rows, dest, verbose)

    """ Get images + sort into folders """

    def extract_images(self, dest, verbose=False):
        rows = self.conn.execute('SELECT Well,Run,Focal,Image FROM IMAGES')
        self.save_image_rows(rows, dest, verbose)

    """ Get single image from well and timestep at all focuses """

    def extract_image_by_timestep(self, dest, well, timestep, verbose=False):
        rows = self.conn.execute("SELECT Well,Run,Focal,Image FROM IMAGES WHERE Well == ? AND Run == ?",
                                 (well, timestep))
        self.save_image_rows(rows, dest, verbose)

    """ Return a list of values of all params with this name """

    def get_params_by_name(self, param):
        return list(map(lambda x: x[0], self.conn.execute('SELECT Val FROM GENERAL WHERE Par LIKE ?',
                                                          (param, )).fetchall()))

    """ Return a list of tuples of key/values of all params with this type """

    def get_params_by_type(self, param):
        return self.conn.execute('SELECT Par,Val FROM GENERAL WHERE Type LIKE ?',
                                 (param, )).fetchall()

    """ Save all the rows from a query """

    def save_image_rows(self, rows, dest, verbose=False):
        for row in rows:
            # extract data
            well = str(row[0])
            run = str(row[1])
            focal = str(row[2])
            img = row[3]

            # decide where to save
            filename = os.path.join(
                dest, "{}_{}_{}.jpg".format(well, run, focal))
            if self.create_directories:
                dir = os.path.join(dest, well, run)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                filename = os.path.join(dir, focal + '.jpg')

            if verbose:
                print('Extracting to ' + filename)
            # write to file
            f = open(filename, 'wb')
            f.write(img)
            f.close()
        rows.close()

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    # sample usage
    path = input('Database path: ')
    output = input("Give an EMPTY directory to extract images to: ")
    # connect to db
    db = EmbryoscopeDB(path, create_directories=False)
    # extract images from a specific well
    db.extract_image_by_timestep(output, well=3, timestep=2, verbose=True)
    # uncomment below to extract all the images in the db
    # db.extractImages(output)
