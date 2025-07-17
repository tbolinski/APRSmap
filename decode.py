import os
import aprs
import _thread
from aprs import APRSFrame, StatusReport, PositionReport
from queue import Queue
import datetime as dt
from ax253 import Address
import database

received = Queue()
moved = Queue()
located = {}

def path_tostr(path):
    nodes = ""
    for addr in path:
        nodes += str(addr)
        nodes += " -> "
    return nodes

def add_location(frame: APRSFrame):
    data = {}
    packet = frame.info.__class__.__name__
    data["source"] = str(frame.source)
    data["destination"] = str(frame.destination)
    data["type"] = str(packet)
    data["path"] = path_tostr(frame.path)
    data["timestamp"] = dt.datetime.now().isoformat()
    data["comment"] = str(frame.info.comment.decode("utf-8"))
    if str(packet) == "PositionReport":
        data["latitude"] = float(frame.info._position.lat)
        data["longitude"] = float(frame.info._position.long)
        data["altitude"] = str(frame.info._position.altitude_ft)
        if float(frame.info._position.lat) != 0 and float(frame.info._position.long) != 0:
            moved.put(data)
            located[str(frame.source)] = data
            database.store(data)
    else:
        data["data"] = str(frame.info.data.decode("utf-8"))
    received.put(data)

def initialize_kiss():
    ip = os.getenv("KISS_IP")
    port = os.getenv("KISS_PORT")
    kiss = aprs.TCPKISS(ip if ip else "127.0.0.1", port if port else 8001)
    kiss.start()

    while True:
        frames = kiss.read(min_frames=1)
        for frame in frames:
            _thread.start_new_thread(add_location, (frame,))