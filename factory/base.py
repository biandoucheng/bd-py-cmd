from functools import wraps
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
        #方法别名容器
        self.method_dict = {}
        #帮助信息中不展示的方法
        self.protected_methods = {'__init__','__find_method','__alias_this_method','__format_args'}



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

        class_objects = [self.__class__]
        for base_class in self.__class__.__bases__:
            if base_class.__name__ == 'BaseCommand':
                continue
            else:
                class_objects.append(base_class)

        for class_object in class_objects:
            class_name = class_object.__name__
            for k, v in vars(class_object).items():
                k = k.replace(class_name + '_', '')
                if k in self.protected_methods:
                    continue
                if not k.startswith('__') and 'function' in str(v) or 'method' in str(v):
                    hps.append(tab + k + '  ' + v.__doc__.lstrip(tab))
                    if self.__find_method(m, k):
                        hps = {hps[0], hps[-1]}
                        hps = list(hps)
                        break


        self.format_print(infos=hps)



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



    def __find_method(self,m:str,name:str):
        """
        __find_method   查询当前方法是否与方法参数匹配
        :param m: string 输入的方法名
        :param name: string 当前对比的方法名
        :return: bool 是否匹配
        """
        if m.lower() == name.lower():
            return True

        alias = self.method_dict.get(name)
        if not isinstance(alias,set):
            return False

        if alias and m.lower() in alias:
            return True

        return False



    def __alias_this_method(self,name:str,alias:list):
        """
        给一个方法添加别名
        :param name: string 方法名
        :param alias: list 别名列表
        :return:
        """

        if name not in self.method_dict:
            self.method_dict[name] = set()

        for a in alias:
            self.method_dict[name].add(str(a).lower())



    @staticmethod
    def format_args(fun):
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

        return wrapper
