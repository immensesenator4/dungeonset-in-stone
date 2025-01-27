import socket
import json
import os
import ast
import types
class Host(object):
    def __init__(self,size:int,port:int):
            self.port=port
            self.hostname = socket.gethostname()
            self.ip_address = socket.gethostbyname(self.hostname)     
            self.data:dict[str,bytes]={}
            self.var=[]
            self.size=size
            self.adresses=[]
            self.record=[]
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
    def store_obj(self,obj:object,obj_name:str):
        original = obj
        z=self.simplify(obj.__dict__)
        
        y = json.dumps(z)
        self.data[obj_name] = y.encode()

        return original
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
    def recieve_obj(self,name:str,obj:list[object],initialization:dict[str,object]={})->object:
        new_data=self.data[name]
        data= new_data.decode()
        data=json.loads(data)
        f=self.unpack(data,classes=obj,initialization=initialization)
        return f
    def get_person(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.ip_address, self.port))
                s.listen()
                conn, addr = s.accept()

                if addr[0] not in self.adresses and len(self.adresses)+1<=self.size:
                     self.adresses.append(addr[0])
                     self.record.append(0)
                
                if addr[0] in self.adresses:
                    
                    for i in range(0,len(self.adresses)):
                        self.record[i]+=1
                        if addr[0]== self.adresses[i]:
                            self.record[i]=0
                        elif self.record[i]==10:
                            self.record.pop(i)
                            self.adresses.pop(i)
                            break
                    os.system('cls')
                    for adr in self.adresses:
                        print(f"{adr} is conected to network")
                    with conn:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            if ("recieve" in f"{data!r}" ):
                                if "file" in f"{data!r}":
                                        con=False
                                        file=""
                                        for char in f"data!r":
                                            
                                            if con:
                                                file+=char
                                            if char=="=":
                                                con=True
                                        f = open(file,'rb')
                                        s.connect((self.host, self.port))
                                        l = f.read(1024)
                                        while (l):
                                            s.send(l)
                                            l = f.read(1024)
                                        f.close()
                                else:
                                    var=""
                                    count=0
                                    for i in f"{data!r}":
                                        if count==0:
                                            pass
                                        elif i == "=":
                                            break
                                        else:
                                            var+=i
                                        count+=1
                                    
                                        
                                    if var in self.var:
                                        self.send(self.data[var],conn)
                                    else:
                                        self.send(b'N/a',conn)
                            elif "send file" in f"{data!r}":
                                    con=False
                                    file=""
                                    count=0
                                    for char in f"{data!r}":
                                        
                                        if con:
                                            file+=char
                                        if char==" ":
                                            count+=1
                                            if count ==2:
                                                con=True
                                    f = open(file,'wb')
                                    l = conn.recv(1024)
                                    while (l):
                                        f.write(l)
                                        l = conn.recv(1024)
                                    f.close()
                            elif "hi"in f"{data!r}":
                                self.send("available".encode(),conn)
                            else:
                                var=""
                                count=0
                                for i in f"{data!r}":
                                    if count==0:
                                        pass
                                    elif i == "=":
                                        break
                                    else:
                                        var+=i
                                    count+=1
                                self.var.append(var)
                                count = len(var)+1
                                new_data=""
                                for char in f"{data!r}":
                                    if count<0:
                                        new_data+=char
                                    count-=1
                                self.data[var]= new_data.encode()
                                self.send(b'recieved',conn)
                            return data,addr
                else:
                    self.send(b"server not found",conn)
    def comunicate(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.ip_address, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print(f"{data!r}")
                        l=input("respond")
                        self.send(l.encode(),conn)
                        os.system('cls')
    def send(self,data:bytes,conn):
        conn.sendall(data)

# h=Host(4,13455)

# while True:
#     h.get_person()