'''
1st selection: 3DC, 1050co distance, ftrless
    - 53142 particles
    - based on 184253 particles (J20 384b1_bs_2)
    - based on 2DC of 299556 particles (Extract/384b1_notrash_wide)
    - based on 2DC of 777793 particles (Class2D/768bin3, everything but trash)

2nd selection: 3DC, 971co distance, ftrless
    - 55031 particles
    - based on 184253 particles (J20 384b1_bs_2)
    - based on 2DC of 299556 particles (Extract/384b1_notrash_wide)
    - based on 2DC of 777793 particles (Class2D/768bin3, everything but trash)

'''

import pandas as pd
import numpy as np
import glob
from datetime import date
# regular dict functions the same way (being ordered) but backwards compatibility is an issue
from collections import OrderedDict

'''
USAGE TO BE WRITTEN LELMAO

'''


class Star:

    def __init__(self, filename=''):
        # Initialize parser
        self.lines = list()
        self.datablocks = list()
        self.datapairs = dict()
        self.filename = filename
        self.dataframes = list()
        # Read .star file
        if filename != '':
            self.read()

    def __str__(self):
        print(self.dataframes)
        print(self.dataframe_to_string(self.dataframes[0]))
        return ':)'

    def read(self):
        # Reads rln star file and saves data into an internal dataframe.
        self.read_file(self.filename)
        self.parse_lines()
        self.parse_datablocks()

    def read_file(self, file):
        # Read file and saves lines in lines and orig_lines
        with open(file) as fin:
            self.lines = fin.readlines()

    def parse_lines(self):
        # Parses lines for loops
        datablock = []
        in_datablock = False
        for line in self.lines:
            line = line.strip()
            if line == "loop_":
                in_datablock = True
                datablock = []
                continue
            if line == '' and in_datablock:
                in_datablock = False
                self.datablocks.append(datablock)
                continue
            if line == '':
                continue
            if in_datablock:
                datablock.append(line)
                continue
        if in_datablock:
            self.datablocks.append(datablock)

    def parse_datablocks(self):
        # Converts .star loop into a panda dataframe
        for datablock in self.datablocks:
            loop = dict()
            col_names = []
            for line in datablock:
                line = line.strip()
                if line[0] == '_':
                    col_names.append(line[1:])
                    loop[line[1:]] = []
                else:
                    values = line.split()
                    for i in range(len(col_names)):
                        loop[col_names[i]].append(values[i])
            df = pd.DataFrame(loop)
            self.dataframes.append(df)

    def dataframe_to_string(self, dataframe):
        # Converts dataframe into a .star file compatible string
        # Conversion of dataframe into fragments
        columns = [*dataframe]
        tostring = 'data_\nloop_' + '\n'
        for colname in columns:
            tostring += '_' + colname + '\n'
        tostring += dataframe.to_string(index=False, header=False)
        tostring += '\n'
        return tostring


if __name__ == '__main__':

    # Getting all particle IDs
    particle_groups = OrderedDict()
    for file in sorted(glob.glob("*.star")):
        print("Found " + file + ".")
        parser = Star(filename=file)
        particle_series = parser.dataframes[1]["rlnImageName #8"]
        # Saving particle ID list as well as length as an entry in particle groups dict
        particle_groups[file] = particle_series

    # Analyze particle identities between groups
    # Save identities (total & percentage) in array
    colnames = list(particle_groups.keys())
    num_matrix = np.ndarray([len(colnames), len(colnames)])
    perc_matrix = np.ndarray([len(colnames), len(colnames)])
    numResults = pd.DataFrame(data=num_matrix)
    percResults = pd.DataFrame(data=perc_matrix)
    # Calculate particle overlap between all groups and save in matrix
    for i in range(len(colnames)):
        total_num = len(particle_groups[colnames[i]])
        for j in range(len(colnames)):
            # Calculate overlap between two groups (first and second)
            first = particle_groups[colnames[i]]
            second = particle_groups[colnames[j]]
            result = pd.Series(np.intersect1d(first, second))
            # Save result in matrix
            numResults.loc[i, j] = len(result)
            percResults.loc[i, j] = len(result) / total_num
    # Rename columns and rows (row is index)
    numResults.columns = colnames
    numResults.index = colnames
    percResults.columns = colnames
    percResults.index = colnames
    print(numResults)
    print(percResults)

    # Calculate total overlap (anything else to compare?)
    all_series = []
    for series in colnames:
        all_series.append(set(particle_groups[series]))
    sets = map(set, all_series)
    total_overlap = len(set.intersection(*sets))
    print(total_overlap)

    # Print results and save in file
    today = date.today()
    date_string = today.strftime("%y%m%d")
    '''
    # Calculate the intersection, i.e. particles IDs that are found in both columns
    intersection = pd.Series(list(set(first_particle_names) & set(second_particle_names)))
    len_intersect = len(intersection)
    
    outfile = date_string + '_particle_identity_check.txt'
    report_string = "Created on " + date_string + "\n"
    report_string += "Filename 1: " + filename1 + "\n"
    report_string += "     NumParticles: " + str(len_first) + "\n"
    report_string += "Filename 2: " + filename2 + "\n"
    report_string += "     NumParticles: " + str(len_second) + "\n"
    report_string += "NumParticles found in both .star files: " + str(len_intersect) + "\n"
    report_string += "     PercentageIdentity: " + "File 1: " + str(len_intersect / len_first * 100) + \
                     "% ; File 2: " + str(len_intersect / len_second * 100) +"%\n"
    with open(outfile, "w") as fout:
        fout.write(report_string)
    '''