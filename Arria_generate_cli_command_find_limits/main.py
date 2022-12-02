import ipaddress

def add_multi_ip(network, count):
    array= [str(ip) for ip in ipaddress.IPv4Network(network)]

    for i in range(1,count+1):
        print('configure interface 1 rule add ip={} to 3 type=direct status=active name="test"'.format(array[i]))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    add_multi_ip("192.169.0.0/16",253)
