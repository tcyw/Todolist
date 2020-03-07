"""
File:test_number.py
Author:Tcyw
Date:2020-03-08
Connect:741047561@qq.com
Description:

"""
import unittest
import random

class TestSequenceFunctions(unittest.TestCase):
    """
        setUp() 和 tearDown() 方法分别在各测试前后运行,并且名字以 test_ 开头的函数都作为测试
    执行。

    """
    def setUp(self) -> None:
        self.seq = [0,1,2,3,4,5,6,7,8]
    def test_choice_ok(self):
        item = random.choice(self.seq)
        result = item in self.seq
        self.assertTrue(result)
    def test_sample_ok(self):
        result = random.sample(self.seq,4)
        self.assertEqual(len(result),4)
    def tearDown(self) -> None:
        del self.seq









