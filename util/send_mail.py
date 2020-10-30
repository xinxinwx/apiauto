import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime

class SendEmail:
    global send_user
    global email_host
    global password
    email_host = "smtp.qq.com"
    send_user = "380222985@qq.com"
    password = "eyteexarlvghbhhg"



    def send_main(self,pass_list,fail_list):
        # 邮件发送给谁
        user_list = ['380222985@qq.com']

        user = "测试报告" + "<" + send_user + ">"
        message = MIMEMultipart()

        message['From'] = user
        message['To'] = ";".join(user_list)
        pass_num=float(len(pass_list))
        fail_num=float(len(fail_list))
        count_num=pass_num+fail_num
        #取小数点后两位
        pass_result="%.2f%%" %(pass_num/count_num*100)
        fail_result="%.2f%%" %(fail_num/count_num*100)
        content = "此次一共运行接口个数为{}个,通过个数为{}个,失败个数为{},通过率为{},失败率为{}".format(count_num, pass_num, fail_num, pass_result,
                                                                   fail_result)
        sub = content
        message['Subject'] = sub

        filename = '../log/log.txt'
        time = datetime.date.today()
        att = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s_Log.txt"' % time
        message.attach(att)

        apifilename = '../log/api.txt'
        time = datetime.date.today()
        att = MIMEText(open(apifilename, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s_Api.txt"' % time
        message.attach(att)



        # part=MIMEText(self.getcontent(pass_num,fail_num))
        # message.attach(part)
        # f=open('../main/bg.html', 'rb')
        # part=MIMEApplication(f.read())
        # f.close()
        # part.add_header('Content-Disposition','attachment',filename='%s_测试报告.html' % time)
        # message.attach(part)
        # windows发送邮件
        # server = smtplib.SMTP()
        # server.connect(email_host)
        # linux发送邮件
        server = smtplib.SMTP_SSL(email_host, 465)
        server.login(send_user, password)
        server.sendmail(send_user,user_list,message.as_string())
        server.close()


    def getcontent(self,pass_num,fail_num):
         count_num = pass_num + fail_num
         # 取小数点后两位
         pass_result = "%.2f%%" % (pass_num / count_num * 100)
         fail_result = "%.2f%%" % (fail_num / count_num * 100)
         content = "此次一共运行接口个数为{}个,通过个数为{}个,失败个数为{},通过率为{},失败率为{}".format(count_num, pass_num, fail_num, pass_result,fail_result)
         return content



if __name__ == '__main__':
    sen = SendEmail()

    # user_list = ['380222985@qq.com']
    # sub = '这个是测试邮件'
    # content = '这个是强强测试的邮件'
    sen.send_main([],[1,2,3])
