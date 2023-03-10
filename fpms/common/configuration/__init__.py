#--coding:utf-8


import os
import yaml
from abc import abstractclassmethod, abstractmethod

from nmsplus.common import log


class UserdefineObjectLoadHandler:
    @abstractmethod
    def load_object(cls): pass



class NmsplusConfigureManager:
    SEC_ROOT = 'CONFIG'
    
    def __init__(self, config_d:dict):
        if isinstance(config_d, dict):
            self._config_d = config_d
        else:
            raise Exception(f'Configuration 정보는 dict 형태 여야 합니다.(config_d={type(config_d)}') 
        
        
    def __repr__(self):
        return f'<{self.__class__.__name__}:{self._config_d}>'
    
    
    @property
    def config(self):
        return self._config_d.get(self.SEC_ROOT, None)
            
        
    @classmethod
    def create_instance_profile(cls, profile:str, filename:str, userobject_loader:UserdefineObjectLoadHandler=None):
        ''' 실행환경 정보 조회하여 ConfigureManager 인스턴스 전달

        :param profile: 실행환경 조회할 profile명
        :param filename: 실행환경 파일명. (파일 포멧: yaml)
        :return: ConfigureManager 인스턴스
        '''
        service_home = os.path.join(os.environ['SERVICE_HOME'])
        yaml_path = os.path.join(service_home, 'resource', profile.lower(), 'configuration', filename)
        
        log.debug(yaml_path)
        config_d = cls.load_configuration(yaml_path, userobject_loader)
        
        return cls(config_d)
    
    @classmethod
    def create_instance_filename(cls, pathfilename:str, userobject_loader:UserdefineObjectLoadHandler=None):
        yaml_filename = os.path.expandvars(pathfilename)
        config_d = cls.load_configuration(yaml_filename, userobject_loader)
        
        return cls(config_d)
    
    
    @classmethod
    def load_configuration(cls, yaml_filename:str, userobject_loader:UserdefineObjectLoadHandler=None):                
        if not os.path.exists(yaml_filename) : 
            raise Exception(f'Configuration 파일이 존재하지 않습니다.({yaml_filename})')
        
        # cls._load_userdefine_object()
        if userobject_loader:
            userobject_loader.load_object()
            
        with open(yaml_filename) as yaml_fid:
            config_d = yaml.load(yaml_fid, yaml.FullLoader)
            
        return config_d
    
    
    @classmethod
    @abstractclassmethod
    def _load_userdefine_object(cls):
        '''사용자 정의 객체에 대한 yaml parsing 처리 추가
        '''
        pass
    
    
