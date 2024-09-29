import redis

# Connect to Redis Client
hostname = '#'
portnumber = 13869
password = '#'

r = redis.StrictRedis(host=hostname,
                      port=portnumber,
                      password=password)

# Simulated Logs
with open('simulated_logs.txt', 'r') as f:
    logs_text = f.read()

encoded_logs = logs_text.split('\n')

# Push into Redis database
r.lpush('attendance:logs', *encoded_logs)
