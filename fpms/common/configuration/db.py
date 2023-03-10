#--coding:utf-8


from collections import namedtuple
from dataclasses import dataclass


MariaConnInfo_NT = namedtuple('MariaConnInfo_NT', ['user', 'password', 'database', 'host', 'port', 'charset'])    

@dataclass
class DBConfig:
    conn_infos: dict
            
    def get_conn_info(self, db_nm:str) -> dict:
        return self.conn_infos[db_nm]._asdict()
    
    def get_conn_url_mysql(self, db_nm:str) -> str:
        dbsvc:MariaConnInfo_NT = self.conn_infos[db_nm]
        return f'mysql+mysqldb://{dbsvc.user}:{dbsvc.password}@{dbsvc.host}:{dbsvc.port}/{dbsvc.database}'
    
