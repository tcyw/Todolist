"""
File:manage.py
Author:Tcyw
Date:2020-03-07
Connect:741047561@qq.com
Description:

"""
from app import create_app


app = create_app()
# 通过命令行管理服务器配置
from flask_script import Manager,Shell
manager = Manager(app)
# manager.run()
@manager.command
def test():
    """
    执行Flask项目的测试用例
    :return:
    """
    import unittest
    # 发现所有的测试用例（Testcase）绑定成一个测试集合（testsuite）
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
if __name__ == '__main__':
    manager.run()
