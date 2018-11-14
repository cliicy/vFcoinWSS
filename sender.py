#  -*- coding:utf-8 -*-
import pika
import sys


class MqSender:
    """
    mq消息生产者
    """
    rabbitmq_host = "51facai.51vip.biz"
    rabbitmq_port = "50896"
    # rabbitmq_host = "10.0.131.74"
    # rabbitmq_port = "5672"
    rabbitmq_username = "guest"
    rabbitmq_pwd = "guest"
    queue_name = ''

    def __init__(self, platform, data_type):
        username = self.rabbitmq_username  # 指定远程rabbitmq的用户名密码
        pwd = self.rabbitmq_pwd
        s_conn = None
        ret = 'succeed'
        try:
            user_pwd = pika.PlainCredentials(username, pwd)
            self.s_conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=user_pwd))  # 创建连接
        except IOError:
            print('cannot open', sys.exc_info()[0])
            ret = 'error'
        except Exception as err:
            print("Unexpected error:", err)
            ret = 'error'
        finally:
            print(ret)
            if ret == 'error':
                print('error will not write data to mq', self.s_conn)
            else:
                print("isopen", self.s_conn.is_open)
                self.chan = self.s_conn.channel()  # 在连接上创建一个频道
                self.queue_name = '%s_%s' % (platform, data_type)
                # self.chan.queue_declare(queue=self.queue_name)  # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行

    def send(self, msg):
        if self.s_conn.is_closed:
            self.conn_()

        self.chan.basic_publish(exchange='',  # 交换机
                           routing_key=self.queue_name,  # 路由键，写明将消息发往哪个队列，本例是将消息发往队列hello
                           body=msg)  # 生产者要发送的消息

        print("send ", self.queue_name + "#")
        print("send ", msg)

    def conn_(self):
        username = self.rabbitmq_username  # 指定远程rabbitmq的用户名密码
        pwd = self.rabbitmq_pwd
        user_pwd = pika.PlainCredentials(username, pwd)
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=user_pwd))  # 创建连接
        self.chan = self.s_conn.channel()

    def close(self):
        self.s_conn.close()  # 当生产者发送完消息后，可选择关闭连接


if __name__ == '__main__':
    sender = MqSender("huobi", "kline")
    sender.send("{'e': 'trade', 'E': 1534216038532, 's': 'BCCUSDT',"
                " 't': 7962795, 'p': '484.30000000', 'q': '0.53500000',"
                " 'b': 44015203, 'a': 44015210, 'T': 1534216038531, 'm': True, 'M': True}")
    sender.send("bbb")
    sender.send("aaccca")
    sender.close()
