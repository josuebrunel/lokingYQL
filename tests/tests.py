from __future__ import absolute_import

import os, logging, time, json
import pdb
import unittest
from xml.dom import minidom
from xml.etree import cElementTree as xtree

from myql import MYQL
from myql.utils import pretty_xml, pretty_json
from myql.contrib.auth import YOAuth

from myql.contrib.table import Table
from myql.contrib.table import Base, BaseInput
from myql.contrib.table import Binder, BinderFunction, InputKey, InputValue, PagingPage, PagingUrl, PagingOffset

from myql.contrib.stockscraper import StockRetriever

import readline, rlcompleter
readline.parse_and_bind('tab: complete')

logging.basicConfig(level=logging.DEBUG,format="[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s \n")
logging.getLogger('Test-mYQL')


def json_write_data(json_data, filename):
    with open(filename, 'w') as fp:
        json.dump(json_data, fp, indent=4, sort_keys=True, ensure_ascii=False)
        return True
    return False

def json_get_data(filename):
    with open(filename, 'r') as fp:
        json_data = json.load(fp)
    return json_data


class TestMYQL(unittest.TestCase):
    
    def setUp(self,):
        self.yql = MYQL(format='json',community=True)
        self.insert_result = None

    def tearDown(self):
        pass

    def test_use(self):
        self.yql.use('http://www.josuebrunel.org/users.xml',name='users')
        response = self.yql.rawQuery('select * from users')
        self.yql.yql_table_url = None
        try:
            logging.debug(pretty_json(response.content))
        except (Exception,) as e:
            logging.error(e)
        self.assertEqual(response.status_code,200)

    def test_raw_query(self,):
        response = self.yql.rawQuery('select name, woeid from geo.states where place="Congo"')
        try:
            logging.debug(pretty_json(response.content))
        except (Exception,) as e:
            logging.error(e)
        self.assertEqual(response.status_code,200)

    def test_get(self,):
        self.yql.format = 'xml'
        response = self.yql.get('geo.countries', ['name', 'woeid'], 1)
        self.yql.format = 'json'
        try:
            logging.debug(pretty_xml(response.content))
        except (Exception,) as e:
            logging.error(e)
        self.assertEqual(response.status_code,200)

    def test_select(self,):
        response = self.yql.select('geo.countries', ['name', 'code', 'woeid']).where(['name', '=', 'Canada'])
        try:
            logging.debug(pretty_json(response.content))
        except (Exception,) as e:
            logging.error(e)
        self.assertEqual(response.status_code,200)

    def test_select_in(self,):
        response = self.yql.select('yahoo.finance.quotes').where(['symbol','in',("YHOO","AAPL","GOOG")])
        try:
            logging.debug(pretty_json(response.content))
        except (Exception,) as e:
            logging.error(e)
        self.assertEqual(response.status_code,200)

    def test_1_insert(self,):
        response = self.yql.insert('yql.storage.admin',('value',),('http://josuebrunel.org',))
        try:
            logging.debug(pretty_json(response.content))
            data = response.json()['query']['results']['inserted']
            logging.debug(data)
            json_write_data(data,'yql_storage.json')
        except (Exception,) as e:
            logging.error(response.content)
            logging.error(e)
 
        self.assertEqual(response.status_code,200)

    def test_2_check_insert(self,):
        json_data = json_get_data('yql_storage.json')
        response = self.yql.select('yql.storage').where(['name','=',json_data['select']])
        try:
            logging.debug(pretty_json(response.content))
        except (Exception,) as e:
            logging.error(response.content)
            logging.error(e)

        self.assertEqual(response.status_code,200)
       
    def test_3_update(self,):
        json_data = json_get_data('yql_storage.json')
        response = self.yql.update('yql.storage',('value',),('https://josuebrunel.org',)).where(['name','=',json_data['update']])
        try:
            logging.debug(pretty_json(response.content))
        except (Exception,) as e:
            logging.error(response.content)
            logging.error(e)
 
        self.assertEqual(response.status_code,200)

    def test_4_delete(self,):
        json_data = json_get_data('yql_storage.json')
        response = self.yql.delete('yql.storage').where(['name','=',json_data['update']])
        try:
            logging.debug(pretty_json(response.content))
        except (Exception,) as e:
            logging.error(response.content)
            logging.error(e)
 
        self.assertEqual(response.status_code,200)


       
