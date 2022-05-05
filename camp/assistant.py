import os
from factory import base

class Command(base.BaseCommand):
    def __init__(self):
        super().__init__(name=__class__.__module__,alias='助手',description='命令助手')
    
    @base.BaseCommand.as_cmder
    def make_cmd(self,pkg:str,name:str,pdir:str,alias:str,desc:str):
        """
        根据脚本创建一个命令
        
        :param pkg:   str 脚本包路径
        :param name:  str 脚本名称
        :param pdir:  str 脚本存放目录
        :param alias: str 脚本别名
        :param desc:  str 脚本描述
        """
        fn = "%s.py" % name
        f_fn = pdir.replace("\\","/").rstrip("/") + "/" + fn
        
        if os.path.exists(f_fn):
            print("""
        命令已存在
                  """)
            return

        tmp = \
        """
from factory import base
from {pkg} import {name}

class Command(base.BaseCommand,{name}.{name}):
    def __init__(self):
        super().__init__(name=__class__.__module__,alias='{alias}',description='{desc}')
        super(base.BaseCommand,self).__init__()
        """ .format(
            pkg=pkg,
            name=name,
            alias=alias,
            desc=desc
        )
        
        with open(file=f_fn,mode='w',encoding='utf8') as f:
            f.write(tmp.lstrip())
        
        print("""
        命令创建成功
              """)
        