from server import (
  Config,
  DNSQuestion,
  DNSfunctions,
  DNSResourceRecord,
  DNSHeader
)
import socket
from datetime import datetime
class DNSServer:
  def __init__(self,port=Config.DNS_PORT):
    self.port=port
    self.sock=None
    self.records={
    # Documentation & Testing
    'example.com': '93.184.216.34',      # IANA reserved domain for examples
    'test.local': '127.0.0.1',           # Localhost (Loopback)
    'router.local': '192.168.1.1',       # Common default gateway

    # Tech Giants (Note: These have many IPs, these are just one valid option each)
    'google.com': '142.250.190.46',      # Google Search
    'youtube.com': '142.250.190.78',     # YouTube
    'facebook.com': '157.240.22.35',     # Facebook
    'amazon.com': '205.251.242.103',     # Amazon
    'microsoft.com': '20.112.52.29',     # Microsoft
    'apple.com': '17.253.144.10',        # Apple

    # Dev Tools & Info
    'github.com': '140.82.112.3',        # GitHub
    'stackoverflow.com': '151.101.1.69', # Stack Overflow
    'wikipedia.org': '185.15.58.224',    # Wikipedia
    'cloudflare.com': '104.16.132.229',  # Cloudflare
    'python.org': '45.55.99.72',         # Python Software Foundation

    # Public DNS Resolvers (Often used to test connectivity)
    'dns.google': '8.8.8.8',             # Google Public DNS
    'one.one.one.one': '1.1.1.1',        # Cloudflare Public DNS
}
  def start(self):
    self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind(('0.0.0.0',self.port))
    print(f"[*] DNS Server started on port {self.port}")
    print(f"[*] Serving {len(self.records)} records")
    print("[*] Press Ctrl+C to stop\n")
    try:
      while True:
          self.handel_request()
    except KeyboardInterrupt:
            print("\n[*] Shutting down...")
    finally:
      self.sock.close()
  def handel_request(self):
    try:
      data,addr=self.sock.recvfrom(Config.MAX_PACKET_SIZE)
      timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      print(f"[{timestamp}] Query from {addr[0]}:{addr[1]}")
      response=self.process_query(data)
      self.sock.sendto(response,addr)
    except Exception as e:
       print(f"[!] Error handling request: {e}")
  def process_query(self,data):
    try:
      header=DNSHeader.parse(data)
      print(f"{header}")
      if header.get_qr()!=QR_QUERY:
        print(" [!] Not A query")
