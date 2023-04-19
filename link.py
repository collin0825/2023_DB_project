# import cx_Oracle
# # cx_Oracle.init_oracle_client(lib_dir="./instantclient_19_8") # init Oracle instant client 位置
# connection = cx_Oracle.connect('GROUP1', '2IGVB44zhK', cx_Oracle.makedsn('140.117.69.70', 1521, service_name='ORCLPDB1'))
# cursor = connection.cursor()

import oracledb 
# cx_Oracle.init_oracle_client() # init Oracle instant client 位置 
# # connection = cx_Oracle.connect('GROUP1', '2IGVB44zhK', cx_Oracle.makedsn('140.117.69.70', 1521, service_name='ORCLPDB1')) 
connection = oracledb.connect(user='GROUP1', password='2IGVB44zhK', host='140.117.69.70', port=1521, service_name='ORCLPDB1') 
cursor = connection.cursor()