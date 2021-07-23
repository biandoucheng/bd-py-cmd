# 使用Python3.5 实现的命令行调用方案
### 创建命令行实例时要继承factory.base.BaseCommand
### 并且将命令行类命名为Command
### 通过采用factory.base.format_args可以防止意外参数传入
### 通过从方法名下方的 """注释信息""" 提取方法描述，参数描述，以及其它帮助信息
### 引入其它项目中使用时，需要在pycmd.py中指定好全局参数（项目路径，命令行实例路径，命令行包名 ...）


### Please enjoy it .
