import re
######### utility function for hex literals ###########
def bin_buf(value_str):
    value_str = re.sub('\s+', '', value_str)
    value_str = re.sub('^(0x)+', '', value_str)
    value_str = value_str.lower()
    if not re.match('^[0-9a-f]+$', value_str):
        raise ValueError("Invalid hex string: {}".format(value_str))

    result = bytearray()
    if not len(value_str) % 2 == 0:
        value_str = "0".join(["", value_str])
    for i in range(0, len(value_str), 2):
        cur_byte = value_str[i] + value_str[i + 1]

        result.append(int(cur_byte, 16))


    return bytes(result)
#######################################################
