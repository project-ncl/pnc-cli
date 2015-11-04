#!/bin/sh
coverage run runtests.py -vv
coverage report -m --omit=test/*,*swagger_client/models/*,runtests*,/usr/*,*test_api*

