from threading import Thread

from flask import current_app, render_template
from flask_mail import Mail, Message

def thread_tasks(app,mail,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to,subject,filename,**kwargs):
    """
      发送邮件的封装
      :param to: 收件人
      :param subject: 邮件主题
      :param filename: 邮件正文对应的html名称
      :param kwargs: 关键字参数, 模版中需要的变量名
      :return:
    """
    # 获取当前app的配置信息
    app = current_app._get_current_object()
    mail = Mail(app)
    msg = Message(subject=subject,
            recipients=to,
            sender=app.config['MAIL_USERNAME']
            )
    # msg.body = 'westos'
    msg.html = render_template(filename+'.html',**kwargs)
    # 启动多线程执行发送邮件的任务
    thread = Thread(target=thread_tasks,args=(app,mail,msg))
    thread.start()