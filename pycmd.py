import sys,traceback,os
from types import FunctionType
from importlib import import_module
from .cmd.factory.dacmd import CmdMeta
from bdpyconsts import bdpyconsts as pyconst

class CmdBaseConf:
    # project root directory
    __PROJECT_ROOT_DIR = os.path.abspath('.')
    # command script saver relative path
    __CMD_DIR = "cmd"
    # command folder, which can only be a child of the root directory
    __CMD_ROOT_DIR = ""
    # command package import path
    __CMD_MODULE_PATH = ""
    # Internal command import path
    __INNER_CMD_MODEL_PATH = "bdpycmd.cmd.camp"
    # Internal command
    __INNER_CMD = {
        "assistant":CmdMeta(
            number=0,
            name="assistant",
            alias="command assistant",
            desc="Generate execution commands from existing modules"
        )
    }
    # has been initialized
    __initialized = False
    
    @classmethod
    def init(cls,root_dir:str,cmd_dir:str):
        """
        Initialize path configuration
        
        :param root_dir: str project root directory
        :param cmd_dir:  str Subdirectories in the project where commands are stored
        """
        # path formatting
        cls.__PROJECT_ROOT_DIR = root_dir.replace("\\", "/").rstrip("/")
        
        # path formatting
        cls.__CMD_DIR = cmd_dir.replace("\\", "/").strip("./")
        
        # Make sure the project directory is in the system path
        sys.path.append(cls.__PROJECT_ROOT_DIR)
        
        # set command folder
        cls.__CMD_ROOT_DIR = cls.__PROJECT_ROOT_DIR  + "/" + cls.__CMD_DIR
        
        # Set command import path
        cls.__CMD_MODULE_PATH = cls.__CMD_DIR.replace("/", ".")

        # Set to non execution mode
        pyconst._BD_CMD_RUN_NOW = False
    
    
    @classmethod
    def initialized(cls):
        return cls.__initialized

    @classmethod
    def help(cls):
        """
        command line interpreter
        
        :param cmd:      parent command name  If this parameter is omitted, the help is called
        :param son:      subcommand name  If this parameter is omitted, help is called
        :param **kwargs: Subcommand arguments Unsupported arguments are filtered out
        """
        tab = """
        """
        cmders = []
        for _,v in cls.__INNER_CMD.items():
            cmders.append(v)
        
        numb = 1
        for fh in os.listdir(cls.__CMD_ROOT_DIR):
            if fh.endswith('.py') and os.path.isfile(cls.__CMD_ROOT_DIR+'/'+fh) and fh not in ['__init__.py']:
                n = fh[:-3]
                m = import_module(cls.__CMD_MODULE_PATH + "." + n)
                if hasattr(m,"_BDCMD_DESC_"):
                    info = m._BDCMD_DESC_
                else:
                    info = {
                        "name":n,
                        "alias":n,
                        "desc":n
                    }
                info["number"] = numb
                numb += 1
                cmders.append(CmdMeta(**info))
        
        print(str(cls.help.__doc__).lstrip(tab))

        _cmd = cls.search(cms=cmders)

        if not _cmd:
            msg = """
        Target command not found
            """
            print(msg)
        else:
            cls.run(dic_args={
                "cmd":_cmd
            })
    
    @classmethod
    def search(cls,cms:list) -> str:
        """
        Retrieve command list based on keywords

        :param cms: list[CmdMeta] Command Meta Information List
        :return: str Target Command
        """
        keyword = ""
        tag_cmd = ""
        checked = "/"
        exited = "."
        
        head_message = """
        >>> Selection Parent Command : Commands
"""
        print(head_message)
        while True:
            if keyword == exited:
                tag_cmd = ""
                break
            
            if keyword == checked:
                break
            
            if not keyword:
                for _cmd in cms:
                    tag_cmd = _cmd.name
                    keyword = input(_cmd.say()+"\n").lstrip()
                    if not keyword:
                        continue
                    else:
                        break
                else:
                    if not keyword:
                        tag_cmd = ""
                        break
            else:
                print()
                _word = keyword
                keyword = ""
                for _cmd in cms:
                    if _cmd.search(_word):
                        tag_cmd = _cmd.name
                        keyword = input(_cmd.say()+"\n").strip()
                        if not keyword:
                            continue
                        else:
                            break
                else:
                    if not keyword:
                        tag_cmd = ""
                        break
                
        print()
        return tag_cmd

    @classmethod
    def chunk_list(cls,ls:list,size:int):
        """
        Group the list by seize
        
        :param ls: list
        :param size: int #list length
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
            index = i // size
            remain = i % size
            
            if remain == 0:
                res.append([])
            
            res[index].append(ls[i])
        
        return res

    @classmethod
    def find_real_cmder(cls,cmd:object,son:str):
        """
        query parent command
        
        :param cmd: object #parent command class object
        :param son: string #subcommand name
        :return: object #real command object
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
        execute command line
        
        :param kwargs: dict #command line arguments
        :return:
        """
        try:
            # Is it an internal command
            is_inner = True if kwargs['cmd'] in cls.__INNER_CMD else False
            modpth = cls.__INNER_CMD_MODEL_PATH if is_inner and __name__ != "__main__" else cls.__CMD_MODULE_PATH
            
            #import command module
            import importlib
            cmd = importlib.import_module(modpth + '.' + kwargs['cmd'])
            importlib.reload(cmd)

            #Get command execution method
            cmder = cls.find_real_cmder(cmd=cmd.Command,son=kwargs['son'])

            #run command
            if not cmder:
                print('{cmd}`s subcommands `{son}` does not exist'.format(cmd=kwargs['cmd'], son=kwargs['son']))
            else:
                cmder(cmd.Command(),**kwargs)
        except ImportError:
            print('command not exists')
            print(traceback.format_exc())
        except Exception as e:
            print('run command failed: %s ' % str(e))
            print(traceback.format_exc())

    @classmethod
    def run(cls,dic_args:dict=None):
        """
        Receive command line arguments and execute commands
        
        :param dic_args: dict Parameter Dictionary
        :return:
        """
        help_list = ['help', 'h', 'hp', 'hlp']
        args = sys.argv

        # dictionary parameter determination and input parameter analysis
        if not isinstance(dic_args,dict) or "cmd" not in dic_args:
            dic_args = {}
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
            
            # Start Command Execution
            pyconst.unlock()
            pyconst._BD_CMD_RUN_NOW = True
            pyconst.locked()
            cls.run_command(**dic_args)


# execution entry
if __name__ == '__main__':
    # initialization
    if not CmdBaseConf.initialized():
        CmdBaseConf.init(
            root_dir='.',
            cmd_dir='cmd/camp'
        )
    
    # execution
    CmdBaseConf.run()
