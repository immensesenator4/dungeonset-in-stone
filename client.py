import socket, select
import json
import os
import ast
import types
#what is below is a send and recieve function
HOST =  "192.168.12.195" 
PORT = 13455 
class client(object):
    def __init__(self,port=0):
        self.host,self.port= self.find_servers(set_port=port)

    def send_str(self,var:str,contents):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(f"{var}={contents}".encode())
            return s.recv(1024)
    def send_file(self,File:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                f = open(f'{File}','wb')
                s.connect((self.host, self.port))
                l = f.read(1024)
                s.send(f"send file {File}".encode())
                while (l):
                    s.send(l)
                    l = f.read(1024)
                f.close()
                
    def send_int(self,var:str,contents:int):
        y = json.dumps(contents)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(f"{var}={y}".encode())
            return s.recv(1024)
    def send_bool(self,var:str,contents:bool):
        y = json.dumps(contents)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(f"{var}={y}".encode())
            return s.recv(1024)
    def send_dict(self,var:str,contents:dict):
        y = json.dumps(contents)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(f"{var}={y}".encode())
            return s.recv(1024)
    def send_list(self,var:str,contents:list):
        y = json.dumps(contents)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(f"{var}={y}".encode())
            return s.recv(1024)
    def send_obj(self,var:str,contents:object):
        y = json.dumps(contents.__dict__)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(f"{var}={y}".encode())
            return s.recv(1024)
    def recieve_str(self,var:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            s.connect((self.host, self.port)) 
            s.sendall(f"{var}=recieve".encode())
            return s.recv(1024)
    def recieve_file(self,File:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
            s.send(f"Recieve File={File}")    
            f = open(File,'wb')
            l = s.recv(1024)
            while (l):
                f.write(l)
                l = s.recv(1024)
            f.close()
    def recieve_int(self,var:str):    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            s.connect((self.host, self.port)) 
            s.sendall(f"{var}=recieve".encode())
            return int(s.recv(1024).decode()[0:-1])
    def recieve_bool(self,var:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            s.connect((self.host, self.port)) 
            s.sendall(f"{var}=recieve".encode())
            new_bool=s.recv(1024).decode()
            return ("true"in new_bool.lower())
    def recieve_dict(self,var:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            s.connect((self.host, self.port)) 
            s.sendall(f"{var}=recieve".encode())
            new_dict=s.recv(1024).decode()
            new_dict=ast.literal_eval(new_dict[0:-1])
            
            return new_dict
    def recieve_list(self,var:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            s.connect((self.host, self.port)) 
            s.sendall(f"{var}=recieve".encode())
            return json.loads(s.recv(1024).decode()[0:-1])
    def unsimplify(self,obj, is_dict:bool=True,replace:dict={}):
        def alter__init__(self,new_dict:dict):
            for key, value in new_dict.items():
                setattr(self, key, value) 
        funcType = types.MethodType

        excludables=(int,str,float,dict,list)
        z= json.loads(obj)
        is_dict=isinstance(z,dict)
        if is_dict:
            for key,var in z.items():
                new_var=json.loads(var)

                if isinstance(new_var,excludables):
                    if isinstance(var,list):
                        is_items = len(var)>0
                        
                        if is_items:
                            new_var= self.simplify(var,False)
                        else:
                            return new_var
                    elif isinstance(var,dict):
                        is_items = len(var)>0
                    
                        if is_items:
                            z= self.simplify(var,False)
                        else:
                            return new_var

        
        return z
    def receive_obj(self,var:str,new_var:object,replace:dict={}):
        def alter__init__(self,new_dict:dict):
             for key, value in new_dict.items():
                setattr(self, key, value) 
        funcType = types.MethodType
        new_var.__init__=funcType(alter__init__,new_var)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            s.connect((self.host, self.port)) 
            s.sendall(f"{var}=recieve".encode())
            class_param=s.recv(1024).decode()
            class_param=ast.literal_eval(class_param[0:-1])
            class_param= self.simplify(class_param)
            new_var.__init__(class_param)
            return new_var
    def comunicate(self,content:str):
         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            s.connect((self.host, self.port)) 
            s.sendall(content.encode())
            return s.recv(1024)
    def scan_port(self,ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.00000000001)  # Timeout after 1 second
                s.connect((ip, port))
                s.send("hi".encode())
                return ("server not found" not in s.recv(1024).decode())
        except (socket.timeout, ConnectionRefusedError):
            return False
    def find_servers(self,start=1,end=99999,set_port=0):
        net_ip= self.simplify_ip(socket.gethostbyname(socket.gethostname()))
        if set_port>0:
            for i in range(1, 255):
                ip = f"{net_ip}.{i}"
                if self.scan_port(ip, set_port):
                    print(f"Server found at {ip}:{set_port}")
                    return ip,set_port
            net_ip=self.simplify_ip(net_ip)
            for x in range(1,255):
                for i in range(1, 255):
                    ip = f"{net_ip}.{x}.{i}"
                    if self.scan_port(ip, set_port):
                        print(f"Server found at {ip}:{set_port}")
                        return ip,set_port
        else:
            for port in range(start,end):
                for i in range(1, 255):
                    ip = f"{net_ip}.{i}"
                    if self.scan_port(ip, port):
                        print(f"Server found at {ip}:{port}")
                        return ip,port
        return "m","n"
    def simplify_ip(self,ip:str):
        new_ip=""
        net_ip=""
        count=0
        for char in ip:
            if char==".":
                count+=1
                net_ip=new_ip
            
            new_ip+=char
        return net_ip

# d=client(port=13455)
# while True:
#     while d.scan_port(d.host,d.port):
#         os.system("cls")
#         if input("what do you want to do : \\send\ or /recieve/ : ")=="send":
#             var=input("whats the name of the var : ")
#             contents = input("what is the message : ")
#             d.send_str(var,contents)
#         else:
#             var=input("whats the name of the var : ")
#             print(d.recieve_str(var))  
#         input("press \\any\ button to /continue/\n")
#     d.host = d.find_servers(set_port=d.port)[0]