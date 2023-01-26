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
from datetime import date

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
    # Read particle star file 1 and star file 2
    filename1 = '1st_selection_particles.star'
    filename2 = '2nd_selection_particles.star'
    first = Star(filename=filename1)
    second = Star(filename=filename2)

    # Get particle IDs from both star files using rlnImageName column
    first_particle_names = first.dataframes[1]["rlnImageName #8"]
    len_first = len(first_particle_names)
    second_particle_names = second.dataframes[1]["rlnImageName #8"]
    len_second = len(second_particle_names)

    # Calculate the intersection, i.e. particles IDs that are found in both columns
    intersection = pd.Series(list(set(first_particle_names) & set(second_particle_names)))
    len_intersect = len(intersection)

    # Print results and save in file
    today = date.today()
    date_string = today.strftime("%y%m%d")

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