import json
import sys
import socket

from bloom_filter import BloomFilter
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE, deserialize, serialize
from node_ring import NodeRing
from lru_cache import lru_cache

BUFFER_SIZE = 1024

bloomfilter = BloomFilter(len(USERS), 0.05)


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

# @lru_cache(3)
def put(data_bytes, node):
    response = str(node.send(data_bytes).decode())
    bloomfilter.add(deserialize(data_bytes)["id"])
    print("BLOOMFILTER: member added")
    return response

@lru_cache(3)
def get(key, data_bytes, node):
    if bloomfilter.is_member(deserialize(data_bytes)["id"]):
        print("BLOOMFILTER: is member")
        return node.send(data_bytes)
    print("BLOOMFILTER: is not a member")
    return 'Key does not exist'

# @lru_cache(3)
def delete(data_bytes, node):
    if bloomfilter.is_member(deserialize(data_bytes)["id"]):
        print("BLOOMFILTER: is member")
        return node.send(data_bytes)
    print("BLOOMFILTER: is not a member")
    return 'Key does not exist'

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


    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        # response = client_ring.get_node(key).send(data_bytes)
        response = get(key, data_bytes, client_ring.get_node(key))
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
