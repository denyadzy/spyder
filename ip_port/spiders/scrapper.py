"""modul of spyders,creating lounchung"""
import scrapy
import re
from ..items import DataFields
#from scrapy_splash import SplashRequest
#import json
class PortSpider(scrapy.Spider):
    name = "port_spider"

    
    def start_requests(self):
        """goes thru URLs, calling parse fun"""
        
        urls = [
        "http://spys.one/proxies/",
#        "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#            yield SplashRequest(url=url, callback=self.parse)

            
    def parse(self, response):
        """Function for parsing. Filling database.""" 
        # found value of variables in skript tag
        dependences = response.xpath("//body/script/ text()").extract()[0]
        part = response.xpath("//table[2]//table//tr[@onmouseover]//td[@colspan ='1'][1] ").extract()
        
        #using property that a^b^b=a we can just found 6-letter variable, and save its nubmerwithoyit  xor
        
        if dependences[-1]==";":
            dependences = dependences[:-1]
        dependences = dependences.split(";")
        # found all xor statemnts
        keys = [x for x in dependences if "^"  in x]
        
        dic_numbers = {} # dic of encrypted numbers
        for i in keys:
            # spliting string into encrypted, number and decrypter
            devided = i.split("=")
            #while in encrypting uses only one operand ^ we can hardcoding: 
            try:
                encrypted = devided[0]
                num_cryp = devided[1].split("^")
            except:
                encrypted = devided[1]
                num_cryp = devided[0].split("^")
            
            if len(num_cryp[0]) == 1:
                num = num_cryp[0]
            else:
                num = num_cryp[1]
            
            dic_numbers[encrypted] = num
    
        for i in part:
            variables = re.findall("\+\((\w+)\^(\w+)\)", i) 
           
            port = ""
            for item in variables:
                if item[0] in dic_numbers:
                    port += dic_numbers[item[0]]
                elif item[1] in dic_numbers:
                    port += dic_numbers[item[1]]
                else:
                    print("some undefinite encryped item", item)
                
            ip_adress = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', i)[0]
            
            table_row = DataFields()
            table_row['ip_adress'] = ip_adress
            table_row['port'] = port
            yield table_row
            
          
