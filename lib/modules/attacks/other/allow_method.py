import re

from lib.utils.container import Services
from .. import AttackPlugin


class AllowMethod(AttackPlugin):
    def process(self, start_url, crawled_urls):
        output = Services.get('output')
        request = Services.get('request_factory')
        datastore = Services.get('datastore')

        output.info('Checking http allow methods..')
        db = datastore.open('allowmethod.txt', 'r')
        dbfiles = [x.split('\n') for x in db]
        try:
            for method in dbfiles:
                resp = request.send(url=start_url, method=str(method[0]), payload=None, headers=None)
                if re.search(r'allow|public', str(resp.headers.keys()), re.I):
                    allow = resp.headers['allow']
                    if allow is None:
                        allow = resp.headers['public']
                    if allow is not None and allow != '':
                        output.finding('HTTP Allow Method: %s' % allow)
                        break
        except Exception as e:
            print(e)
