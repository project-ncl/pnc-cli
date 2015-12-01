#!/bin/sh
coverage run runtests.py --junitxml results.xml -vv
coverage report -m --omit=test/*,*swagger_client/models/*,runtests*,/usr/*,*test_api*

