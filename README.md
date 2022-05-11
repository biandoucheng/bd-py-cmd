# 使用Python3 实现的命令行调用方案
## 使用方法
`
用于将python代码以命令行的形式运行
    使用：
    pip install bdpycmd

    your_project_root_dir:
        | your_cmd_dir
            | your_cmd_1.py
                from bdpycmd.cmd.factory import base
                
                class Command(base.BaseCommand)
                    def __init__(self):
                        super().__init__(name=__class__.__module__,alias='xxx',description='xxxx')
                    
                    @base.BaseCommand.as_cmder
                    your_function()
                        """
                        你的方法描述信息
                        
                        :param p1: str xxx
                        :param p2: str xxx
                        ...
                        """
            
            | your_cmd_2.py
                from your_script_package import your_script_name
                from bdpycmd.cmd.factory import base
                
                class Command(base.BaseCommand,your_script_name.your_script_class):
                    def __init__(self,):
                        super().__init__(name=self.__class__.__module__,alias='xxx',description='xxxxxx')
                        super(base.BaseCommand,self).__init__()        
    
        | pycmd.py
            from  bdpycmd.cmd import *
            
            CmdBaseConf.init(
                root_dir='.',
                cmd_dir='your_cmd_dir'
            )
            
            if __name__ == '__main__':
                CmdBaseConf.run()
    
    
    run: python pycmd.py -cmd=xxx -son=xxx -p1=xx -p2=xxx
`