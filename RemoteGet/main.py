# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import json
import os
import pexpect


if __name__ == "__main__":
    with open("conf.json") as conf_file:
        temp_data = json.load(conf_file)
        data = temp_data["pc"]
        store_dir = temp_data["store_dir"]

    # check if store directory exists. If don't exist then create it
    if os.path.isdir(store_dir) == False:
        os.mkdir(store_dir)

    for line in data:
        test = "scp {user}@{ip}:{remotepath}/{filename} {wheretostore}".format(
            passw=line["pass"],
            user=line["user"],
            ip=line["ip"],
            remotepath=line["remotepath"],
            filename=line["filename"],
            wheretostore=store_dir + "/" + line["ip"] + "_" + line["filename"],
        )

        print(test)

        child = pexpect.spawn(test, timeout=3)
        child.expect("password:")
        child.sendline(line["pass"])
        child.expect(pexpect.EOF)
        child.close()
