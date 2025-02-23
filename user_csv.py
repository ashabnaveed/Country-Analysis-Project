# user_csv.py
# ENDG 233 F24
# Ashab Naveed and Nawfal Cheema
# 441
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.
import os, sys

def read_csv(filename, include_header=True):

    """
    Reads a CSV file and returns the data as a list of rows.

    Arguments:
        filename -- The name of the file being read.
    
    Optional Arguments:
        include_header -- Indicates if the header should be returned with the data; assumed to be true

    Returns:
        data: 2D array of read information from text.
    
    """

    filename = filename.replace('.csv', '')

    data = []

    with open(f'data_files/{filename}.csv', 'r') as file:
        lines = file.readlines()

        if include_header:
            start_line = 0
        else:
            start_line = 1

        for i in range(start_line, len(lines)):
            line = lines[i].strip()
            values = line.split(',')

            row = []

            for value in values:
                if value.isdigit():
                    row.append(float(value))
                else:
                    row.append(value)
            
            data.append(row)
    
    return data


def write_csv(filename, data, overwrite=False):
    
    """ 
    Writes data to a CSV file 

    Arguments:
        Filename -- The name of the file being written to.
        Data -- A 2D List Containing the data to write.
        
    Optional Arguments:
        Overwrite: Overwriting or appending to the file, default is appending.

    Returns:
        N/A (Updates a file)

    """
    filename = filename.replace('.csv', '')

    if overwrite:
        mode = "w" # Write mode
    else:
        mode = "a" # Append mode
    
    file = open(f'data_files/{filename}.csv', mode)

    for row in data:
        input_line = '' # Blank string for the added line

        for index, i in enumerate(row):
            input_line += str(i)

            if index != len(row) - 1:
                input_line += ','
        
        input_line += '\n'

        file.write(input_line)

    file.close()


##TESTING THE CODE
write_csv('test', [["apple", 1, 1.1, "ba na na", 2, 2.2, "cherry", 3, 3.3, "date", 4, 4.4], ["elephant", 5, 5.5, "fig", 6, 6.6, "grape", 7, 7.7, "honeydew", 8, 8.8],], overwrite=True)
print(read_csv('test.csv'))

    
    

    

