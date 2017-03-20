#!/bin/sh
py.test "$@" test/integration --junitxml results.xml
