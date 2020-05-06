import functools
import json
import sys
import socket

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE, deserialize, serialize
from node_ring import NodeRing
from lru_cache import LRUCache

BUFFER_SIZE = 1024
cache = LRUCache(3)

def lru_cache(size):
    def lru_cache_decorator(func):
        operation = func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("BEFORE ", func.__name__, size)

            data = deserialize(args[0])

            if operation == 'put':
                key = data['id']
                value = data['payload']
                if cache.get(key) == value:
                    print("PUT: CACHE HIT")
                    response = key
                else:
                    print("PUT: CACHE MISS, HITTING SERVER")
                    response = func(*args, **kwargs)
                cache.put(key, json.dumps(value).encode())
                print("CACHE CONTENTS", cache.map, "LEN ", len(cache.map))

            elif operation == 'get':
                key = data['id']
                value = cache.get(key)
                if value:
                    print("GET: CACHE HIT")
                    response = value
                else:
                    print("GET: CACHE MISS, HITTING SERVER")
                    response = func(*args, **kwargs)
                    print("GET RESPONSE ", response)
                    cache.put(key, response)

            elif operation == 'delete':
                key = data['id']
                response = func(*args, **kwargs)
                cache.delete(key)

            print("AFTER", func.__name__, size)
            return response
        return wrapper
    return lru_cache_decorator

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

@lru_cache(3)
def put(data_bytes, node):
    return str(node.send(data_bytes).decode())

@lru_cache(3)
def get(data_bytes, node):
    return node.send(data_bytes)

@lru_cache(3)
def delete(data_bytes, node):
    return node.send(data_bytes)

def process(udp_clients):
    client_ring = NodeRing(udp_clients)
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        # response = client_ring.get_node(key).send(data_bytes)
        response = put(data_bytes, client_ring.get_node(key))
        print(response)
        hash_codes.add(response)


    # print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(cache.map)}")
    
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        # response = client_ring.get_node(key).send(data_bytes)
        response = get(data_bytes, client_ring.get_node(key))
        print(response)

    # DELETE all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_DELETE(hc)
        # response = client_ring.get_node(key).send(data_bytes)
        response = delete(data_bytes, client_ring.get_node(key))
        print(response)


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)
