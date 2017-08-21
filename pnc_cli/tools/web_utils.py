# -*- coding: utf-8 -*-

import logging
import os
import urllib2


def download_file(file_url, file_path, artifact):
    try:
        logging.debug("Downloading from %s to '%s'", file_url, file_path)
        handler = urllib2.urlopen(file_url)
    except urllib2.HTTPError, err:
        logging.error("[%s] Failed to download %s. %s", artifact, file_url, err)
        return None
    if handler.getcode() == 200:
        pom = handler.read()
        handler.close()
        file_dir = os.path.split(file_path)[0]
        if file_dir and not os.path.exists(file_dir):
            os.mkdir(file_dir)
        pom_file = None
        try:
            pom_file = open(file_path, "w")
            pom_file.write(pom)
        finally:
            if pom_file:
                pom_file.close()
        return file_path
    else:
        logging.error("[%s] Failed to download %s.", artifact, file_url)
        return None
