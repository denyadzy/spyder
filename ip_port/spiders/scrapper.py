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
        values = [x for x in dependences if x  not in keys]
        
        dic_params = {} # dic of params 
        for i in values:
            # spliting string into encrypted var and number 
            splited = i.split("=")
            dic_params[splited[0]] = int(splited[1])
            
        dic_numbers = {}    # dict of XOR number and var
        dic_vars ={}        # dict of XOR of two vars
        
        for i in keys:
            # spliting string into encrypted var, number and decrypter var
            splited = i.split("=")
            #while in encrypting uses only one operand ^ we can devideinto value and parametr: 
            try:
                encrypted = splited[0]
                num_cryp = splited[1].split("^")
            except:
                encrypted = splited[1]
                num_cryp = splited[0].split("^")
            
            try:
                
                num = int(num_cryp[0])
                
            except:
                
                try:
                     num = int(num_cryp[1])
                     
                except:
                    
                    try:# cathing, if XOR to two variables from list
                        dic_vars[encrypted] = dic_params[num_cryp[0]]^dic_params[num_cryp[1]]
                        
                    except:
                        print("encrypted not integer, can't be a port numer")
                    
                        
                    
                    
            dic_numbers[encrypted] = str(num)

        #fining port and ip adress
        for i in part:
            variables = re.findall("\+\((\w+)\^(\w+)\)", i) 
           
            port = ""
            for item in variables:
                # findind value of XOR of value and variable
                if item[0] in dic_numbers:
                    port += dic_numbers[item[0]]
                    
                elif item[1] in dic_numbers:
                    port += dic_numbers[item[1]]
                    
                else:
                    # catching  variable what equals to XOR of two variables
                    try:
                        port += str(dic_vars[item[0]]^dic_params[item[1]])
                    except:
                        
                        try:
                            port += str(dic_vars[item[1]]^dic_params[item[0]])
                        # can't find any match
                        except:
                            print("some undefinite encryped item", item)
                
            ip_adress = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', i)[0]
            
            table_row = DataFields()
            table_row['ip_adress'] = ip_adress
            table_row['port'] = port
            yield table_row
            
          
