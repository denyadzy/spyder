# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from items import DataFields

"""creating database for datafrom site"""

Base = declarative_base()

class DataTable(Base):
    """initing database"""
    
    __tablename__ = 'parsed_data'
    id = Column(Integer, primary_key=True)
    ip_adress = Column(String)
    port = Column(Integer)

    def __init__(self, ip_adress,port):
        self.ip_adress = ip_adress
        self.port = port
       
    def __repr__(self):
        return "<Data ip: %s, port: %s>" % (self.ip_adress, self.port)


class ParsedPipeline(object):
    """Filling database"""  
    
    def __init__(self):
        basename = 'ip_port'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)
            
    def open_spider(self, spider):
        self.session = Session(bind=self.engine)
    
    def process_item(self, column, spider):
        if isinstance(column, DataFields):             
            dt = DataTable(column['ip_adress'],column['port'])
            self.session.add(dt)
            
        return column
          
    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    
