from netaddr import *
initinal_number = 3232235521

def print_hi(count, groupby):
    i = 0

    while i < count:
        if i % groupby == 0:
            print("-------------------------------------")

        test = IPAddress(initinal_number + i)
        test_str = str(test)
        test_dict = test_str.split(".")

        # ToDo: Нужно переделать это говно, нужно учитывать маску и считать broadcast и network правильно
        if test_dict[3] == "0"
            count = count + 1
            i = i + 1
            continue
        if test_dict[3] == "255":
            count = count + 1
            i = i + 1
            continue

        print(test_str)

        i = i + 1


if __name__ == "__main__":
    print_hi(4096, 256)
