import sys,traceback,os

"""
全局定义，初始化操作
1、定义项目根目录
2、定义命令包名
3、引入全局包环境
4、设定命令目录
"""
#定义项目根目录
BD_PROJECT_ROOT_DIR = os.path.abspath(os.path.pardir)
#定义命令包名
BD_CMD_DIR = 'camp'
#引入全局包环境
sys.path.append(BD_PROJECT_ROOT_DIR)
#设定命令文件夹
BD_CMD_ROOT_DIR = BD_PROJECT_ROOT_DIR + '/' + BD_CMD_DIR
#设定命令行导入包名
BD_CMD_MODULE_PATH = BD_CMD_DIR.replace("/",'.').replace('\\','.')


def help():
    """
    命令行解释器     引入父级命令并将相关字典参数传入子命令并执行
    :param cmd:      父级命令名称  若忽略该参数则调用该help
    :param son:      子命令名称    若忽略该参数则调用help
    :param **kwargs: 需要传入子命令的参数 不支持的参数会被自动过滤掉
    """
    tab = """
    """
    cmders = [[str(help.__doc__).lstrip(tab)]]
    tmp = ['可用的命令有:']
    for fh in os.listdir(BD_CMD_ROOT_DIR):
        if fh.endswith('.py') and os.path.isfile(BD_CMD_ROOT_DIR+'/'+fh) and fh not in ['__init__.py','base.py']:
            tmp.append(fh.replace('.py',''))
        if len(tmp) == 10:
            cmders.append(tmp)
            tmp = []
    else:
        if tmp:
            cmders.append(tmp)

    for cms in cmders:
        print(tab + ('  '.join(cms)))



def find_real_cmder(cmd:object,son:str):
    """
    通过遍历类及其父类的字典来查询到需要的父级命令实现
    :param cmd: object 父级命令类对象
    :param son: string 子级命令名称
    :return: object 真正的命令实现类
    """
    cmder = cmd.__dict__.get(son)

    if not cmder:
        for parent in cmd.__bases__:
            cmder = parent.__dict__.get(son)
            if cmder:
                break

    return cmder



def run_command(**kwargs):
    """
    执行命令行
    :param kwargs: 命令行参数及命令参数
    :return:
    """
    try:
        #导入命令实例
        cmd = __import__(BD_CMD_MODULE_PATH + '.' + kwargs['cmd'], fromlist=['None'])

        #获取真实的命令执行方法(子命令)
        cmder = find_real_cmder(cmd=cmd.Command,son=kwargs['son'])
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
        print(traceback.format_exc())
        print('{cmd}命令不存在'.format(cmd=kwargs['cmd']))
    except Exception as e:
        print('命令执行失败')
        print(traceback.format_exc())



def run():
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
        help()
    else:
        if 'son' not in dic_args or dic_args['son'] in help_list or not dic_args['son']:
            dic_args['son'] = 'help'
            if 'm' not in dic_args:
                dic_args['m'] = ''

        run_command(**dic_args)



#这里是命令行入口
if __name__ == '__main__':
    run()
