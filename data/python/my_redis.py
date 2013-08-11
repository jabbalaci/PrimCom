>>> import redis
>>> r = redis.Redis()    # default: localhost, port 6379
>>> r.set("name", "jabba")
True
>>> r.get("name")
'jabba'

# the list is called "test"
# rpush: right push, i.e. put an element on its right side (tail)
>>> r.rpush("test", 24)
1L
>>> r.rpush("test", 67)
2L
>>> r.rpush("test", 9)
3L
# list all the elements (-1 is the index of the last element)
>>> r.lrange("test", 0, -1)
['24', '67', '9']
# number of elements
>>> r.llen("test")
3
# delete the list if you don't need it anymore
>>> r.delete("test")
1

# link: https://ubuntuincident.wordpress.com/2013/08/12/redis/
