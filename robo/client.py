import grpc

import checklink_pb2
import checklink_pb2_grpc


# открываем канал и создаем клиент
channel = grpc.insecure_channel('localhost:6066')
stub = checklink_pb2_grpc.CheckLinkStub(channel)

# текст для хеширования
#text = 'https://habr.com/ru/post/467607/'
text = input(str('введите ссылку: '))

# запрос за md5
to_checklink_access = checklink_pb2.Text(data=text)
response = stub.checklink_access(to_checklink_access)
print(response.data)

# запрос за ha256
to_checklink_crwdelay = checklink_pb2.Text(data=text)
response = stub.checklink_crwdelay(to_checklink_crwdelay)
print(response.data)
