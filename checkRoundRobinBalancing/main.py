import os
import glob
from pprint import pprint
from scapy.all import *


def remove_padding(packet):
    if "Padding" in packet:
        del packet["Padding"]
    return packet


def worker_compare(original, balanced, ignore_paddding):
    scapy_original = PcapReader(original[0]).read_all()
    scapy_balanced = []

    balanced_total_packets_count = 0
    for balanced_item in balanced:
        temp_scapy_reader = PcapReader(balanced_item).read_all()
        balanced_total_packets_count += len(temp_scapy_reader)
        scapy_balanced.append(temp_scapy_reader)

    if len(scapy_original) != balanced_total_packets_count:
        pprint(
            "Не совпадает количество пакетов в исходном файле ({}) и балансировки ({})".format(
                len(scapy_original), balanced_total_packets_count
            )
        )
        exit(1)

    # убираем padding если требуется
    if ignore_paddding:
        for packet in scapy_original:
            # не нравится вот так далеть, но работает
            packet = remove_padding(packet)

        for balanced_item in scapy_balanced:
            for packet in balanced_item:
                # не нравится вот так далеть, но работает
                packet = remove_padding(packet)

    # начинается основная работа

    count = 0
    for original_packet in scapy_original:
        found = False
        count += 1
        for balanced_item in scapy_balanced:
            for balanced_packet in balanced_item:
                if original_packet == balanced_packet:
                    found = True
                    break

            if found:
                break

        if not found:
            pprint(
                "Не найдет пакет номер {} , его содержимое {}".format(
                    count, original_packet
                )
            )
            exit(1)

    pprint("Все ок")


if __name__ == "__main__":
    # ToDo: не будет проверки ситуации когда в исходнм pcap есть дублирующие пакеты.

    # search one pcap file in Original directry
    original_array = glob("Original/*.pcap")

    # check what there is only one pcap file
    if len(original_array) != 1:
        pprint(
            "В каталоге Original найдено {} pcap файлов, а ожидается один pcap файл".format(
                len(original_array)
            )
        )
        exit(1)

    # search pcap files in Balanced directory
    balanced_array = glob("Balanced/*.pcap")

    # check what there is at least one pcap file
    if len(balanced_array) == 0:
        pprint("В каталоге Balanced не найдено ни одного pcap файла")
        exit(1)

    # check what original file name doesn't exist in balances_array
    for item in balanced_array:
        if os.path.basename(item) == os.path.basename(original_array[0]):
            pprint("Совпадение имени исходного файла и файла после балансировки")
            exit(1)

            # ignore_paddding
    worker_compare(original_array, balanced_array, True)
