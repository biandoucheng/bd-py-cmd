from factory import base

class ttt:
    
    @base.BaseCommand.as_cmder
    def run(self,):
        """
        测试命令
        """
        print("测试创建命令 >>>:\npython pycmd.py -cmd=assistant -son=make_cmd -pkg=factory -name=ttt -pdir=../camp/ -alias=测试命令 -desc=测试命令创建功能")