# cmpe273-assignment3



## 1. DELETE operation

*Request*

```
{ 
    'operation': 'DELETE',
    'id': 'hash_code_of_the_object',
}
```

*Response*

```
{
    'success'
}
```

For this operation, I added a for loop for deletion like PUT and GET for all users in cache_client.py. Also, I added SERIALIZE_DELETE function in pickle_hash.py



## 2. LRU Cache

* Created a class LRUCache in lru_cache.py. Added a decorator function called lru_cache in the same file.
* The LRUCache has 2 dummy nodes, head and tail. Head being the oldest node and tail being the newest node. SO deletion of node is done from head end and addition from tail end.
* Modified the cache_client.py file to have separate get(), put() and delete() functions and invoked them from the loops for put, get and delete in process().
* As per instructions, only get() is decorated by lru_cache decorator (cache of size 3).
* Successful test output is shown below:

*test_lru_cache.py output*

```
pallavi@desktop:~/Desktop/cmpe273/assignments/cmpe273-assignment3$ python3 test_lru_cache.py 
[0.00000048s] fibonacci(0) -> 0 
[0.00000048s] fibonacci(1) -> 1 
[0.00006199s] fibonacci(2) -> 1 
[cache-hit] fibonacci(1) -> 1 
[cache-hit] fibonacci(2) -> 1 
[0.00001788s] fibonacci(3) -> 2 
[0.00010467s] fibonacci(4) -> 3 
[cache-hit] fibonacci(3) -> 2 
[cache-hit] fibonacci(4) -> 3 
[0.00001431s] fibonacci(5) -> 5 
[0.00015974s] fibonacci(6) -> 8 
fibonacci(6)=8

[0.00000191s] get_data(1) -> {'id': 1, 'value': 'Foo Bar - 1'} 
{'id': 1, 'value': 'Foo Bar - 1'}
[0.00000191s] get_data(2) -> {'id': 2, 'value': 'Foo Bar - 2'} 
{'id': 2, 'value': 'Foo Bar - 2'}
[0.00000119s] get_data(3) -> {'id': 3, 'value': 'Foo Bar - 3'} 
{'id': 3, 'value': 'Foo Bar - 3'}
[0.00000072s] get_data(4) -> {'id': 4, 'value': 'Foo Bar - 4'} 
{'id': 4, 'value': 'Foo Bar - 4'}
[cache-hit] get_data(1) -> {'id': 1, 'value': 'Foo Bar - 1'} 
{'id': 1, 'value': 'Foo Bar - 1'}
[cache-hit] get_data(2) -> {'id': 2, 'value': 'Foo Bar - 2'} 
{'id': 2, 'value': 'Foo Bar - 2'}
[cache-hit] get_data(3) -> {'id': 3, 'value': 'Foo Bar - 3'} 
{'id': 3, 'value': 'Foo Bar - 3'}
[cache-hit] get_data(4) -> {'id': 4, 'value': 'Foo Bar - 4'} 
{'id': 4, 'value': 'Foo Bar - 4'}
[0.00000095s] get_data(5) -> {'id': 5, 'value': 'Foo Bar - 5'} 
{'id': 5, 'value': 'Foo Bar - 5'}
[0.00000119s] get_data(6) -> {'id': 6, 'value': 'Foo Bar - 6'} 
{'id': 6, 'value': 'Foo Bar - 6'}
Num of function calls:10
Num of cache misses:6
```



## 3. Bloom Filter

* Created a BloomFilter class in a separate file, bloom_filter.py
* The class takes n (probable number of keys) and p (false positive probability) as parameters.
* I used a simple boolean array as as the bloom_filter array (instead of bit array).
* I used the MD5 hash_code_hex() from pickle_hash.py to hash my keys (instead of mmh3).
* Successful test output is shown below:

```
pallavi@desktop:~/Desktop/cmpe273/assignments/cmpe273-assignment3$ pipenv run python3 test_bloom_filter.py 
'bonny' is probably present!
'bloom' is probably present!
'bolster' is probably present!
'bonus' is probably present!
'blossom' is probably present!
'abundance' is probably present!
'abundant' is probably present!
'abounds' is probably present!
'abound' is probably present!
'twitter' is definitely not present!
'facebook' is definitely not present!
'accessable' is probably present!
```



*Complete Sample output for cache_client.py*

