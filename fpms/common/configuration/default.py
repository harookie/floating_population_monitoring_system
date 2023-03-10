#--coding:utf-8


import yaml
from dataclasses import dataclass

from nmsplus.common.configure import UserdefineObjectLoadHandler
from nmsplus.common.configure.db import MariaConnInfo_NT, DBConfig
from nmsplus.common import log



    
@dataclass
class DefaultConfig:
    db_config: DBConfig
    log_path: str = './'
    log_level: str = 'INFO'
           

class DefaultConfigHandler(UserdefineObjectLoadHandler):
    def load_object(self):
        '''사용자 정의 객체에 대한 yaml parsing 처리 추가
        '''
        yaml.add_constructor('!DefaultConfig',  self._make_object)
        yaml.add_constructor('!DBConfig',  self._make_object)
        yaml.add_constructor('!MariaConnInfo_NT',  self._make_object)
        
        
    def _make_object(self, loader:yaml.Loader, node:yaml.Node):
        class_name_d = {
                        '!DefaultConfig': DefaultConfig,
                        '!DBConfig': DBConfig,
                        '!MariaConnInfo_NT': MariaConnInfo_NT,
                       }

        if node.tag in class_name_d:
            return class_name_d[node.tag](**loader.construct_mapping(node))
        
        
 


if __name__ == '__main__':
    from nmsplus.common.configure import NmsplusConfigureManager
    config_o:DefaultConfig = NmsplusConfigureManager.create_instance_profile('dev', 'default.yaml', DefaultConfigHandler()).config
    print(config_o.db_config)
    print(config_o.db_config.get_conn_info('nmsplus'))