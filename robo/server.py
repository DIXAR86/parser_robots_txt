import time
from concurrent import futures

import grpc

import checklink
import checklink_pb2
import checklink_pb2_grpc


class CheckLinkServicer(checklink_pb2_grpc.CheckLinkServicer):

    def checklink_access(self, request, context):
        response = checklink_pb2.Text()
        response.data = checklink.checklink_access(request.data)
        return response

    def checklink_crwdelay(self, request, context):
        response = checklink_pb2.Text()
        response.data = checklink.checklink_crwdelay(request.data)
        return response


def serve():
    # создаем сервер
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

    # прикреплям хандлеры
    checklink_pb2_grpc.add_CheckLinkServicer_to_server(CheckLinkServicer(), server)

    # запускаемся на порту 6066
    print('Starting server on port 6066.')
    server.add_insecure_port('[::]:6066')
    server.start()

    # работаем час или до прерывания с клавиатуры
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
