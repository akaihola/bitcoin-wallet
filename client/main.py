import web, os, re, json, string, urllib
import pprint
import bitcoin
from btcdjson import BitcoindJson
from sqlite3 import dbapi2 as sqlite


if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys
    parser = ArgumentParser(
        'Bitcoin Evolved - '
        'A new kind of Bitcoin client to make Bitcoin easy and enjoyable to use')
    parser.add_argument('-u', '--user', nargs='?', default='',
                        help='username for bitcoind server (default: empty)')
    parser.add_argument('-P', '--password', nargs='?', default='',
                        help='password for bitcoind server (default: empty)')
    parser.add_argument('-s', '--server', dest='host', nargs='?', default='localhost',
                        help='bitcoind server host (default: localhost)')
    parser.add_argument('-p', '--port', nargs='?', type=int, default=8332,
                        help='bitcoind server port (default: 8332)')
    parser.add_argument('wsgi_args', nargs='*')
    args = parser.parse_args()
    sys.argv[1:] = args.wsgi_args
else:
    from argparse import Namespace
    args = Namespace(user='', password='', host='localhost', port=8332)


urls = (
    '/', 'main',
    '/api/(.*)', 'API',
    '/tests', 'testingInterface'
)


if args.user or args.host != 'localhost':
    btcJson = BitcoindJson(**args.__dict__)
else:
    from bitcoin.config import read_default_config
    cfg = read_default_config()
    btcJson = BitcoindJson(
        user=cfg.get('rpcuser', ''),
        password=cfg['rpcpassword'],
        host='localhost',
        port=int(cfg.get('rpcport', '8332')))



db = sqlite.connect('main.db')
dbc = db.cursor()

render = web.template.render('templates/')

class API:
    def GET(self, action = None):
        request = web.input()
        result = btcJson(action, web.input())
        return result
    
    
class testingInterface:
    def GET(self):
        return render.tests()
    
        
class main:
    def GET(self):
        get = web.input(loadPartial=False)
        
        
        if get.loadPartial != False:
            
            content = web.template.frender('templates/partial/' + get.loadPartial + '.html')()
        
        else:
            dashboard = web.template.frender('templates/partial/dashboard.html')()
            content = render.main(unicode(dashboard))

        return content


app = web.application(urls, globals(), True)

if __name__ == "__main__":
    app.run()
