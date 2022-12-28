import re
import os
import glob
import subprocess
from pprint import pprint
from collections import namedtuple



FlowInfo = namedtuple('FlowInfo', 'ip_port_1 ip_port_2 frames_1 bytes_1 frames_2 bytes_2 total_frames total_bytes' )

class TSharkReportsFileNames:
    def __init__(self, file_name, temp_path):
        self._temp_path = temp_path
        self._file= os.path.splitext(os.path.basename(file_name))[0]

    def getDict(self):
        res = dict()
        res["ipv4"] = ("conv,ipv4", self._temp_path + "/" + self._file + ".ipv4")
        res["ipv6"] = ("conv,ipv6", self._temp_path + "/" + self._file + ".ipv6")
        res["udp"] = ("conv,udp", self._temp_path + "/" + self._file + ".udp")
        res["tcp"] = ("conv,tcp", self._temp_path + "/" + self._file + ".tcp")
        return res

    def getFileByKey(self, key):
        temp= self.getDict()
        tshark_param, filename = temp[key]
        return filename

    def __str__(self):
        return self._temp_path+ "/"+ self._file



def process_tshark_report(filename):
    file_input = open(filename,'r')

    re_comp = re.compile(r"(?P<ip_port_1>\S+) *<-> (?P<ip_port_2>\S+) *(?P<frames_1>\d+) *(?P<bytes_1>\d+) +(?P<frames_2>\d+) +(?P<bytes_2>\d+) +(?P<total_frames>\d+) +(?P<total_bytes>\d+)")
    for line in file_input:
        match_re = re.match(re_comp, line)
        if not match_re:
            continue
        yield FlowInfo(match_re.group('ip_port_1'), match_re.group('ip_port_2'), match_re.group('frames_1'), match_re.group('bytes_1'), match_re.group('frames_2'), match_re.group('bytes_2'), match_re.group('total_frames'), match_re.group('total_bytes') )



def get_tshark_reports_put_to_temp(filenames):

    if type(filenames) == str:
        filenames=[filenames]

    res =[]

    for file in filenames:
        temp = TSharkReportsFileNames(file, 'Temp_dir')
        for item in temp.getDict().values():
            key, file_name = item
            with open(file_name, "w") as output_file_handler:
                tshark_return_code = subprocess.run( ['tshark','-r', file, '-q', '-z', key, '-C', 'NoTunnels'], stdout=output_file_handler, stderr= subprocess.PIPE, encoding ='utf-8')
        res.append(temp)
    return res


def is_different_worker(original_info, balanced_info, key, ignore_bytesize):
    pprint("start check: {}".format(key))

    original_gen = process_tshark_report(original_info[0].getFileByKey(key))

    for original_line in original_gen:
        res = False

        for balanced_file in balanced_info:
            balanced_gen = process_tshark_report(balanced_file.getFileByKey(key))
            for balanced_line in balanced_gen:
                if ignore_bytesize:
                    if (original_line.ip_port_1 == balanced_line.ip_port_1 and original_line.ip_port_2 == balanced_line.ip_port_2 and
                        original_line.frames_1 == balanced_line.frames_1 and original_line.frames_2 == balanced_line.frames_2 and
                        original_line.total_frames == balanced_line.total_frames):
                            res = True
                            break
                else:
                    if original_line == balanced_line:
                        res = True
                        break

        if res== False:
            pprint("diff. Key = {}  Line ={}".format(key, original_line))
            return True

    return False





def check_result(original, balanced, ignore_bytesize= False):

    pprint("start IP+IP symmetrized check")

    pprint( is_different_worker(original, balanced, "ipv4", ignore_bytesize) )
    pprint(is_different_worker(original, balanced, "ipv6", ignore_bytesize))

    pprint("start 5 Turple check")
    pprint( is_different_worker(original, balanced, "tcp", ignore_bytesize) )
    pprint(is_different_worker(original, balanced, "udp", ignore_bytesize))

if __name__ == '__main__':

    # ToDo: add check what all unsupported files went to first port

    # clear temp directory
    temp_array = glob.glob("Temp_dir/*")
    for temp_file in temp_array:
        os.remove(temp_file)

    # search one pcap file in Original directry
    original_array = glob.glob("Original/*.pcap")

    # check what there is only one pcap file
    if len(original_array) != 1:
        pprint("В каталоге Original найдено {} pcap файлов, а ожидается один pcap файл".format(len(original_array)))
        exit(1)

    original_info= get_tshark_reports_put_to_temp(original_array)

    # search pcap files in Balanced directory
    balanced_array = glob.glob("Balanced/*.pcap")

    #check what there is at least one pcap file
    if len(balanced_array) == 0:
        pprint("В каталоге Balanced не найдено ни одного pcap файла")
        exit(1)


    # check what original file name doesn't exist in balances_array
    for item in balanced_array:
        if os.path.basename(item) == os.path.basename(original_array[0]):
            pprint("Совпадение имени исходного файла и файла после балансировки")
            exit(1)


    balanced_info = get_tshark_reports_put_to_temp(balanced_array)

    check_result(original_info, balanced_info, False)
