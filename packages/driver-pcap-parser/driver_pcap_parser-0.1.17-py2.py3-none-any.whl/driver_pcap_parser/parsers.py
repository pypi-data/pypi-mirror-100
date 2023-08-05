import json
import logging
import re
import struct


def get_json_serial(packet):
    try:
        raw_json_data = struct.unpack_from(">256s", bytes(packet), offset=54)[0].decode('utf8')
        json_data = json.loads(raw_json_data)
        serial = json_data[0].get("terminalSerial")
        clientid = json_data[0].get("clientId")
    except Exception as e:
        logging.debug(e)
        return dict()
    return dict(serial=serial, clientid=clientid, terminal_type="JSON")


def get_m7_serial(packet):
    serial = None
    try:
        pkt_data = struct.unpack_from(">64s", bytes(packet), offset=54)[0].decode('utf8')
        pkt_match = re.match("(\d{15}),3(\d{9}),(\d{14}),.*", pkt_data)
    except Exception as e:
        logging.debug(e)
        return dict()
    if pkt_match:
        serial = str(pkt_match.group(1))
    return dict(terminal_serial=serial, terminal_type="M7")


def get_vt10_serial(packet):
    serial = None
    try:
        pkt_data = struct.unpack_from(">64s", bytes(packet), offset=54)[0].decode('utf8')
        pkt_match = re.match("(\d{15}),2(\d{9}),(\d{14}),.*", pkt_data)
    except Exception as e:
        logging.debug(e)
        return dict()
    if pkt_match:
        serial = str(pkt_match.group(1))
    return dict(terminal_serial=serial, terminal_type="VT10")


def get_ruptela_serial(packet):
    try:
        data = b''.join(struct.unpack_from('>8c', bytes(packet), offset=68))
        serial = str(int.from_bytes(data, byteorder='big'))
    except Exception as e:
        logging.debug(e)
        return dict()
    if len(serial) > 15:
        return dict()
    return dict(terminal_serial=serial, terminal_type="Ruptela")


def get_teltonika_serial(packet):
    try:
        serial_length = struct.unpack_from('>b', bytes(packet), offset=67)[0]
        if len(packet) > 100:
            return dict()
        if serial_length < 15:
            return dict()
        fmt = ">{}s".format(str(serial_length))
        serial = struct.unpack_from(fmt, bytes(packet), offset=68)[0].decode('utf8')
    except Exception as e:
        logging.debug(e)
        return dict()
    return dict(terminal_serial=serial, terminal_type="Teltonika")
