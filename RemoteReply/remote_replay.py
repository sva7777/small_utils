import json
import paramiko
import logging

from concurrent.futures import ThreadPoolExecutor


def main_worker(item):
    with connect_to_pc(item["ip"], item["user"], item["pass"]) as client:
        res = run_cmd(client, item["path"], item["tcpreplay_cmd"])
        logger.debug(
            "IP = {} \n команда :{} \n результат: \n {}".format(
                item["ip"], item["tcpreplay_cmd"], res
            )
        )
        return res


def main(devices):
    with ThreadPoolExecutor() as executor:
        res = executor.map(main_worker, devices)


def connect_to_pc(ip_addr, user, passwd, port=22):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip_addr, username=user, password=passwd, port=port)
    # stdin, stdout, stderr = client.exec_command(cmd)
    # stdin, stdout, stderr = client.exec_command('ls -l')
    # data = stdout.read() + stderr.read()
    # print(data)
    return client


def run_cmd(client, path, cmd):
    stdin, stdout, stderr = client.exec_command(f"cd {path}; {cmd}")
    # stdin, stdout, stderr = client.exec_command(cmd)
    data = stdout.read() + stderr.read()
    data = data.decode("utf-8")

    return data


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s- %(levelname)s - %(message)s", "%H:%M:%S"
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    with open("conf.json") as conf_file:
        data = json.load(conf_file)["pc"]

    main(data)
