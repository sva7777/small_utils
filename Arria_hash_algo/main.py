import json


def process_file(file_name):
    with open(file_name, "r") as file_stream:
        json_dict = json.load(file_stream)

    for entry in json_dict:
        yield entry


def calculate_hash(src_byte_0, dst_byte_0):
    a = int(src_byte_0)
    b = int(dst_byte_0)

    if a < 0 or a > 255:
        raise ValueError("src_byte_0 is not correct. It is <0 or >255")

    if b < 0 or b > 255:
        raise ValueError("src_byte_0 is not correct. It is <0 or >255")

    return a ^ b


def check_correctness_of_balancing(original_gen, balanced_files):
    for entry in original_gen:
        src_byte_0 = entry["Address A"].split(".")[-1]
        dst_byte_0 = entry["Address B"].split(".")[-1]

        print(
            "A:{}  B:{}  hash ={} ".format(
                entry["Address A"],
                entry["Address B"],
                calculate_hash(src_byte_0, dst_byte_0),
            )
        )


# ToDo: add code to pretict (function is known) output port for a packet.
# допустим 20 выходных портов
# 12.8 IP адресов на поддиапазон
# 00 - 12
# 01 - 13
# 02 - 13
# 03 - 13
# 04 - 13
# 05 - 12
# 06 - 13
# 07 - 13
# 08 - 13
# 09 - 13
# 10 - 12
# 11 - 13
# 12 - 13
# 13 - 13
# 14 - 13
# 15 - 12
# 16 - 13
# 17 - 13
# 18 - 13
# 19 - 13


if __name__ == "__main__":
    original_gen = process_file("original.json")

    balanced_files = []

    # ToDo: rewrite code. search files in directory. Order them

    balanced_files.append("1.json")
    balanced_files.append("2.json")
    balanced_files.append("3.json")
    balanced_files.append("4.json")

    print(len(balanced_files))

    check_correctness_of_balancing(original_gen, balanced_files)
