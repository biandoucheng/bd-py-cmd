from functools import wraps
from types import FunctionType
import re

class BaseCommand:
    def __init__(self,name='',alias='',description=''):
        """
        初始化命令类
        :param alias: 该命令类的别名
        :param description: 对该命令功能的描述
        """
        self.name = name.split('.')[-1] + '.Command'
        self.alias = alias + '命令'
        self.description = description
        self.info = """
        {name}  {alias} {description}
        """.format(
            name=self.name,
            alias=self.alias,
            description=self.description
        )
        #帮助信息中不展示的方法
        self.protected_methods = {'__init__','as_cmder'}


    def help(self,m=''):
        """
        help    帮助方法    输出帮助信息
        """
        tab = """
        """
        if not isinstance(m,str):
            m = ''

        #输出命令的帮助信息
        hps = [self.info]

        #处理命令类的继承
        class_objects = [self.__class__]
        self.deep_clss(self.__class__,class_objects)

        #遍历命令类及命令类继承的一级子类的对象成员，找出命令方法
        for class_object in class_objects:
            class_name = class_object.__name__
            for k, v in vars(class_object).items():
                k = k.replace(class_name + '_', '')
                if k in self.protected_methods:
                    continue
                
                if not k.startswith('_') and isinstance(v,FunctionType) and v.__name__.endswith('___bdcmder'):
                    hps.append(tab + k + '  ' + v.__doc__.lstrip(tab))

        self.format_print(infos=hps)

    def deep_clss(self,obj:object,clss:list):
        """
        递归完成继承类查询
        
        :param obj: object 初始类
        :param clss: list 目标类集合
        """
        for it in obj.__bases__:
            if it.__name__ == 'BaseCommand' or it == object:
                continue
            else:
                clss.append(it)
                self.deep_clss(it,clss=clss)

    def format_print(self,*args,infos:list=[],ft:bool=True):
        """
        格式化打印
        :param infos: list 需要打印的信息列表
        :param ft: bool 首行之外的行加缩进
        :return:
        """
        tab = """
    """
        print(tab,*args)
        for info in infos:
            if ft:
                print(info)
                ft = False
            else:
                print('    '+info)


    @staticmethod
    def as_cmder(fun):
        """
        参数格式化方法 所有可用命令方法均需使用该修饰器 用于过滤掉非法参数
        注意方法的参数注释必须要规范，否则将不能正确过滤掉参数
        :param kwargs: dict 字典型参数
        :return: 方法本身的返回值
        """
        @wraps(fun)
        def wrapper(self,**kwargs):
            args_regex = re.compile(r':param\s([\w]+):',re.DOTALL)
            dc = fun.__doc__
            if not dc:
                dc = ''
            all_arg_names = args_regex.findall(dc)
            target = {}
            for k in all_arg_names:
                if k in kwargs:
                    target[k] = kwargs[k]
            return fun(self,**target)

        wrapper.__name__ = wrapper.__name__ + '___bdcmder'
        return wrapper