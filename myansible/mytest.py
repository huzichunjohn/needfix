#!/usr/bin/python

class Test(object):
    def __init__(self):
	self.test = True

    def hello(self):
	print self.test

class MyTest(Test):
    def __init__(self):
	self.test = False
	print self.test
	super(MyTest, self).__init__()
	print self.test

    def hello(self):
	print self.test



if __name__ == "__main__":
    test = MyTest()
    test.hello()
