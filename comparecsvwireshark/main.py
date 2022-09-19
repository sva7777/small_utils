# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re


def process_file(file_name, col_number):
    fileinput= open(file_name,'r')
    fileoutput=open('write_'+file_name,'w')

    for line in fileinput:
        re_comp= re.compile(r"\"Address A\",\"")
        match_re= re.match(re_comp, line )
        if match_re:
            continue
        test = line.split(",",col_number)
        if len(test) >col_number :
            substring = ''
            for i in range(col_number):
                substring = substring + test[i]+','

            yield substring


def compare_files(fileoriginal_gen , colnumber, temp_write_files) :

    for line in fileoriginal_gen:
        # find line from original
        res = False
        for filename in temp_write_files:
            gen = process_file(filename,colnumber)

            for line1 in gen:
                if line == line1:
                   res = True
                   break;


        if res == False:
            print(line+'\n');



if __name__ == '__main__':
    # for ethernet and IP colnumber==3,  for udp and tcp colnumber==5
    colnumber = 5

    temp_result_files = []

    original_gen= process_file('original.csv',colnumber)

    temp_result_files.append( "1.csv" )
    temp_result_files.append( "2.csv" )
    temp_result_files.append( "3.csv" )

    compare_files(original_gen, colnumber, temp_result_files)