```
pallavi@desktop:~/Desktop/cmpe273/assignments/cmpe273-assignment3$ python3 cache_client.py
Connecting to server at 127.0.0.1:4001
BLOOMFILTER: member added
d0df71363130955e493c24ac0d296a75
Connecting to server at 127.0.0.1:4000
BLOOMFILTER: member added
1c84c3d6dec3775654c4573ca4df1064
Connecting to server at 127.0.0.1:4000
BLOOMFILTER: member added
e52f43cd2c23bb2e6296153748382764
Connecting to server at 127.0.0.1:4003
BLOOMFILTER: member added
9aa0c932fb8eba9a72a6ae60064a0507
Connecting to server at 127.0.0.1:4000
BLOOMFILTER: member added
6aaae4a8f8468ef61e78b4ced80fa140
Connecting to server at 127.0.0.1:4001
BLOOMFILTER: member added
d0df71363130955e493c24ac0d296a75
Number of Users=6
Number of Users Cached=5
9aa0c932fb8eba9a72a6ae60064a0507
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4003
[0.00019574s] get('9aa0c932fb8eba9a72a6ae60064a0507', b'\x80\x03}q\x00(X\t\x00\x00\x00operationq\x01X\x03\x00\x00\x00GETq\x02X\x02\x00\x00\x00idq\x03X \x00\x00\x009aa0c932fb8eba9a72a6ae60064a0507q\x04u.', <__main__.UDPClient object at 0x7f7ff60af828>) -> b'{"name": "Agueda Letsinger", "email": "aletsinger@gmail.com", "age": 23}' 
b'{"name": "Agueda Letsinger", "email": "aletsinger@gmail.com", "age": 23}'
1c84c3d6dec3775654c4573ca4df1064
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4000
[0.00018692s] get('1c84c3d6dec3775654c4573ca4df1064', b'\x80\x03}q\x00(X\t\x00\x00\x00operationq\x01X\x03\x00\x00\x00GETq\x02X\x02\x00\x00\x00idq\x03X \x00\x00\x001c84c3d6dec3775654c4573ca4df1064q\x04u.', <__main__.UDPClient object at 0x7f7ff60af780>) -> b'{"name": "Bari Pushard", "email": "bpushard@gmail.com", "age": 21}' 
b'{"name": "Bari Pushard", "email": "bpushard@gmail.com", "age": 21}'
6aaae4a8f8468ef61e78b4ced80fa140
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4000
[0.00014877s] get('6aaae4a8f8468ef61e78b4ced80fa140', b'\x80\x03}q\x00(X\t\x00\x00\x00operationq\x01X\x03\x00\x00\x00GETq\x02X\x02\x00\x00\x00idq\x03X \x00\x00\x006aaae4a8f8468ef61e78b4ced80fa140q\x04u.', <__main__.UDPClient object at 0x7f7ff60af780>) -> b'{"name": "Lisbeth Stacker", "email": "lstacker@gmail.com", "age": 24}' 
b'{"name": "Lisbeth Stacker", "email": "lstacker@gmail.com", "age": 24}'
d0df71363130955e493c24ac0d296a75
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4001
[0.00015545s] get('d0df71363130955e493c24ac0d296a75', b'\x80\x03}q\x00(X\t\x00\x00\x00operationq\x01X\x03\x00\x00\x00GETq\x02X\x02\x00\x00\x00idq\x03X \x00\x00\x00d0df71363130955e493c24ac0d296a75q\x04u.', <__main__.UDPClient object at 0x7f7ff60af7b8>) -> b'{"name": "John Smith", "email": "jsmith@gmail.com", "age": 20}' 
b'{"name": "John Smith", "email": "jsmith@gmail.com", "age": 20}'
e52f43cd2c23bb2e6296153748382764
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4000
[0.00017428s] get('e52f43cd2c23bb2e6296153748382764', b'\x80\x03}q\x00(X\t\x00\x00\x00operationq\x01X\x03\x00\x00\x00GETq\x02X\x02\x00\x00\x00idq\x03X \x00\x00\x00e52f43cd2c23bb2e6296153748382764q\x04u.', <__main__.UDPClient object at 0x7f7ff60af780>) -> b'{"name": "Irish Rackers", "email": "irackers@gmail.com", "age": 22}' 
b'{"name": "Irish Rackers", "email": "irackers@gmail.com", "age": 22}'
9aa0c932fb8eba9a72a6ae60064a0507
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4003
b'Not supported operation=DELETE'
1c84c3d6dec3775654c4573ca4df1064
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4000
b'Not supported operation=DELETE'
6aaae4a8f8468ef61e78b4ced80fa140
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4000
b'Not supported operation=DELETE'
d0df71363130955e493c24ac0d296a75
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4001
b'Not supported operation=DELETE'
e52f43cd2c23bb2e6296153748382764
BLOOMFILTER: is member
Connecting to server at 127.0.0.1:4000
b'Not supported operation=DELETE'
```

