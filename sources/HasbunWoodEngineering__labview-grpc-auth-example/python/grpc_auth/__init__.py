from importlib import import_module
import sys

# Make generated gRPC modules importable both as grpc_auth.auth_pb2
# and as top-level auth_pb2, which grpc_tools generates.
try:
    _messages = import_module(".auth_pb2", package=__name__)
    sys.modules.setdefault("auth_pb2", _messages)
    _services = import_module(".auth_pb2_grpc", package=__name__)
    sys.modules.setdefault("auth_pb2_grpc", _services)
except Exception:
    # Generated stubs may not exist yet.
    pass
