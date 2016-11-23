# coding: utf-8

"""
Copyright 2015 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from datetime import datetime
from pprint import pformat
from six import iteritems


class ProjectRest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ProjectRest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'name': 'str',
            'description': 'str',
            'issue_tracker_url': 'str',
            'project_url': 'str',
            'configuration_ids': 'list[int]',
            'license_id': 'int'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'issue_tracker_url': 'issueTrackerUrl',
            'project_url': 'projectUrl',
            'configuration_ids': 'configurationIds',
            'license_id': 'licenseId'
        }

        self._id = None
        self._name = None
        self._description = None
        self._issue_tracker_url = None
        self._project_url = None
        self._configuration_ids = None
        self._license_id = None

    @property
    def id(self):
        """
        Gets the id of this ProjectRest.


        :return: The id of this ProjectRest.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProjectRest.


        :param id: The id of this ProjectRest.
        :type: int
        """
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ProjectRest.


        :return: The name of this ProjectRest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProjectRest.


        :param name: The name of this ProjectRest.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ProjectRest.


        :return: The description of this ProjectRest.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ProjectRest.


        :param description: The description of this ProjectRest.
        :type: str
        """
        self._description = description

    @property
    def issue_tracker_url(self):
        """
        Gets the issue_tracker_url of this ProjectRest.


        :return: The issue_tracker_url of this ProjectRest.
        :rtype: str
        """
        return self._issue_tracker_url

    @issue_tracker_url.setter
    def issue_tracker_url(self, issue_tracker_url):
        """
        Sets the issue_tracker_url of this ProjectRest.


        :param issue_tracker_url: The issue_tracker_url of this ProjectRest.
        :type: str
        """
        self._issue_tracker_url = issue_tracker_url

    @property
    def project_url(self):
        """
        Gets the project_url of this ProjectRest.


        :return: The project_url of this ProjectRest.
        :rtype: str
        """
        return self._project_url

    @project_url.setter
    def project_url(self, project_url):
        """
        Sets the project_url of this ProjectRest.


        :param project_url: The project_url of this ProjectRest.
        :type: str
        """
        self._project_url = project_url

    @property
    def configuration_ids(self):
        """
        Gets the configuration_ids of this ProjectRest.


        :return: The configuration_ids of this ProjectRest.
        :rtype: list[int]
        """
        return self._configuration_ids

    @configuration_ids.setter
    def configuration_ids(self, configuration_ids):
        """
        Sets the configuration_ids of this ProjectRest.


        :param configuration_ids: The configuration_ids of this ProjectRest.
        :type: list[int]
        """
        self._configuration_ids = configuration_ids

    @property
    def license_id(self):
        """
        Gets the license_id of this ProjectRest.


        :return: The license_id of this ProjectRest.
        :rtype: int
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """
        Sets the license_id of this ProjectRest.


        :param license_id: The license_id of this ProjectRest.
        :type: int
        """
        self._license_id = license_id

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
	    elif isinstance(value, datetime):
		result[attr] = str(value.date())
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()
