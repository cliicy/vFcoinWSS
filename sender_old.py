#  -*- coding:utf-8 -*-
import pika
import sys
from config import rabbitmq_host
from config import rabbitmq_pwd
from config import rabbitmq_username
from config import rabbitmq_port


class MqSender:
    """
    mq消息生产者
    """
    rabbitmq_host = rabbitmq_host
    rabbitmq_port = rabbitmq_port
    rabbitmq_username = rabbitmq_username
    rabbitmq_pwd = rabbitmq_pwd
    queue_name = ''

    def __init__(self, platform, data_type):
        username = self.rabbitmq_username  # 指定远程rabbitmq的用户名密码
        pwd = self.rabbitmq_pwd
        user_pwd = pika.PlainCredentials(username, pwd)
        try:
            self.s_conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=user_pwd))  # 创建连接
        except IOError:
            print('cannot open', sys.exc_info()[0])
            return None
        except Exception as err:
            print("sender Unexpected error:", err)
            return None
        print("isopen", self.s_conn.is_open)
        self.chan = self.s_conn.channel()  # 在连接上创建一个频道
        self.queue_name = '%s_%s' % (platform, data_type)
        # self.chan.queue_declare(queue=self.queue_name)  # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行

    def send(self, msg):
        # if msg is None:
        #     msg = ""
        if self.s_conn.is_closed:
            self.conn_()
        self.chan.exchange_declare(
            exchange='db_type',
            exchange_type='topic'
        )
        self.chan.basic_publish(exchange='db_type',  # 交换机
                           routing_key=self.queue_name,
                           body=msg)  # 生产者要发送的消息
        print("send ", msg)
        print("send ", self.queue_name + "#")

    def conn_(self):
        username = self.rabbitmq_username  # 指定远程rabbitmq的用户名密码
        pwd = self.rabbitmq_pwd
        user_pwd = pika.PlainCredentials(username, pwd)
        self.s_conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=user_pwd))  # 创建连接
        self.chan = self.s_conn.channel()

    def close(self):
        self.s_conn.close()  # 当生产者发送完消息后，可选择关闭连接


if __name__ == '__main__':
    sender = MqSender("fcoin", "kline")
    sender.close()
