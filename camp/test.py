from factory import base


class Command(base.BaseCommand):
    def __init__(self):
        super().__init__(name=__class__.__module__,alias='测试',description='测试命令组件是否可以正常执行')


    @base.BaseCommand.format_args
    def test(self,a=1,b=2):
        """
        测试用例
        :param a: 参数 a
        :param b: 参数 b
        :return:
        """
        self.format_print(a,b)


    @base.BaseCommand.format_args
    def test2(self):
        """
        测试方法2
        :return:
        """
