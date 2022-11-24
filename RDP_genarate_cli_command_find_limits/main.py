import ipaddress


def set_filters_drop(count):

    array= [str(ip) for ip in ipaddress.IPv4Network("10.0.0.0/16")]


    for i in range(count):
        print("set packet-broker flow vasily{} match from-port p2-1".format(i))
        print("set packet-broker flow vasily{} match src-ip {}".format(i,array[i]))
        print("set packet-broker flow vasily{} match priority {}".format(i,i))
        print("set packet-broker flow vasily{} drop".format(i))
        #print("set packet-broker flow vasily{} to-port p50-1".format(ii))

def del_filters(count):
    for i in range(count):
        print("del packet-broker flow rule_{}".format(i))

def link_group(count):
    for i in range(count):
        print("set packet-broker link-group vasily{}".format(i))

def del_link_group(count):
    for i in range(count):
        print("del packet-broker link-group vasily{}".format(i))


def share_group(count):
    for i in range(count):
        print("set packet-broker share-group vasily{}".format(i))

def del_share_group(count):
    for i in range(count):
        print("del packet-broker share-group vasily{}".format(i))

def filters_balance(count):
    array= [str(ip) for ip in ipaddress.IPv4Network("10.0.0.0/16")]

    for i in range(count):
        print("set packet-broker flow vasily{} match from-port p1-1".format(i))
        print("set packet-broker flow vasily{} match src-ip {}".format(i,array[i]))
        print("set packet-broker flow vasily{} match priority {}".format(i,i))
        print("set packet-broker flow vasily{} to-balance-group vasily{}".format(i, 0))


def filters_mirror(count):
    array= [str(ip) for ip in ipaddress.IPv4Network("10.0.0.0/16")]

    for i in range(count):
        print("set packet-broker flow vasily{} match from-port p1-1".format(i))
        print("set packet-broker flow vasily{} match src-ip {}".format(i,array[i]))
        print("set packet-broker flow vasily{} match priority {}".format(i,i))
        print("set packet-broker flow vasily{} to-mirror-group vasily{}".format(i, 0)) #i


def add_ports_to_shared_group(count):
    for i in range(count):
        print("set packet-broker share-group vasily{} port p1-1".format(i))
        print("set packet-broker share-group vasily{} port p2-1".format(i))

def add_max_ports_to_link_group(count):
    for i in range(count):
        ii=i+1
        print("set packet-broker link-group vasily0  port p{}-1".format(ii))

def del_max_ports_to_link_group(count):
    for i in range(count):
        ii=i+1
        print("del packet-broker link-group vasily0  port p{}-1".format(ii))

def add_max_ports_to_share_group(count):
    for i in range(count):
        ii=i+1
        print("set packet-broker share-group vasily0  port p{}-1".format(ii))

def del_max_ports_to_share_group(count):
    for i in range(count):
        ii=i+1
        print("del packet-broker share-group vasily0  port p{}-1".format(ii))


if __name__ == '__main__':
    #set_filters_drop(513)
    del_filters(200)
    #link_group(16)
    #del_link_group(16)
    #share_group(200)
    #del_share_group(200)
    #filters_balance(513)
    #filters_mirror(513)
    #add_ports_to_share_group(200)

    #add_max_ports_to_link_group(32)
    #del_max_ports_to_link_group(32)

    #add_max_ports_to_share_group(32)
    #del_max_ports_to_share_group(32)

