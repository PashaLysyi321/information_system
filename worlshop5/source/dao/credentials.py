import cx_Oracle

username = 'SYSTEM'
password = 'oracle'
ip = 'localhost'
port = 1521
service_name = 'XE'
dsn = cx_Oracle.makedsn(ip, port, service_name=service_name)
databaseName = dsn

DIALECT = 'oracle'
SQL_DRIVER = 'cx_oracle'
USERNAME = 'SYSTEM'
PASSWORD = 'oracle'

HOST = 'localhost'
PORT = 1521
SERVICE = 'orcl'

ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE
