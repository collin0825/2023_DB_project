from typing import Optional
from link import *
import datetime

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class Member():
    def get_member(mid):
        sql = "SELECT MID, NAME, PASSWORD, IDENTITY, NAME FROM MEMBER WHERE MID = :mid"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mid' : mid}))
    
    def get_profile(mid):
        sql = "SELECT * FROM MEMBER WHERE MID = :mid"
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'mid' : mid}))
    
    def get_all_account():
        sql = "SELECT MID FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def update_profile(input):
        sql = "UPDATE MEMBER SET PID=:pid, BIRTH=:birth, PHONE=:phone, GENDER=:gender, DEPT=:dept, GRADE=:grade, EMAIL=:email WHERE MID=:mid"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def create_member(input):
        sql = 'INSERT INTO MEMBER VALUES (:mid, :name, :password, :identity, null, null, null, null, null, null, null)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(mid, vid):
        sql = 'DELETE FROM SAVERECORD WHERE VID=:vid AND MID=:mid'
        DB.execute_input(DB.prepare(sql), {'mid': mid, 'vid':vid})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM APPLICATION NATURAL JOIN APPLYRECORD WHERE MID = :id ORDER BY AID'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))
    
    def get_role(userid):
        sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM SAVERECORD WHERE SAVERECORD.MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM SAVERECORD WHERE MID = :id'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_saveInterest(user_id, time):
        sql = 'INSERT INTO INTEREST VALUES (:id, :time)' #, cart_tno_seq.nextval
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def add_saveRecord(user_id, time, vid):
        sql = 'INSERT INTO SAVERECORD VALUES (:id, :time, :vid)' #, cart_tno_seq.nextval
        # DB.setinputsizes(time=oracledb.TIMESTAMP)
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time, 'vid': vid})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()
       
class Vacancy():
    def count():
        sql = 'SELECT COUNT(*) FROM VACANCY'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_vacancy(vid):
        sql ='SELECT * FROM VACANCY NATURAL JOIN DEPARTMENT WHERE VID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': vid}))

    def get_all_vacancy():
        sql = 'SELECT * FROM VACANCY NATURAL JOIN DEPARTMENT'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_open_vacancy():
        sql = 'SELECT * FROM VACANCY NATURAL JOIN DEPARTMENT WHERE STATUS = 1'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_name(pid):
        sql = 'SELECT PNAME FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]

    def add_vacancy(input):
        sql = 'INSERT INTO VACANCY VALUES (:vid, :workTime, :vName, :content, :salary, :skill, :required, :status, :did)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(pid):
        sql = 'DELETE FROM PRODUCT WHERE PID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def update_vacancy(input):
        input['required'] = int(input['required'])
        sql = 'UPDATE VACANCY SET WORKTIME=:workTime, VNAME=:vName, CONTENT=:content, SALARY=:salary, REQUIRED=:required, SKILL=:skill WHERE VID=:vid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_status(vid, status):
        if status == 'open':
            sql = 'UPDATE VACANCY SET STATUS=1 WHERE VID=:vid'
        else:
            sql = 'UPDATE VACANCY SET STATUS=0 WHERE VID=:vid'
        DB.execute_input(DB.prepare(sql), {'vid': vid})
        DB.commit()
    def get_dept(office, unit):
        sql = 'SELECT DID FROM DEPARTMENT WHERE OFFICE = :office AND DIVISION = :unit'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'office': office, 'unit': unit}))
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_product(pid):
        sql = 'SELECT * FROM SAVERECORD WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))
    
    def check_saveRecord(pid, mid):
        sql = 'SELECT * FROM SAVERECORD WHERE VID = :id AND MID = :mid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid, 'mid': mid}))

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pid':pid}) )[0]
    
    def update_vacancy(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    
class Apply_List():
    def get_application():
        sql = 'SELECT A.MID, M.NAME, V.VID, V.VNAME, A.AID, R.STATUS FROM APPLICATION A, APPLYRECORD R, MEMBER M, VACANCY V WHERE R.AID = A.AID AND A.MID = M.MID AND R.VID = V.VID GROUP BY V.VID, V.VNAME, A.MID, M.NAME , A.AID, R.STATUS ORDER BY V.VNAME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_applydetail():
        sql = 'SELECT A.MID, M.DEPT, M.GRADE, M.NAME, V.VID, V.VNAME, A.AVAILABLETIME, A.BONUS, R.TIME, A.AID FROM APPLICATION A, APPLYRECORD R, MEMBER M, VACANCY V WHERE R.AID = A.AID AND A.MID = M.MID AND R.VID = V.VID'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def update_status(aid, status):
        if status == 'meet':
            sql = 'UPDATE APPLYRECORD SET STATUS=1 WHERE AID=:aid'
        else:
            sql = 'UPDATE APPLYRECORD SET STATUS=2 WHERE AID=:aid'
        DB.execute_input(DB.prepare(sql), {'aid': aid})
        DB.commit()

    def get_aid():
        sql = 'SELECT * FROM APPLICATION'
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def insert_application(input):
        sql = 'INSERT INTO APPLICATION VALUES (:aid, :avaTime, :bonus, :mid)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def insert_applyrecord(input):
        sql = 'INSERT INTO APPLYRECORD VALUES (:aid, :vid, :time, :status)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()


class Order_List():
    def add_order(input):
        sql = 'INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_order():
        sql = 'SELECT OID, NAME, PRICE, ORDERTIME FROM ORDER_LIST NATURAL JOIN MEMBER ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.PID = P.PID'
        return DB.fetchall(DB.execute(DB.connect(), sql))


class Analysis():
    def month_apply(i):
        sql = 'SELECT EXTRACT(MONTH FROM TIME), COUNT(*) FROM APPLYRECORD WHERE EXTRACT(MONTH FROM TIME)=:mon GROUP BY EXTRACT(MONTH FROM TIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i}))
    
    def category_vacancy():
        sql = 'SELECT COUNT(*), OFFICE FROM VACANCY NATURAL JOIN DEPARTMENT WHERE STATUS=1 GROUP BY OFFICE'
        return DB.fetchall( DB.execute( DB.connect(), sql))
    
    def category_vacancy_all():
        sql = 'SELECT COUNT(*), OFFICE FROM VACANCY NATURAL JOIN DEPARTMENT GROUP BY OFFICE'
        return DB.fetchall( DB.execute( DB.connect(), sql))