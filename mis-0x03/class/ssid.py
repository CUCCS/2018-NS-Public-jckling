from scapy.all import *
import chardet

# type: management frame-0
# subtype：Association request-0   Reassociation request-2   Probe Request-4    Probe Response-5 	Beacon Frame-8

def ssid_coding(name):
    encoding_type = str(chardet.detect(name)['encoding']) # 判断字符编码
    if str(encoding_type) != 'None':
        return encoding_type, str(name, encoding_type)
    else:
        if b'\xf0\x9f\x91\xbe\xf0\x9f\x91\xbe\xf0\x9f\x91\xbe' == name:
            return 'utf-8', str(name, 'utf-8')
        else:
            return 'GBK', str(name, 'gbk')

# Beacon、Probe Response
# 其他含有SSID的帧在捕获的包中没有
def find_ssid(path):
    packets = rdpcap(path)
    SSID_bytes, SSID = [], []
    mat = '{:15s}{:<9d}{:45s}'
    for pkt in packets:
        if pkt.haslayer(Dot11):
            if pkt.type == 0 and (pkt.subtype == 8 or pkt.subtype == 5):
                if pkt.info not in SSID_bytes:
                    encoding_type, name = ssid_coding(pkt.info)
                    print(mat.format(encoding_type, len(pkt.info), name))
                    SSID_bytes.append(pkt.info)
                    SSID.append(name)
    print('Toatal:', len(SSID))
    return SSID

# 无Beacon，有Probe Response
def hidden_ssid(path):
    packets = rdpcap(path)
    beacons, responses = [], []
    for pkt in packets:
        if pkt.haslayer(Dot11) and pkt.type == 0:
            if pkt.subtype == 8 and pkt.info not in beacons:
                beacons.append(pkt.info)
            elif pkt.subtype == 5 and pkt.info not in responses:
                responses.append(pkt.info)
    hidden_bytes, hidden = [], []
    for ssid in responses:
        if ssid not in beacons and ssid not in hidden_bytes:
            encoding_type, name = ssid_coding(ssid)
            print('%-15s%-9d%s'%(encoding_type, len(ssid), name))
            hidden_bytes.append(ssid)
            hidden.append(name)
    print('Toatal:', len(hidden))
    return hidden

if __name__ == '__main__':
    packets_faked1 = "faked_essids-01-filtered.cap"
    packets_faked3 = "faked_essids-03-filtered.cap"
    find_ssid(packets_faked1)
    print('-'*200)
    find_ssid(packets_faked3)
    print('-' * 200)

    packets_hidden1 = "hidden_finder-01-filtered.cap"
    packets_hidden2 = "hidden_finder-02-filtered.cap"
    hidden_ssid(packets_hidden1)
    print('-'*100)
    hidden_ssid(packets_hidden2)