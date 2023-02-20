# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import glob
from enum import Enum
from pprint import pprint

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
            pprint(str(entry)+'\n');



if __name__ == '__main__':

    balanced_files = []

    # search one pcap file in Original directry
    original_array = glob.glob("Original/*.json")

    # check what there is only one json file
    if len(original_array) != 1:
        pprint("В каталоге Original найдено {} json файлов, а ожидается один pcap файл".format(len(original_array)))
        exit(1)

    # search pcap files in Balanced directory
    balanced_array = glob.glob("Balanced/*.json")

    # search pcap files in Balanced directory
    balanced_array = glob.glob("Balanced/*.json")

    original_gen= process_file(original_array[0])

    compare_files(original_gen, balanced_array, TypeOfCompare.TCP_OR_UDP )