class TestOAuth(unittest.TestCase):

    def setUp(self,):
        pass

    def tearUp(self,):
        pass

    def test_get_guid(self,):
        oauth = YOAuth(None, None, from_file='credentials.json')
        yql = MYQL(format='json', oauth=oauth)
        response = yql.getGUID('josue_brunel')
        logging.debug(response.content)
        self.assertEqual(response.status_code,200)

    def test_yahoo_fantasy_sport(self,):
        oauth = YOAuth(None, None, from_file='credentials.json')
        yql = MYQL(format='json', oauth=oauth)
        teams = ('mlb.l.1328.t.1','mlb.l.1328.t.2')
        year = '2015-05-05'
        for team in teams:
            response = yql.select('fantasysports.teams.roster').where(['team_key','=',team],['date','=',year])
            self.assertEqual(response.status_code,200)
            if not response.status_code == 200:
                return False

            data = response.json()
            current_team = data['query']['results']['team']
            print(current_team['team_id'],current_team['name'],current_team['number_of_trades'],current_team['number_of_moves'])


class TestStockScraper(unittest.TestCase):

    def setUp(self,):
        self.stock = StockRetriever(format='json')

    def tearDown(self):
        pass

    def test_get_current_info(self,):
        data = self.stock.get_current_info(["YHOO","AAPL","GOOG"])
        logging.debug(pretty_json(data.content))
        self.assertEqual(data.status_code,200)

    def test_get_news_feed(self,):
        data = self.stock.get_news_feed('YHOO')
        logging.debug(pretty_json(data.content))
        self.assertEqual(data.status_code,200)

    def test_get_historical_info_with_args(self,):
        data = self.stock.get_historical_info('YHOO',items=['Open','Close','High','Low'], limit=5,startDate='2014-09-11',endDate='2015-02-10')
        logging.debug(pretty_json(data.content))
        self.assertEqual(data.status_code,200) 

    def test_get_historical_info_without_args(self,):
        data = self.stock.get_historical_info('YHOO')
        logging.debug(pretty_json(data.content))
        self.assertEqual(data.status_code,200)

    def test_get_options_info(self,):
        data = self.stock.get_options_info('YHOO')
        logging.debug(pretty_json(data.content))
        self.assertEqual(data.status_code,200)   

    def test_get_index_summary(self,):
        data = self.stock.get_index_summary('GOOG',('Volume','Change'))
        logging.debug(pretty_json(data.content))
        self.assertEqual(data.status_code,200)   

    def test_get_industry_index(self,):
        data = self.stock.get_industry_index(112)
        logging.debug(pretty_json(data.content))
        self.assertEqual(data.status_code,200)   


