from config import Config
import socket
import struct
import sys
from datetime import datetime


class DNSHeader:
    """
        DNS Header Structure (12 bytes)

        Fields:
            id: 16-bit transaction ID
            flags: 16-bit flags field containing:
                - QR: Query (0) or Response (1)
                - OPCODE: Operation code
                - AA: Authoritative Answer
                - TC: Truncation
                - RD: Recursion Desired
                - RA: Recursion Available
                - Z: Reserved (must be 0)
                - RCODE: Response code
            qdcount: Number of questions
            ancount: Number of answers
            nscount: Number of authority records
            arcount: Number of additional records
        """

    def __init__(self,id,flags,qdcount,account,nscount,arcount):
        self.id=id
        self.flag=flags
        self.qdcount=qdcount
        self.account=account
        self.nscount=nscount
        self.arcount=arcount
    @classmethod
    def parse(cls,data):
        if len(data)<12:
            raise ValueError ("DNS header must be least 12 bytes")
        
    # Unpack the hdeader using big-endian format 
    #Format 6 unsigned shorts (>HHHHHH)
        id,flags,qdcount,account,nscount,arcount=struct.unpack('>HHHHHH',data[:12])
        return cls(id,flags,qdcount,nscount,arcount)

    def pack(self):
        return struct.pack('>HHHHHH',self.id,
        self.flags,self.qdcount,self.ancount,self.nscount,self.arcount)
    
    def get_qr(self):
        return (self.flags >>15)& 0x1
    
    def get_opcode(self):
        return (self.flags >> 11)& 0xF
    def get_rd(self):
        return (self.flags >> 8)&0x1
    def get_rcode(self):
        return self.flags & 0xF
    
    def set_flags(self,qr=0,opcode=0,aa=0,tc=0,ra=0,rcode=0):
        self.flags=(
            qr <<15|opcode<<11|aa<<10|tc<<9|ra<<7|rd<<8|rcode & 0xF
        )
    def __str__(self):
        return (f"DNSHeader(id={self.id}, qr={self.get_qr()}, "
                f"opcode={self.get_opcode()}, rd={self.get_rd()}, "
                f"rcode={self.get_rcode()}, qd={self.qdcount}, "
                f"an={self.ancount}, ns={self.nscount}, ar={self.arcount})")


