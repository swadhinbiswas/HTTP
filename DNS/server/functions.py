

class DNSfunctions:
    @classmethod
    def parse_domain_name(cls,data,offset):
        labels=[]
        while True:
            if offset>=len(data):
                raise ValueError("Invalid domain name :Unexpected end of the data ")
            length=data[offset]
            offset+=1
            if length==0:
                break
            if length & 0xC0==0xC0:
                if offset>=len(data):
                    raise ValueError ("Invalid Compression pointer ")
                
                pointer_offset=((length & 0x3F)<< 8) |data[offset]
                offset+=1
                pointed_name,_=cls.parse_domain_name(data,pointer_offset)
                if pointed_name and pointed_name != ".":
                    labels.append(pointed_name)
                return '.'.join(labels), offset 

            if  offset+length>len(data):
                raise ValueError("Invalid Domain name : label Extends beyond data")
            label=data[offset:offset+length].decode('ascii')
            labels.append(label)
            offset+=length 
        return '.'.join(labels) if labels else '.', offset 
    
    @classmethod
    def encode_domain_name(cls,domain):
        if domain ==".":
            return b'\x00'
        encoded =b''
        for label in domain.split('.'):
            if label:
                length=len(label)
                if length>63:
                    raise ValueError(f"Label too Long:{label}")
                encoded+=bytes([length])+label.encode('ascii')
        encoded+=b'\x00'
        return encoded 




