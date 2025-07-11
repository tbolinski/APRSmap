import os
import aprs
import _thread
from aprs import APRSFrame, StatusReport, PositionReport
from queue import Queue
import datetime as dt
import database

received = Queue()
moved = Queue()
located = {}

def add_location(frame: APRSFrame):
    data = {}
    packet = frame.info.__class__.__name__
    data["source"] = str(frame.source)
    data["destination"] = str(frame.destination)
    data["type"] = str(packet)
    #data["path"] = str(frame.path)
    data["timestamp"] = dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    if packet == "PositionReport":
        data["latitude"] = str(frame.info._position.lat)
        data["longitude"] = str(frame.info._position.long)
        data["altitude"] = str(frame.info._position.altitude_ft)
        moved.put(data)
        located[str(frame.source)] = data
        database.store(data)
    else:
        data["data"] = str(frame.info.data.decode("utf-8"))
    data["comment"] = str(frame.info.comment.decode("utf-8"))
    received.put(data)

def initialize_kiss():
    ip = os.getenv("KISS_IP")
    port = os.getenv("KISS_PORT")
    kiss = aprs.TCPKISS(ip if ip else "127.0.0.1", port if port else 8001)
    kiss.start()

    while True:
        frames = kiss.read(min_frames=1)
        for frame in frames:
            add_location(frame)