from functools import wraps
from types import FunctionType
import re

class BaseCommand:
    # Internal command
    INNER_CMD = {"assistant"}
    
    def __init__(self,name='',alias='',description=''):
        """
        Initialize the command
        
        :param alias: str #alias for the command
        :param description: str #a description of the function of the command
        """
        self.name = name.split('.')[-1] + '.Command'
        self.alias = alias + 'command'
        self.description = description
        self.info = """
        {name}  {alias} {description}
        """.format(
            name=self.name,
            alias=self.alias,
            description=self.description
        )
        #Methods not shown in the help information
        self.protected_methods = {'__init__','as_cmder'}


    def help(self,m=''):
        """
        help    Help method, output help information
        """
        tab = """
        """
        if not isinstance(m,str):
            m = ''

        #help output command
        hps = [self.info]

        #Handling inheritance of command classes
        class_objects = [self.__class__]
        self.deep_clss(self.__class__,class_objects)

        #Traverse the object members of the command class and the parent class
        # inherited by the command class to find the command method
        for class_object in class_objects:
            class_name = class_object.__name__
            for k, v in vars(class_object).items():
                k = k.replace(class_name + '_', '')
                if k in self.protected_methods:
                    continue
                
                if not k.startswith('_') and isinstance(v,FunctionType) and v.__name__.endswith('___bdcmder'):
                    hps.append(tab + k + '  ' + str(v.__doc__).lstrip(tab))

        self.format_print(infos=hps)

    def deep_clss(self,obj:object,clss:list):
        """
        Recursively complete inherited class query
        
        :param obj: object #initial class
        :param clss: list #target class list
        """
        for it in obj.__bases__:
            if it.__name__ == 'BaseCommand' or it == object:
                continue
            else:
                clss.append(it)
                self.deep_clss(it,clss=clss)

    def format_print(self,*args,infos:list=[],ft:bool=True):
        """
        formatted print
        
        :param infos: list #List of information to be printed
        :param ft: bool #Lines beyond the first line are indented
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
        Parameter formatting method. 
        All available command methods need to use this modifier to filter out illegal parameters. 
        Note that the parameter annotation of the method must be standardized, 
        otherwise the parameters will not be correctly filtered out.
        
        :param kwargs: dict #Character typical parameters
        :return:
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