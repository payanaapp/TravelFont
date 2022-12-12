from flask import Flask, request, Blueprint
from payana.payana_service.server import payana_bigtable_server_init


def run():
    payana_bigtable_server_init.initialize_app()
    
def main():
    payana_bigtable_server_init.initialize_app()

if __name__ == "__main__":
    main()
