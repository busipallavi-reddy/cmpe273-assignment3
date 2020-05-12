import functools
import time


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class LRUCache():
    def __init__(self, capacity=3):
        self.capacity = capacity
        self.map = {}
        self.head = Node(-1, -1)  # dummy head node
        self.tail = Node(-1, -1)  # dummy tail node
        self.head.next = self.tail  # head being oldest
        self.tail.prev = self.head  # tail being most recent

    def move_recent(self, node):
        prev = node.prev
        prev.next = node.next
        node.next.prev = prev
        last = self.tail.prev
        last.next = node
        node.prev = last
        node.next = self.tail
        self.tail.prev = node

    def add_node(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def remove(self):
        node = self.head.next
        node.next.prev = self.head
        self.head.next = node.next
        del self.map[node.key]

    def put(self, key, val):
        node = self.map.get(key)
        if not node:
            newNode = Node(key, val)
            self.map[key] = newNode
            self.add_node(newNode)
            if len(self.map) > self.capacity:
                self.remove()
        else:
            node.val = val
            self.move_recent(node)

    def get(self, key):
        node = self.map.get(key)
        if not node:
            return None
        # move this node to recently seen towards tail
        self.move_recent(node)
        return node.val

    def delete(self, key):
        node = self.map.get(key)
        if not node:
            return
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev
        del node

def lru_cache(size):
    def lru_cache_decorator(func):
        cache = LRUCache(size)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            operation = func.__name__
            # print("BEFORE ", func.__name__, size)
            args_list = []
            if args:
                args_list.append(', '.join(repr(arg) for arg in args))
            args_str = ', '.join(args_list)
            key = args[0]
            value = cache.get(key)
            if value:
                print('[cache-hit] %s(%s) -> %r ' % (operation, args_str, value))
                # print("GET: CACHE HIT")
                response = value
            else:
                start_time = time.time()
                # print("GET: CACHE MISS, HITTING SERVER")
                response = func(*args, **kwargs)
                end_time = time.time() - start_time
                print('[%0.8fs] %s(%s) -> %r ' % (end_time, operation, args_str, response))
                # print("GET RESPONSE ", response)
                cache.put(key, response)

            # print("AFTER", func.__name__, size)
            return response
        return wrapper
    return lru_cache_decorator