class TestTable(unittest.TestCase):

    def setUp(self,):
        self.table_desc = {
            'name': 'mytest',
            'author': 'josuebrunel',
            'apiKeyURL': 'http://josuebrunel.org/api',
            'documentationURL': 'http://josuebrunel.org/doc.html',
            'sampleQuery': ['SELECT * FROM mytable', 'SELECT name FROM mytable WHERE id="345"','DELETE FROM mytable WHERE id="345"'],
        }

        self.table = Table(**self.table_desc)

        self.binder_desc = {
            'name': 'select',
            'itemPath': 'products.product',
            'produces': 'xml'
        }

        self.binder = Binder(**self.binder_desc)
        self.binder_insert = Binder('insert','products.product','json')

        self.key_desc = {
            'id': 'artist',
            'type': 'xs:string',
            'paramType': 'path'
        }

        self.key = InputKey(**self.key_desc)
        self.key2 = InputKey(id='song', type='xs:string', paramType='path', required='true')

        start= {'id': 'ItemPage', 'default': '1'}
        pageSize= {'id':'Count' ,'max':'25'}
        total= {'default': '10'}
        self.paging = PagingPage(start, pageSize, total)

    def xml_pretty_print(self, data):
        """Pretty logging.debug xml data
        """
        raw_string = xtree.tostring(data, 'utf-8')
        parsed_string = minidom.parseString(raw_string)
        return parsed_string.toprettyxml(indent='\t')

    def test_add_binder(self,):
        self.assertEqual(self.table.addBinder(self.binder),True)
        logging.debug(self.xml_pretty_print(self.table.etree))

    def test_remove_binder(self,):
        self.binder.addInput(self.key)
        self.binder_insert.addInput(self.key)
        self.binder.addFunction('', from_file='tests_data/jscode.js')
        self.binder_insert.addFunction("console.log('hello this is an insert function'); ")
        self.table.addBinder(self.binder)
        self.table.addBinder(self.binder_insert)
        self.table.save(name='before', path='tests_data')
        self.assertEqual(os.path.isfile('tests_data/before.xml'),True)
        self.table.removeBinder('select')
        self.table.save(name='after', path='tests_data')
        self.assertEqual(os.path.isfile('tests_data/after.xml'),True)

    def test_add_input_to_binder(self,):
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addInput(self.key),True)
        logging.debug(self.xml_pretty_print(self.binder.etree))

    def test_remove_input(self,):
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addInput(self.key),True)
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addInput(self.key2),True)
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.removeInput(key_id='artist'),True)
        logging.debug(self.xml_pretty_print(self.binder.etree))

    def test_add_function_from_file(self,):
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addFunction('', from_file='tests_data/jscode.js'),True)
        logging.debug(self.xml_pretty_print(self.binder.etree))

    def test_remove_function(self,):
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addFunction('', from_file='tests_data/jscode.js'),True)
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.removeFunction(), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))

    def test_add_paging(self,):
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addPaging(self.paging), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))

    def test_create_binder_with_paging(self,):
        start= {'id': 'ItemPage', 'default': '1'}
        pageSize= {'id':'Count' ,'max':'25'}
        total= {'default': '10'}
        paging = PagingPage(start, pageSize, total)
        logging.debug(self.xml_pretty_print(paging.etree))
        self.binder_desc['paging']=paging
        logging.debug(self.binder_desc)
        binder = Binder(**self.binder_desc)
        self.assertNotEqual(binder.paging,None)
        logging.debug(self.xml_pretty_print(binder.etree))

    def test_create_binder_with_offset_paging(self,):
        start= {'id': 'ItemPage', 'default': '1'}
        pageSize= {'id':'Count' ,'max':'25'}
        total= {'default': '10'}
        paging = PagingOffset(True,  start, pageSize, total)
        logging.debug(self.xml_pretty_print(paging.etree))
        self.binder_desc['paging']=paging
        logging.debug(self.binder_desc)
        binder = Binder(**self.binder_desc)
        self.assertNotEqual(binder.paging,None)
        logging.debug(self.xml_pretty_print(binder.etree))


    def test_create_binder_with_url_paging(self,):
        nextpage = {'path': 'ysearchresponse.nextpage'}
        paging = PagingUrl(nextpage)
        logging.debug(self.xml_pretty_print(paging.etree))
        self.binder_desc['paging']=paging
        logging.debug(self.binder_desc)
        binder = Binder(**self.binder_desc)
        self.assertNotEqual(binder.paging,None)
        logging.debug(self.xml_pretty_print(binder.etree))


    def test_remove_paging(self,):
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addPaging(self.paging), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.removePaging(), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))

    def test_create_binder_with_urls(self,):
        url = 'http://josuebrunel.org/service/v1'
        url2 = 'http://josuebrunel.org/service/v1/?name=lol'
        self.binder_desc['urls'] = [url, url2]
        binder = Binder(**self.binder_desc)
        logging.debug(self.xml_pretty_print(binder.etree))
        self.assertEqual(self.binder.addUrl(url), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))


    def test_add_url(self,):
        url = 'http://josuebrunel.org/service.js'
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addUrl(url), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))

    def test_remove_url(self,):
        url = 'http://josuebrunel.org/service.js'
        url2 = 'http://google.com'
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addUrl(url), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.addUrl(url2), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))
        self.assertEqual(self.binder.removeUrl(url), True)
        logging.debug(self.xml_pretty_print(self.binder.etree))

    def test_save_file(self,):
        self.table.save()
        self.assertEqual(os.path.isfile('mytest.xml'),True) 

    def test_save_with_another_name(self):
        name = "tests_data/toto"
        self.table.save(name)
        self.assertEqual(os.path.isfile(name+'.xml'),True)

    def test_save_to_different_location(self,):
        fname = "titi"
        path = 'tests_data'
        name = os.path.join(path,fname)
        self.table.save(name=fname, path=path)
        self.assertEqual(os.path.isfile(name+'.xml'),True)

    def test_create_table(self,):
        self.binder.addInput(self.key)
        self.binder.addFunction('', from_file='tests_data/jscode.js')
        logging.debug(self.xml_pretty_print(self.table.etree))
        self.table.addBinder(self.binder)
        self.table.save(name='mytable', path='tests_data')
        self.assertEqual(os.path.isfile('tests_data/mytable.xml'),True)
        logging.debug(self.xml_pretty_print(self.table.etree))

    def test_create_table_and_add_two_binders(self,):
        self.binder.addInput(self.key)
        self.binder_insert.addInput(self.key)
        self.binder.addFunction('', from_file='tests_data/jscode.js')
        self.binder_insert.addFunction("console.log('hello this is an insert function'); ")
        logging.debug(self.xml_pretty_print(self.table.etree))
        self.table.addBinder(self.binder)
        logging.debug(self.xml_pretty_print(self.table.etree))
        self.table.addBinder(self.binder_insert)
        self.table.save(name='mytable', path='tests_data')
        self.assertEqual(os.path.isfile('tests_data/mytable.xml'),True)
        logging.debug(self.xml_pretty_print(self.table.etree))

    def test_create_table_with_binder(self,):
        self.binder.addInput(self.key)
        self.binder.addFunction('', from_file='tests_data/jscode.js')
        self.table_desc['bindings'] = [self.binder]
        table = Table(**self.table_desc)
        logging.debug(self.xml_pretty_print(table.etree))
        table.save(name='mytable', path='tests_data')
        self.assertEqual(os.path.isfile('tests_data/mytable.xml'),True)
        logging.debug(self.xml_pretty_print(table.etree))

    def test_create_table_with_two_binders(self,):
        self.binder.addInput(self.key)
        self.binder.addFunction('', from_file='tests_data/jscode.js')
        self.table_desc['bindings'] = [self.binder, self.binder_insert]
        table = Table(**self.table_desc)
        logging.debug(self.xml_pretty_print(table.etree))
        table.save(name='mytable', path='tests_data')
        self.assertEqual(os.path.isfile('tests_data/mytable.xml'),True)
        logging.debug(self.xml_pretty_print(table.etree))

    def test_add_function_table(self):
        logging.debug(self.xml_pretty_print(self.table.etree))
        bf = BinderFunction('concat', inputs=[self.key, self.key2])
        bf.addFunction('', from_file='tests_data/jscode.js')
        self.table.addBinder(bf)
        #self.assertEqual(self.table.addFunction('', from_file='tests_data/jscode.js'),True)
        logging.debug(self.xml_pretty_print(self.table.etree))

    def test_create_function_with_func_code(self):
        logging.debug(self.xml_pretty_print(self.table.etree))
        bf = BinderFunction('concat', func_code='console.log("hello moron !!!")')
        logging.debug(self.xml_pretty_print(bf.etree))

    def test_create_function_with_func_file(self):
        logging.debug(self.xml_pretty_print(self.table.etree))
        bf = BinderFunction('concat', func_file='tests_data/jscode.js')
        logging.debug(self.xml_pretty_print(bf.etree))


    def test_remove_function_table(self,):
        logging.debug(self.xml_pretty_print(self.table.etree))
        self.assertEqual(self.table.addFunction('', from_file='tests_data/jscode.js'),True)
        logging.debug(self.xml_pretty_print(self.table.etree))
        self.assertEqual(self.table.removeFunction(),True)
        logging.debug(self.xml_pretty_print(self.table.etree))

    def test_baseinput_to_xml(self,):
        i = BaseInput('key','name','xs:string', 'path', required=True, default='josh', private=True, maxBatchItems=10)
        logging.debug(self.xml_pretty_print(i.etree))

    def test_inputvalue(self,):
        v = InputValue('content', 'xs:string', 'variable', required=True)
        logging.debug(self.xml_pretty_print(v.etree))
    
    def tearUp(self):
        os.path.unlink('tests_data/mytest.xml')
        os.path.unlink('tests_data/toto.xml')
        
if '__main__' == __name__:
    unittest.main()

