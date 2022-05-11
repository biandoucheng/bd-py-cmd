import os
from ..factory import base

class Command(base.BaseCommand):
    def __init__(self):
        super().__init__(name=__class__.__module__,alias='command assistant',description='command to create it from an existing module')
    
    @base.BaseCommand.as_cmder
    def make_cmd(self,pkg:str,name:str,pdir:str,alias:str,desc:str,inner:str='false'):
        """
        Create a command from a module
        
        :param pkg:   str #Module package path such as: a.b.c
        :param name:  str #Module name, without the .py suffix
        :param pdir:  str #Script storage relative directory
        :param alias: str #command alias
        :param desc:  str #command description
        """
        # Determine if it has the same name as a built-in command
        if name in self.INNER_CMD:
            self.format_print("Command name conflicts with built-in commands")
            return
        
        fn = "%s.py" % name
        f_fn = pdir.replace("\\","/").rstrip("/") + "/" + fn
        
        if os.path.exists(f_fn):
            self.format_print("command already exists")
            return

        if inner == 'true':
            bscmd = '..factory'
        else:
            bscmd = 'bdpycmd.cmd.factory'
        
        tmp = \
        """
from {bscmd} import base
from {pkg} import {name}

class Command(base.BaseCommand,{name}.{name}):
    def __init__(self):
        super().__init__(name=__class__.__module__,alias='{alias}',description='{desc}')
        super(base.BaseCommand,self).__init__()
        """ .format(
            bscmd=bscmd,
            pkg=pkg,
            name=name,
            alias=alias,
            desc=desc
        )
        with open(file=f_fn,mode='w',encoding='utf8') as f:
            f.write(tmp.lstrip())
        
        self.format_print("Command created successfully")
    
    @base.BaseCommand.as_cmder
    def test(self,a=1,b=2):
        """
        test command
        
        :param a: any
        :param b: any
        :return:
        """
        self.format_print(a,b)

        