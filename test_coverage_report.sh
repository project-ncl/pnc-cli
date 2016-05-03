#!/bin/sh
coverage run runtests.py -vv
coverage report -m --omit=test/*,*swagger_client/models/*,runtests*,/usr/*,*test_api*,*swagger_client/configuration.py,*swagger_client/rest.py,*__init__.py*,pnc_cli/utils.py,*api_client.py*
