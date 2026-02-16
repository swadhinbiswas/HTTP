from server import DNSfunctions
from server import DNSQuestion
from server import Config
import socket
class DNSResourceRecord:
  def __init__(self,
  name:str,rtype,rclass,ttl,rdata
                ):
      self.name=name
      self.rtype=rtype
      self.rclass=rclass
      self.ttl=ttl
      self.rdata=rdate
  def pack(self):
    packed_name=DNSfunctions.encode_domain_name(self.name)
    packed_fields=struct.pack('>HHIH',self.rtype,self.rclass,self.ttl,len(self.rdata))
    return packed_name+packed_fields+self.rdata
  def __str__(self):
    if self.rtype==Config.TYPE_A and len(self.rdata)==4:
      ip=socket.inet_ntoa(self.rdata)
      return f"RR({self.name}->{ip},TTL={self.ttl})"
    return f"RR({self.name},type={self.rtype},TTL={self.ttl})"
    
