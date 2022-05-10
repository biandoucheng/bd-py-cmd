import sys,traceback,os
from types import FunctionType

class CmdBaseConf:
    # 项目根目录
    __PROJECT_ROOT_DIR = os.path.abspath('.')
    # 命令脚本存户相对路径
    __CMD_DIR = "cmd"
    # 命令文件夹,该文件夹只能是根目录的子级
    __CMD_ROOT_DIR = ""
    # 命令包导入路径
    __CMD_MODULE_PATH = ""
    # 内部命令导入路径
    __INNER_CMD_MODEL_PATH = "bdpycmd.cmd.camp"
    # 内部命令
    __INNER_CMD = {"assistant"}
    # 是否已经被初始化
    __initialized = False
    
    @classmethod
    def init(cls,root_dir:str,cmd_dir:str):
        """
        初始化路径配置
        
        :param root_dir: str 项目根目录
        :param cmd_dir:  str 项目中存放命令的子目录
        """
        # 路径去斜杠
        cls.__PROJECT_ROOT_DIR = root_dir.replace("\\", "/").rstrip("/")
        
        # 相对路径格式化
        cls.__CMD_DIR = cmd_dir.replace("\\", "/").strip("./")
        
        # 确保项目目录在系统路径中
        sys.path.append(cls.__PROJECT_ROOT_DIR)
        
        # 设置命令文件夹
        cls.__CMD_ROOT_DIR = cls.__PROJECT_ROOT_DIR  + "/" + cls.__CMD_DIR
        
        # 设置命令导入路径
        cls.__CMD_MODULE_PATH = cls.__CMD_DIR.replace("/", ".")
    
    
    @classmethod
    def initialized(cls):
        return cls.__initialized

    @classmethod
    def help(cls):
        """
        命令行解释器     引入父级命令并将相关字典参数传入子命令并执行
        :param cmd:      父级命令名称  若忽略该参数则调用该help
        :param son:      子命令名称    若忽略该参数则调用help
        :param **kwargs: 需要传入子命令的参数 不支持的参数会被自动过滤掉
        """
        tab = """
        """
        headers = [[str(cls.help.__doc__).lstrip(tab)],['可用的命令有:']]
        
        cmders = cls.__INNER_CMD
        
        for fh in os.listdir(cls.__CMD_ROOT_DIR):
            if fh.endswith('.py') and os.path.isfile(cls.__CMD_ROOT_DIR+'/'+fh) and fh not in ['__init__.py']:
                cmders.add(fh.replace('.py',''))

        cmders = cls.chunk_list(list(cmders),5)
        headers.extend(cmders)

        for cms in headers:
            print(tab + ('  '.join(cms)))

    @classmethod
    def chunk_list(cls,ls:list,size:int):
        """
        将列表按照seize分组
        :param ls: list 列表
        :param size: int 大小
        :return: list
        """
        if not list:
            return ls
        
        if size <= 0:
            size = 1
        
        if size == 1:
            return [[i] for i in ls]
        
        res = []
        for i in range(len(ls)):
            index = int(i / size)
            remain = i % size
            
            if remain == 0:
                res.append([])
            
            res[index].append(ls[i])
        
        return res

    @classmethod
    def find_real_cmder(cls,cmd:object,son:str):
        """
        通过遍历类及其父类的字典来查询到需要的父级命令实现
        :param cmd: object 父级命令类对象
        :param son: string 子级命令名称
        :return: object 真正的命令实现类
        """
        if not hasattr(cmd,son):
            return None
        
        val = getattr(cmd,son)
        if not isinstance(val,FunctionType):
            return None
        
        return val

    @classmethod
    def run_command(cls,**kwargs):
        """
        执行命令行
        :param kwargs: 命令行参数及命令参数
        :return:
        """
        try:
            # 判断是否是内部命令
            is_inner = True if kwargs['cmd'] in cls.__INNER_CMD else False
            modpth = cls.__INNER_CMD_MODEL_PATH if is_inner and __name__ != "__main__" else cls.__CMD_MODULE_PATH
            
            #导入命令实例
            cmd = __import__(modpth + '.' + kwargs['cmd'], fromlist=['None'])

            #获取真实的命令执行方法(子命令)
            cmder = cls.find_real_cmder(cmd=cmd.Command,son=kwargs['son'])
            if kwargs['son'] == 'help':
                kwargs = {
                    'm':kwargs['m']
                }

            #执行命令
            if not cmder:
                print('{cmd}的子命令{son}不存在'.format(cmd=kwargs['cmd'], son=kwargs['son']))
            else:
                cmder(cmd.Command(),**kwargs)
        except ImportError:
            print('命令不存在')
            print(traceback.format_exc())
        except Exception as e:
            print('命令执行失败: %s ' % str(e))
            print(traceback.format_exc())

    @classmethod
    def run(cls):
        """
        接收命令行参数，并执行相应命令
        :return:
        """
        help_list = ['help', 'h', 'hp', 'hlp']
        dic_args = {}
        args = sys.argv

        # 参数转字典
        if len(args) < 2:
            dic_args['cmd'] = 'help'
        else:
            for it in args[1:]:
                its = str(it).split('=')
                if len(its) >= 2:
                    k = its[0].lstrip('-')
                    dic_args[k] = '='.join(its[1:]).strip('=')

        if 'cmd' not in dic_args:
            dic_args['cmd'] = 'help'

        if dic_args['cmd'] in help_list:
            cls.help()
        else:
            if 'son' not in dic_args or dic_args['son'] in help_list or not dic_args['son']:
                dic_args['son'] = 'help'
                if 'm' not in dic_args:
                    dic_args['m'] = ''

            cls.run_command(**dic_args)


# 执行入口
if __name__ == '__main__':
    # 初始化
    if not CmdBaseConf.initialized():
        CmdBaseConf.init(
            root_dir='.',
            cmd_dir='cmd/camp'
        )
    
    # 执行
    CmdBaseConf.run()
