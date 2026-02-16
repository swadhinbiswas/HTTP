import socket
import struct
import sys
from datetime import datetime
from server import DNSfunctions



class DNSQuestion:
    def __init__(self,qname,qtype,qclass):
        self.qname=qname
        self.qtype=qtype
        self.qclass=qclass
    @classmethod
    def parse(cls,data,offset):
        qname,offset=DNSfunctions.parse_domain_name(data,offset)
        if offset+4>len(data):
            raise ValueError("Invalid questions:not enough data")

        qtype,qclass=struct.unpack('>HH',data[offset:offset+4])
        offset+=4
        return cls(qname,qtype,qclass),offset
    def pack(self):
        packed_name=DNSfunctions.encode_domain_name(self.qname)
        packed_type_class=struct.pack('>HH',self.qtype,self.qclass)
        return packed_name+packed_type_class

    def __str__(self):
        return f"questions({self.qname},type={self.qtype},class={self.qclass})"


