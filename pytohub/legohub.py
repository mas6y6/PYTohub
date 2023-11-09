from serial import Serial
import serial.tools.list_ports as listports
import time
import tkinter.messagebox as mbox
import tkinter.filedialog as file
import json

class packet_type:
    command = 1
    data_packet = 2
    ping = 3
    error = 4
    returned = 5

class status:
    success = 0
    failure = 1
    connection_error = 3
    usb_error = 2
    unknown = -1

class hubconnection:
    def __init__(self, port: str):
        self.hub = Serial(port,9600,timeout=10)
    
    def send_raw_data(self, data: dict):
        dic = json.dumps(data)
        self.hub.write(bytes(f"�{dic}�\n\r",encoding="utf-8"))
        
    def get_raw_data(self):
        try:
            return self.hub.readline().decode("utf-8").split("�")[1]
        except:
            return None
    
    def send_packet(self,packet):
        packet = {"packet-type":packet_type.data_packet,"packet":packet}
        self.send_raw_data(packet)
        return self.get_raw_data()
    
    def send_ping(self,returndata):
        packet = {"packet-type":packet_type.ping,"return":returndata}
        self.send_raw_data(packet)
        return self.get_raw_data()
    
    def send_command(self,cmd: str,data: list):
        packet = {"packet-type":packet_type.command,"command":cmd,"data":data}
        self.send_raw_data(packet)
        return self.get_raw_data()
    
    def close(self):
        self.hub.close()

def listallports():
    r = listports.comports(include_links=True)
    li = []
    for i in r:
        if i.description == "LEGO Technic Large Hub in FS Mode":
            li.append(i.device)
    return li