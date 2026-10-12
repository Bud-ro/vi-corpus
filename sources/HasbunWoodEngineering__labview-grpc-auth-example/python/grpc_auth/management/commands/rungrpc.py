from concurrent import futures

import grpc
from django.core.management.base import BaseCommand

from grpc_auth.services import AuthService


class Command(BaseCommand):
    help = "Run the gRPC authentication server."

    def add_arguments(self, parser):
        parser.add_argument(
            "--port",
            type=int,
            default=50051,
            help="Port to bind the gRPC server on (default: 50051)",
        )

    def handle(self, *args, **options):
        port = options["port"]
        try:
            from grpc_auth import auth_pb2_grpc
        except ModuleNotFoundError:
            self.stderr.write(
                "gRPC stubs not found. Generate them with:\n"
                "  python -m grpc_tools.protoc -I grpc_auth --python_out=grpc_auth --grpc_python_out=grpc_auth grpc_auth/auth.proto"
            )
            return
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
        server.add_insecure_port(f"[::]:{port}")
        self.stdout.write(
            self.style.SUCCESS(f"gRPC server listening on 0.0.0.0:{port}")
        )
        server.start()
        server.wait_for_termination()
