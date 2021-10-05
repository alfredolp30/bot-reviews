import logging
from model.review_appstore import ReviewAppstore
import sqlite3
from sqlite3.dbapi2 import Error


class DBManager: 

    DATABASE_FILE = "reviews.db"

    def __init__(self) -> None:
        self.con = sqlite3.connect(self.DATABASE_FILE)

    def createTable(self, createTable: str): 
        try: 
            self.con.cursor().execute(createTable)
            self.con.commit()
        except Exception as e: 
            logging.error("error create database {}".format(e))

    def insert(self, table: str, json: dict) -> None:
        try: 
            cols = ', '.join('"{}"'.format(col) for col in json.keys())
            vals = ', '.join(':{}'.format(col) for col in json.keys())
            sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
            self.con.cursor().execute(sql, json)
            self.con.commit()
        except Exception as e:
            logging.error('error insert database {}'.format(e))

    def contains(self, table: str, key: str, value: any) -> bool:
        contains = False
        try: 
            sql = 'SELECT 1 FROM {} WHERE {}={}'.format(table, key, value)
            value = self.con.cursor().execute(sql).fetchone()
            if value != None:
                contains = value[0] >= 1
        except Exception as e:
            logging.error('error contains database {}'.format(e))
        
        return contains
    

    def get(self, table: str, comparator: str, orderBy: str) -> list[any]: 
        try: 
            sql = 'SELECT * FROM {} WHERE {} ORDER BY {} DESC'.format(table, comparator, orderBy)
            print(sql)
            value = self.con.cursor().execute(sql).fetchall()
            return value
        except Exception as e:
            logging.error('error get database {}'.format(e))
        
        return []
        



