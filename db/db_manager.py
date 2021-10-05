import logging
import sqlite3


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
    

    def get(self, table: str, where: str = None, orderBy: str = None, limit: int = None) -> list[any]: 
        try: 
            sql = 'SELECT * FROM {}'.format(table, where, orderBy)

            if where:
                sql += ' WHERE {}'.format(where)
            if orderBy:
                sql += ' ORDER BY {} DESC'.format(orderBy)
            if limit: 
                sql += ' LIMIT {}'.format(limit)

            value = self.con.cursor().execute(sql).fetchall()
            return value
        except Exception as e:
            logging.error('error get database {}'.format(e))
        
        return []
    


