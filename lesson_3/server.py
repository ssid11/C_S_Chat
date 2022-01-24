import argparse
import sys
from chat_warehous import Server

parser = argparse.ArgumentParser()
parser.add_argument('-a',dest='a', default='127.0.0.1')
parser.add_argument('-p', '--port', dest='p', default=7777, type=int)
args = parser.parse_args()
if not args.p in range(1025,65556):
    print('Значение прослушиваемого порта должны быть между 1024 и 65555')
    sys.exit(1)

server = Server(address=args.a, port=args.p)
server.Run()
