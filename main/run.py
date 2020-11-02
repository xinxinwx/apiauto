import unittest

import pytest

if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # test_cases = [RunTest('go_on_run')]
    # suite.addTests(test_cases)
    # with open("bg.html", "wb") as file:
    #     runner = HTMLTestRunnerNew.HTMLTestRunner(
    #         stream=file,
    #         verbosity=2,
    #         title="测试报告",
    #         description="",
    #         tester='李帅磊'
    #     )
    #     runner.run(suite)
    #     unittest.main()
    # 要执行的测试用例
    case_path = 'test_api.py'
    xml_report_path = 'html'
    # args = ['-s', '-q', case_path, '--html=html/bg.html']
    args = ['-s', '-q', case_path, '--allure-report=html/allure-report']
    pytest.main(args=args)