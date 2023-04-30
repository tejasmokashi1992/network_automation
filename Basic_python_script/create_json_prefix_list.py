def create_json_preifx_list():
    final = []
    for IP in a:
        subnet = IP[-2:]
        prefix_list_json = {
        "IpAddress": IP,
        "PrefixList":"IPV4_PREFIXES_TRANSITEDGE",
        "Comment":'ge {}'.format(subnet),
        "IpAddressWithRule":'{0} ge {1}'.format(IP,subnet)
        }
        final.append(prefix_list_json)
    print(final)
