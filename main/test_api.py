#coding:utf-8

import sys
import os
import unittest
import time

import pytest


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from util.runmethod import RunMethod
from data.get_data import GetData
from util.common_assert import CommonUtil
import json
from data.dependent_data import DependentData
from util.send_mail import SendEmail
from util.print_log import initLogging

class TestRun():

    def test_go_on_run(self):
        global pass_count
        global fail_count
        res = None
        pass_count = []
        fail_count = []
        no_run_count = []
        rows_count = GetData().get_case_lines()

        #每次执行用例之前将log日志文件清空数据
        log_file = '../log/log.txt'
        api_file='../log/api.txt'
        with open(log_file,'w') as f:
            f.seek(0,0) #加上f.seek(0)，把文件定位到position 0;没有这句的话，文件是定位到数据最后，truncate也是从最后这里删除
            f.truncate()
        with open(api_file, 'w') as f1:
            f1.seek(0, 0)  # 加上f.seek(0)，把文件定位到position 0;没有这句的话，文件是定位到数据最后，truncate也是从最后这里删除
            f1.truncate()
        for i in range(1,rows_count):
            try:
                is_run = GetData().get_is_run(i)
                if is_run:
                    url = GetData().get_request_url(i)
                    name = GetData().get_request_name(i)
                    method = GetData().get_request_method(i)
                    #获取请求参数
                    data = GetData().get_data_value(i)
                    # 获取excel文件中header关键字
                    header_key = GetData().get_request_header(i)
                    # 获取json文件中header_key对应的头文件数据
                    header = GetData().get_header_value(i)
                    expect = GetData().get_expect_data(i)
                    depend_case = GetData().is_depend(i)
                    print("第",i,"个接口",name,"请求方式", method, "\n",
                          "请求地址", url, "\n",
                          )
                    with open(api_file, 'a') as f1:
                        f1.write("第%s个接口%s，请求方式%s\n请求地址%s\n" % (i,name,method,url))
                    # initLogging(api_file, 'nice')
                    if depend_case != None:
                        self.depend_data = DependentData(depend_case)
                        #获取依赖字段的响应数据
                        depend_response_data = self.depend_data.get_value_for_key(i)
                        if ',' in str(depend_response_data):
                            #判断依赖字段的数量
                            newdepend_response_data=depend_response_data[0:len(depend_response_data) - 1].split(',')
                            #获取请求依赖的key
                            depend_key = GetData().get_depend_field(i).split(',')
                            for index in range(len(newdepend_response_data)):
                                # 将依赖case的响应返回中某个字段的value赋值给该接口请求中某个参数
                                data[depend_key[index]] = newdepend_response_data[index]
                        else:
                            # 获取请求依赖的key
                            depend_key = GetData().get_depend_field(i)
                            # 将依赖case的响应返回中某个字段的value赋值给该接口请求中某个参数
                            data[depend_key] = str(depend_response_data)
                    # cookie相关的没有跑通，代码逻辑是正常的，但是模拟登陆返回一直是非法请求
                    if header_key == 'write_Cookies':
                        header = {'Content-Type': 'application/json'}
                        data=json.dumps(data)
                        res = RunMethod().run_main(method,url,data,header,params=data)
                        # op_header = OperationHeader(res)
                        # op_header.write_cookie()
                        with open(api_file, 'a') as f1:
                            f1.write("请求参数%s\n" % (data))
                            f1.write("第%s个接口%s响应结果%s\n" % (i,name,res))
                        print("请求参数", data, '\n')
                        print("第", i, "个接口",name,"响应结果\n", res, '\n')

                    # elif header_key == 'get_Cookies':
                    #     op_json = OperationJson('../dataconfig/cookie.json')
                    #     cookie = op_json.get_data('apsid')
                    #     cookies = {'apsid':cookie}
                    #     res = RunMethod().run_main(method,url,data,header=cookies,params=data)
                    #     print( "请求参数", data,'\n')
                    #     print("第",i,"个接口响应结果\n",res,'\n')

                    else:
                        res = RunMethod().run_main(method,url,data,header,params=data)
                        with open(api_file, 'a') as f1:
                            f1.write("请求参数%s\n" % (data))
                            f1.write("第%s个接口%s响应结果%s\n" % (i,name,res))
                        print("请求参数", data, '\n')
                        print("第", i, "个接口",name,"响应结果\n", res,'\n')

                    '''
                    get请求参数是params:request.get(url='',params={}),post请求数据是data:request.post(url='',data={})
                    excel文件中没有区分直接用请求数据表示,则data = GetData().get_data_value(i)拿到的数据，post请求就是data=data,get请就是params=data
                    '''
                    #excel中拿到的expect数据是str类型，但是返回的res是dict类型，两者数据比较必须都是字符类型
                    if CommonUtil().is_contain(expect,json.dumps(res)):
                        GetData().write_result(i,json.dumps(res))
                        pass_count.append(i)
                    else:
                        #返回的res是dict类型，要将res数据写入excel中，需将dict类型转换成str类型
                        GetData().write_result(i,json.dumps(res))
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write("\n第%s条用例实际结果与预期结果不一致:\n" % i)
                            f.write("Expected:%s\n  Actual:%s\n" % (expect,res))
                        fail_count.append(i)
                else:
                    no_run_count.append(i)
            except Exception as e:
                print("\n第%s条用例报错:\n" % i,e,"\n")
                # 将异常写入excel的测试结果中
                GetData().write_result(i, str(e))
                # 将报错写入指定路径的日志文件里
                with open(log_file,'a',encoding='utf-8') as f:
                    f.write("\n第%s条用例报错:\n" % i)
                initLogging(log_file,e)
                fail_count.append(i)


        print("成功", len(pass_count), "失败", fail_count)
        pass_count=pass_count
        fail_count=fail_count
        SendEmail().send_main(pass_count,fail_count)



if __name__ == '__main__':
    # run = RunTest()
    # run.go_on_run()
    pytest.main(["-q", "test_api.py"])



