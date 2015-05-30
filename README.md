mYQL
=========

[![Build Status](https://travis-ci.org/josuebrunel/myql.svg?branch=master)](https://travis-ci.org/josuebrunel/myql) [![Documentation Status](https://readthedocs.org/projects/myql/badge/?version=latest)](https://myql.readthedocs.org)
[![Latest Version](https://pypip.in/version/myql/badge.svg)](https://pypi.python.org/pypi/myql/)
[![Downloads](https://pypip.in/download/myql/badge.svg)](https://pypi.python.org/pypi/myql) 
[![Py_Versions](https://pypip.in/py_versions/myql/badge.svg)](https://pypi.python.org/pypi/myql)
[![Implementations](https://pypip.in/implementation/myql/badge.svg)](https://pypi.python.org/pypi/myql)
[![Join the chat at https://gitter.im/josuebrunel/myql](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/josuebrunel/myql?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Code Issues](https://www.quantifiedcode.com/project/gh:josuebrunel:myql/badge.svg)](https://www.quantifiedcode.com/app/project/gh:josuebrunel:myql)


mYQL is a Python wrapper of the Yahoo Query Language. Full documentation [here](http://myql.readthedocs.org/en/latest/)

Yahoo! Query Language Documentation and Support
===============================================

* Yahoo! Query Language - http://developer.yahoo.com/yql/
* Yahoo! Developer Network: http://developer.yahoo.com
* Yahoo! Application Platform - http://developer.yahoo.com/yap/
* Yahoo! Social APIs - http://developer.yahoo.com/social/
* Yahoo! QUery Language Console https://developer.yahoo.com/yql/console/

### Features

* Simple YQL Query 
* Authenticated YQL Query ( OAuth )
* StockScraper
* YQL Open Table (Classes and Metaclasses) Generator 
* Response prettyfier

### Installation

```shell
$ pip install myql
```

### Documentation

Full Documentation is [here](http://myql.readthedocs.org/en/latest/)

### Contribute

* Report issue
* Star and Fork the repository
* Submit pull requests
* Above all, have fun playing with data :wink:

#### Release Notes

##### 1.2.2 ( in development )
-------
* **Python3** support OK [#71](https://github.com/josuebrunel/myql/issues/71)
* **PyPy/PyPy3** support OK
* Fixed issue with **IN** condition in **where** clause
* Fixed issue when passing an empty list/tuple (**[]/()**) in a **where** clause besides first argument
* Import of ***[StockParser](https://github.com/gurch101/StockScraper)*** from Gurchet Rai  OK [#68](https://github.com/josuebrunel/myql/issues/68)
* Insert, Update, Delete methods added [#67](https://github.com/josuebrunel/myql/issues/67) 
* Dummy *try/except* removed from main module
* Fixed **Invalid OAuth Signature** when using a refreshed token [#64](https://github.com/josuebrunel/myql/issues/64)
* Fixed misused of ***MYQL.use(...)*** [#76](https://github.com/josuebrunel/myql/issues/76)
* Fixed format issue [#82](https://github.com/josuebrunel/myql/issues/82)
* Added useful functions in utils [#81](https://github.com/josuebrunel/myql/issues/81)
* Default access to community tables
* Response prettyfier : *pretty_json, pretty_xml*

##### v 1.2.1
------
* Multiple requests while using OAuth fixed 

##### 1.2.0
-------
* OpenTable classes
* Access to resources requiring authentication

##### 0.5.6
-------------
* fetch data
* access to community data
* select data format (xml/json)
* change data source
* filter data 
* fix handling of default response format on the fly 
* fix limit on ***select(...).where(...)*** when no limit value is passed
* fix limit on ***get(...)***



