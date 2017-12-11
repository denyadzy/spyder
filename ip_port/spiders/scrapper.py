"""modul of spyders,creating lounchung"""
import scrapy
import re
from ..items import DataFields
from itertools import cycle


class PortSpider(scrapy.Spider):
    name = "port_spider"

    
    def start_requests(self):
        """goes thru URLs, calling parse fun"""
        
        urls = [
        "http://spys.one/proxies/",
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

            
    def parse(self, response):

        """Function for parsing. Filling database."""

	#get content of cell
        part = response.xpath("//table[2]//table//tr[@onmouseover]//td[@colspan ='1'][1] ").extract() 

        # found value of variables in skript tag
        dependences = response.xpath("//body/script/ text()").extract()[0]
	
        #using property that a^b^b=a we can just found variable, and save its nubmer befor xor
        if dependences[-1]==";":
            dependences = dependences[:-1]
        dependences = dependences.split(";")

        # found all xor statemnts
        keys = [x for x in dependences if "^"  in x]
        values = [x for x in dependences if "^"  not in x]
        
        dic_params = {} # dic of params 
        for i in values:
            # spliting string into encrypted var, number and decrypter var
            devided = i.split("=")
            dic_params[devided[0]] = int(devided[1])
            
        dic_numbers = {} # dic of encrypted numbers
        dic_vars ={}
        for i in keys:
            # spliting string into encrypted var, number and decrypter var
            devided = i.split("=")
            #while in encrypting uses only one operand ^ we can devideinto value and parametr: 
            try:
                encrypted = devided[0]
                num_cryp = devided[1].split("^")
            except:
                encrypted = devided[1]
                num_cryp = devided[0].split("^")
            
            try:
                
                num = int(num_cryp[0])
                
            except:
                
                try:
                     num = int(num_cryp[1])
                     
                except:
                    
                    try:# cathing, if XOR to two variables
                        dic_vars[encrypted] = dic_params[num_cryp[0]]^dic_params[num_cryp[1]]
                        
                    except:
                        print("encrypted not integer, can't be a port numer")
                    
                        
                    
                    
            dic_numbers[encrypted] = str(num)

        #fining port and ip adress
        for i in part:
            variables = re.findall("\+\((\w+)\^(\w+)\)", i) 
           
            port = ""
            for item in variables:
                if item[0] in dic_numbers:
                    port += dic_numbers[item[0]]
                    
                elif item[1] in dic_numbers:
                    port += dic_numbers[item[1]]
                    
                else:
                    try:
                        port += str(dic_vars[item[0]]^dic_params[item[1]])
                    except:
                        
                        try:
                            port += str(dic_vars[item[1]]^dic_params[item[0]])
                        
                        except:
                            print("some undefinite encryped item", item)
                
            ip_adress = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', i)[0]
            
            table_row = DataFields()
            table_row['ip_adress'] = ip_adress
            table_row['port'] = port
            yield table_row
            
          
