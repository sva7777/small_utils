from scapy.all import *
from pprint import pprint


# ToDo: move this function into shared library. It is used by checkRoundRobinBalancing also
def remove_padding(packet):
    if "Padding" in packet:
        del packet["Padding"]
    return packet


def compare(originalfile, replays, ignore_padding=False):
    # PcapReader generator

    scapy_orig = PcapReader(originalfile)
    scapy_repl = PcapReader(replays)

    count = 1

    for packet_1, packet_2 in zip(scapy_orig, scapy_repl):
        packet_1.time = None
        packet_2.time = None

        if ignore_padding:
            packet_1 = remove_padding(packet_1)
            packet_2 = remove_padding(packet_2)

        if packet_1 != packet_2:
            pprint("Разница в пакете номер:" + str(count))
            return

        # pprint("сравнил пакет: " +str(count))
        count = count + 1
    pprint("Содержимое файлов совпадает")


def find_packet(one, bigfile):
    scapy_one = PcapReader(one)
    scapy_bigfile = PcapReader(bigfile)

    count = 1

    packet_1 = next(scapy_one)
    packet_1.time = None

    for packet_2 in scapy_bigfile:
        packet_2.time = None
        if packet_1 == packet_2:
            pprint("Пакет найден в позиции:" + str(count))
            return
        count = count + 1
    pprint("пакет не найден")


def compare_two_packets(file1, file2):
    scapy_one = PcapReader(file1)
    scapy_two = PcapReader(file2)

    packet_1 = next(scapy_one)
    packet_1.time = None
    packet_2 = next(scapy_two)
    packet_2.time = None

    if packet_1 == packet_2:
        pprint("пакеты равные")
    else:
        pprint("пакеты не равны")
        pprint(packet_2)


if __name__ == "__main__":
    compare("original.pcap", "captured.pcap", True)
    # переписать код, так что бы сразу искали
    # find_packet("one.pcap","captured.pcap")
    # compare_two_packets("packet_small.pcap","packet_big.pcap")
