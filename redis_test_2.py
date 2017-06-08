import redis
r = redis.StrictRedis(host='192.168.1.157', port=6379, db=0)
s = r.dbsize('renrenche')
print (s.dbsize())