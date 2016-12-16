import sys
import pymysql
class Connection:
    def __init__(self, user, password, db, host='localhost'):
        self.user = user
        self.password=password
        self.host=host
        self.db=db
        self._connection= None
         
    @property
    def connection(self):
        return self._connection

    def __enter__ (self):
        self.connect()

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.disconnect()
             
    def connect(self):
        if not self._connection:
            self._connection=pymysql.connect(
                                             host=self.host,
                                             user=self.user,
                                             passwd=self.password,
                                             db=self.db
                                             )
                 
    def disconnect (self):
        if self._connection:
            self._connection.close()  
                 
class Jockey:
     def __init__(self, db_connection, jockey_id, name, contacts, ratio):
         self.db_connection=db_connection.connection
         self.jockey_id=jockey_id
         self.name=name
         self.contacts=contacts
         self.ratio=ratio
          
     def save(self):
         c=self.db_connection.cursor()
         c.execute('INSERT INTO jockeys (jockey_id, name, contacts, ratio) VALUES (%s,%s,%s,%s);',
                   (self.jockey_id, self.name, self.contacts, self.ratio)
                   ) 
         self.db_connection.commit()
         c.close()  
          
con= Connection ('root','1234','my_db')  
with con:
    jockey=Jockey(con, 2, 'verv', '1244@mail', '5657')
    jockey.save()    
    
    
    
# db=pymysql.connect(
#                    host='localhost',
#                    user='root',
#                    passwd='1234',
#                    db='my_db'
#                    )
# c=db.cursor()
# # c.execute(
# #            'insert into horses (horse_id, name, ratio, age) values(%s,%s,%s,%s);', (2,'holly', 58,4)
# #            )
# # db.commit()
# c.execute(
#           'select * from horses;'
#           )        
# res_horses=c.fetchall()
# for h in res_horses:
#     print(h)
#    
# c.close()
# db.close()     
