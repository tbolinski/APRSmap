import os
import aprs
import _thread
from aprs import APRSFrame
from queue import Queue
import datetime as dt

received = Queue()
located = {}

def add_location(frame: APRSFrame):
    data = {}
    data["source"] = str(frame.source)
    data["destination"] = str(frame.destination)
    #data["path"] = str(frame.path)
    data["latitude"] = str(frame.info._position.lat)
    data["longitude"] = str(frame.info._position.long)
    data["altitude"] = str(frame.info._position.altitude_ft)
    data["timestamp"] = dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    located[str(frame.source)] = data

def initialize_kiss():
    ip = os.getenv("KISS_IP")
    port = os.getenv("KISS_PORT")
    kiss = aprs.TCPKISS(ip if ip else "127.0.0.1", port if port else 8001)
    kiss.start()

    while True:
        frames = kiss.read(min_frames=1)
        for frame in frames:
            if hasattr(frame.info, "_position"):
                if float(frame.info._position.lat) != 0 and float(frame.info._position.long) != 0: _thread.start_new_thread(add_location, (frame,))
            received.put(frame)