# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
from enum import Enum

class TypeOfCompare(Enum):
    IP = 1
    TCP_OR_UDP =2

def process_file(file_name):
    with open(file_name, 'r') as file_stream:
        json_dict = json.load(file_stream)

    for entry in json_dict:
        yield entry

def compare_files(fileoriginal_gen , balanced_files, compare) :

    for entry in fileoriginal_gen:
        res = False
        for filename in balanced_files:
            gen = process_file(filename)

            for inner_entry in gen:
                if compare == TypeOfCompare.IP:
                    if entry['Address A'] == inner_entry['Address A'] and \
                        entry['Address B'] == inner_entry['Address B'] and \
                        entry['Пакеты'] == inner_entry['Пакеты'] :
                        res = True
                        break;
                elif compare == TypeOfCompare.TCP_OR_UDP:
                    if entry['Address A'] == inner_entry['Address A'] and \
                        entry['Address B'] == inner_entry['Address B'] and \
                        entry['Пакеты'] == inner_entry['Пакеты'] and \
                        entry['Port A'] == inner_entry['Port A'] and \
                        entry['Port B'] == inner_entry['Port B'] :
                        res = True
                        break;
                else:
                    print("unsupported compare type")

        if res == False:
            print(str(entry)+'\n');



if __name__ == '__main__':

    balanced_files = []

    original_gen= process_file('original.json')

    balanced_files.append( "1.json" )
    balanced_files.append( "2.json" )
    balanced_files.append( "3.json" )
    balanced_files.append( "4.json" )

    compare_files(original_gen, balanced_files, TypeOfCompare.TCP_OR_UDP )





