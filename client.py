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

    def simplify_name_func(self,obj:str):
        shortened_name=''
        for i in obj:
            if i ==' ':
                break
            elif "<":
                pass
            else:
                shortened_name+=i
        return shortened_name
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

    def store_obj(self,obj:object,obj_name:str):
        copy_of=type('copy_of',obj.__class__.__bases__,dict(obj.__dict__))
        new=copy_of()
        z=self.simplify(new.__dict__)
        
        y = json.dumps(z)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(f"{obj_name}={y}".encode())
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
    def return_class(self,obj:object,ndict:dict,initialization:dict={},classes:list[object]=[]):
        def alter__init__(self,new_dict:dict,initialization:dict={},classes:list[object]=[],unpack = self.unpack):
                excludables=(int,str,float,dict,list,tuple,bool)
                for key, value in new_dict.items():
                
                    if isinstance(value,excludables):
                        if isinstance(value,list):
                            is_items = len(value)>0
                            if is_items:
                                print(value)
                                z= unpack(value,initialization,classes)
                            else:
                                z=key
                        elif isinstance(value,dict):
                            is_items = len(value)>0
                            if is_items:
                                z= unpack(value, initialization=initialization,classes=classes)
                            else:
                                z=value
                        else:
                            z= value
                    elif value in initialization.keys():
                        z=initialization[key]
                    else:
                        try:
                            z= json.loads(value)
                        except:
                            z= key
                    setattr(self, key, z) 
        funcType = types.MethodType
        obj.__init__=funcType(alter__init__,obj)
        x=obj.__init__(ndict,initialization,classes)
        return x
    def unpack(self,obj:dict|list,initialization:dict={},classes:list[object]=[]):
        excludables=(int,str,float,dict,list,bool)
        
        is_dict= isinstance(obj,dict)
        if is_dict:
            for key,var in obj.items():
                z=var
                if isinstance(var,excludables):
                    if isinstance(var,list):
                        is_items = len(var)>0
                        if is_items:
                            z= self.unpack(var,initialization,classes)
                        else:
                            z=var

                    elif isinstance(var,dict):
                        is_items = len(var)>0
                        if is_items:
                            is_class= 'object' in var.keys()
                            if is_class:
                                for clas in classes:
                                    if self.simplify_name_func(var) in str(clas):
                                        z=self.return_class(clas,obj,initialization,classes)
                            else:
                                
                                self.unpack(var,initialization,classes)
                        else:
                            
                            z=var

                    else:
                        if var in initialization.keys():
                                    z=initialization[key]
                        else:
                            z= var
                
                else:
                    try:
                        z= json.loads(var)
                    except:
                        z= key
                obj[key]=z
            
            return obj
            
        elif isinstance(obj,list):
            for i in range(0,len(obj)):
                var=obj[i]
                z=var
                if isinstance(var,excludables):
                    if isinstance(var,list):
                        is_items = len(var)>0
                        
                        if is_items:
                            z= self.unpack(var,initialization,classes)
                        else:
                            z= var
                    elif isinstance(var,dict):
                        is_items = len(var)>0
                        if is_items:
                            z= self.unpack(var)
                        else:
                            z= var
                    else:
                        if var in initialization.keys():
                            z=initialization[key]
                        else:
                            z= var
                        
                elif var in initialization.keys():
                    z=initialization[var]
                else:
                    try:
                        z= var
                    except:
                        z= obj[i]
                obj[i]=z
            
        
        return obj
    def recvall2(self,sock:socket)->bytes:
        return sock.recv(2**255, socket.MSG_WAITALL)
    def recieve_obj(self,name:str,obj:list[object],initialization:dict[str,object]={})->object:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            s.connect((self.host, self.port)) 
            s.sendall(f"{name}=recieve".encode())
            class_param=self.recvall2(s).decode()
            class_param=ast.literal_eval(class_param[0:-1])
            class_param= self.unpack(class_param,initialization,obj)
        return class_param
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
    def simplify(self,obj:dict|list, is_dict:bool=True)->dict|list:
        excludables=(int,str,float,dict,list,tuple,bool,bytes)
        if is_dict:
            ran=False
            for key,var in obj.items():
                ran=True
                if isinstance(var,excludables):
                    if isinstance(var,list):
                        is_items = len(var)>0
                        if is_items:
                            z= self.simplify(var,False)
                        else:
                            z= var

                    elif isinstance(var,dict):
                        is_items = len(var)>0
                        z= self.simplify(var)
                    else:
                        z= var
                else:
                    try:
                        obj_dict=var.__dict__
                        obj_dict['object']=self.simplify_name_func(str(obj))
                        z= self.simplify(obj_dict)
                    except:
                        z= key
                obj[key]=z
            
            return obj
            
        elif isinstance(obj,list):
            for i in range(0,len(obj)):
                var=obj[i]
                if isinstance(var,excludables):
                    if isinstance(var,list):
                        is_items = len(var)>0
                        
                        if is_items:
                            z= self.simplify(var,False)
                        else:
                            z= var
                    elif isinstance(var,dict):
                        is_items = len(var)>0
                    
                        if is_items:
                            z= self.simplify(var,False)
                        else:
                            z= var
                    else:
                        z= var
                else:
                    try:
                        obj_dict=var.__dict__
                        obj_dict['object']= self.simplify_name_func(str(var))
                        z= self.simplify(obj_dict)
                    except:
                        z= obj[i]
                obj[i]=z
            
        
        return obj
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