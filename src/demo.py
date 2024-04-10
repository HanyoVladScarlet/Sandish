from redis import Redis
import time
import json


def main():
    ''''''
    r = Redis(host='localhost', port=6379, decode_responses=True, password=114514)
    for i in range(20):
        text = json.dumps({
            'timestamp': time.time(),
            'message': f'info{i}',
            'level': 3
        })
        r.zadd('test1', {text: time.time()})
    print(r.zrange('test1', 0, -1, withscores=True))


if __name__ == '__main__':
    main()