# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import checklink_pb2 as checklink__pb2


class CheckLinkStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.
    Args:
      channel: A grpc.Channel.
    """
    self.checklink_access = channel.unary_unary(
        '/CheckLink/checklink_access',
        request_serializer=checklink__pb2.Text.SerializeToString,
        response_deserializer=checklink__pb2.Text.FromString,
        )
    self.checklink_crwdelay = channel.unary_unary(
        '/CheckLink/checklink_crwdelay',
        request_serializer=checklink__pb2.Text.SerializeToString,
        response_deserializer=checklink__pb2.Text.FromString,
        )


class CheckLinkServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def checklink_access(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def checklink_crwdelay(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CheckLinkServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'checklink_access': grpc.unary_unary_rpc_method_handler(
          servicer.checklink_access,
          request_deserializer=checklink__pb2.Text.FromString,
          response_serializer=checklink__pb2.Text.SerializeToString,
      ),
      'checklink_crwdelay': grpc.unary_unary_rpc_method_handler(
          servicer.checklink_crwdelay,
          request_deserializer=checklink__pb2.Text.FromString,
          response_serializer=checklink__pb2.Text.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'CheckLink', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))