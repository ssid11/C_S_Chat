import argparse
import sys
from chat_warehous.client import Client

parser = argparse.ArgumentParser()
parser.add_argument('-a','--address',dest='a', default='127.0.0.1')
parser.add_argument('-p', '--port', dest='p', default=7777, type=int)
args = parser.parse_args()
if not args.p in range(1025,65556):
    print('Значение порта для подключения должно быть между 1024 и 65555')
    sys.exit(1)

client = Client(address=args.a, port=args.p)
client.Greetings()
