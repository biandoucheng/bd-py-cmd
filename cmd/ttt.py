from .factory import base
from cmd.script import ttt

class Command(base.BaseCommand,ttt.ttt):
    def __init__(self):
        super().__init__(name=__class__.__module__,alias='测试命令',description='测试命令创建功能')
        super(base.BaseCommand,self).__init__()
        