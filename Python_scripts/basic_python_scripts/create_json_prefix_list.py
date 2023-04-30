ip_list = ['1.1.1.0/12', '2.2.2.0/16', '3.3.3.0/24']
def create_json_prefix_list():
    final = []
    for IP in ip_list:
        subnet = IP[-2:]
        prefix_list_json = {
        "IpAddress": IP,
        "PrefixList":"IPV4_PREFIXES,
        "Comment":'ge {}'.format(subnet),
        "IpAddressWithRule":'{0} ge {1}'.format(IP,subnet)
        }
        final.append(prefix_list_json)
    print(final)
