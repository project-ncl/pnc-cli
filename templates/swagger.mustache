#!/usr/bin/env python
"""Swagger generic API client. This client handles the client-
server communication, and is invariant across implementations. Specifics of
the methods and models for each application are generated from the Swagger
templates."""

import sys
import os
import re
import json
import datetime
import mimetypes
import random
import string
import requests

class ApiClient(object):
    """Generic API client for Swagger client library builds

    Attributes:
      host: The base path for the server to call
      headerName: a header to pass when making calls to the API
      headerValue: a header value to pass when making calls to the API
    """

    def __init__(self, host=None, headerName=None, headerValue=None):
        self.defaultHeaders = {}
        if (headerName is not None):
            self.defaultHeaders[headerName] = headerValue
        self.host = host
        self.cookie = None
        self.boundary = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
        # Set default User-Agent.
        self.user_agent = 'Python-Swagger'

    @property
    def user_agent(self):
        return self.defaultHeaders['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        self.defaultHeaders['User-Agent'] = value

    def setDefaultHeader(self, headerName, headerValue):
        self.defaultHeaders[headerName] = headerValue

    def callAPI(self, resourcePath, method, queryParams, postData,
                headerParams=None, files=None):

        url = self.host + resourcePath

        mergedHeaderParams = self.defaultHeaders.copy()
        if headerParams: mergedHeaderParams.update(headerParams)
        headers = {}
        if mergedHeaderParams:
            for param, value in mergedHeaderParams.iteritems():
                headers[param] = ApiClient.sanitizeForSerialization(value)

        if self.cookie:
            headers['Cookie'] = ApiClient.sanitizeForSerialization(self.cookie)

        data = self.convertPostData(headers, postData, files)
        result = None

        if method in ['GET']:
            # Options to add statements later on and for compatibility
            result = requests.get(url, params=queryParams, headers=headers)
        elif method in ['POST']:
            result = requests.post(url, params=queryParams, headers=headers, data=data)
        elif method in ['PUT']:
            result = requests.put(url, params=queryParams, headers=headers, data=data)
        elif method in ['DELETE']:
            result = requests.delete(url, params=queryParams, headers=headers, data=data)
        else:
            raise Exception('Method ' + method + ' is not recognized.')

        if 'Set-Cookie' in result.headers:
            self.cookie = result.headers['Set-Cookie']

        return result

    def toPathValue(self, obj):
        """Convert a string or object to a path-friendly value
        Args:
            obj -- object or string value
        Returns:
            string -- quoted value
        """
        if type(obj) == list:
            return ','.join(obj)
        else:
            return str(obj)

    def convertPostData(self, headers, postData, files):
        data = None
        if postData:
            postData = ApiClient.sanitizeForSerialization(postData)
            if 'Content-Type' not in headers or headers['Content-Type'] == 'application/json':
                headers['Content-Type'] = 'application/json'
                data = json.dumps(postData)
            elif headers['Content-Type'] == 'multipart/form-data':
                data = ApiClient.buildMultipartFormData(postData, files)
                headers['Content-Type'] = 'multipart/form-data; boundary={0}'.format(self.boundary)
                headers['Content-length'] = str(len(data))
        return data


    @staticmethod
    def sanitizeForSerialization(obj):
        """
        Sanitize an object for Request.

        If obj is None, return None.
        If obj is str, int, long, float, bool, return directly.
        If obj is datetime.datetime, datetime.date convert to string in iso8601 format.
        If obj is list, santize each element in the list.
        If obj is dict, return the dict.
        If obj is swagger model, return the properties dict.
        """
        if isinstance(obj, type(None)):
            return None
        elif isinstance(obj, (str, int, long, float, bool, file)):
            return obj
        elif isinstance(obj, list):
            return [ApiClient.sanitizeForSerialization(subObj) for subObj in obj]
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        else:
            if isinstance(obj, dict):
                objDict = obj
            else:
                # Convert model obj to dict except attributes `swaggerTypes`, `attributeMap`
                # and attributes which value is not None.
                # Convert attribute name to json key in model definition for request.
                objDict = {obj.attributeMap[key]: val
                           for key, val in obj.__dict__.iteritems()
                           if key != 'swaggerTypes' and key != 'attributeMap' and val is not None}
            return {key: ApiClient.sanitizeForSerialization(val)
                    for (key, val) in objDict.iteritems()}

    @staticmethod
    def buildMultipartFormData(self, postData, files):
        def escape_quotes(s):
            return s.replace('"', '\\"')

        lines = []

        for name, value in postData.items():
            lines.extend((
                '--{0}'.format(self.boundary),
                'Content-Disposition: form-data; name="{0}"'.format(escape_quotes(name)),
                '',
                str(value),
            ))

        for name, filepath in files.items():
            f = open(filepath, 'r')
            filename = filepath.split('/')[-1]
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            lines.extend((
                '--{0}'.format(self.boundary),
                'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(escape_quotes(name),
                                                                                    escape_quotes(filename)),
                'Content-Type: {0}'.format(mimetype),
                '',
                f.read()
            ))

        lines.extend((
            '--{0}--'.format(self.boundary),
            ''
        ))
        return '\r\n'.join(lines)

    def deserialize(self, obj, objClass):
        """Derialize a JSON string into an object.

        Args:
            obj -- string or object to be deserialized
            objClass -- class literal for deserialzied object, or string
                of class name
        Returns:
            object -- deserialized object"""

        # Have to accept objClass as string or actual type. Type could be a
        # native Python type, or one of the model classes.
        if type(objClass) == str:
            if 'list[' in objClass:
                match = re.match('list\[(.*)\]', objClass)
                subClass = match.group(1)
                return [self.deserialize(subObj, subClass) for subObj in obj]

            if (objClass in ['int', 'float', 'long', 'dict', 'list', 'str', 'bool', 'datetime']):
                objClass = eval(objClass)
            else:  # not a native type, must be model class
                objClass = eval(objClass + '.' + objClass)

        if objClass in [int, long, float, dict, list, str, bool]:
            return objClass(obj)
        elif objClass == datetime:
            return self.__parse_string_to_datetime(obj)

        instance = objClass()

        for attr, attrType in instance.swaggerTypes.iteritems():
            if obj is not None and instance.attributeMap[attr] in obj and type(obj) in [list, dict]:
                value = obj[instance.attributeMap[attr]]
                if attrType in ['str', 'int', 'long', 'float', 'bool']:
                    attrType = eval(attrType)
                    try:
                        value = attrType(value)
                    except UnicodeEncodeError:
                        value = unicode(value)
                    except TypeError:
                        value = value
                    setattr(instance, attr, value)
                elif (attrType == 'datetime'):
                    setattr(instance, attr, self.__parse_string_to_datetime(value))
                elif 'list[' in attrType:
                    match = re.match('list\[(.*)\]', attrType)
                    subClass = match.group(1)
                    subValues = []
                    if not value:
                        setattr(instance, attr, None)
                    else:
                        for subValue in value:
                            subValues.append(self.deserialize(subValue, subClass))
                    setattr(instance, attr, subValues)
                else:
                    setattr(instance, attr, self.deserialize(value, attrType))

        return instance

    def __parse_string_to_datetime(self, string):
        """
        Parse datetime in string to datetime.

        The string should be in iso8601 datetime format.
        """
        try:
            from dateutil.parser import parse

            return parse(string)
        except ImportError:
            return string