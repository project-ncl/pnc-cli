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


class BuildStatusChangedEventRest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuildStatusChangedEventRest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'old_status': 'str',
            'new_status': 'str',
            'build_task_id': 'int',
            'user_id': 'int',
            'build_configuration_id': 'int',
            'build_configuration_name': 'str',
            'build_start_time': 'datetime',
            'build_end_time': 'datetime'
        }

        self.attribute_map = {
            'old_status': 'oldStatus',
            'new_status': 'newStatus',
            'build_task_id': 'buildTaskId',
            'user_id': 'userId',
            'build_configuration_id': 'buildConfigurationId',
            'build_configuration_name': 'buildConfigurationName',
            'build_start_time': 'buildStartTime',
            'build_end_time': 'buildEndTime'
        }

        self._old_status = None
        self._new_status = None
        self._build_task_id = None
        self._user_id = None
        self._build_configuration_id = None
        self._build_configuration_name = None
        self._build_start_time = None
        self._build_end_time = None

    @property
    def old_status(self):
        """
        Gets the old_status of this BuildStatusChangedEventRest.


        :return: The old_status of this BuildStatusChangedEventRest.
        :rtype: str
        """
        return self._old_status

    @old_status.setter
    def old_status(self, old_status):
        """
        Sets the old_status of this BuildStatusChangedEventRest.


        :param old_status: The old_status of this BuildStatusChangedEventRest.
        :type: str
        """
        allowed_values = ["NEW", "WAITING_FOR_DEPENDENCIES", "BUILDING", "BUILD_COMPLETED", "DONE", "REJECTED", "REJECTED_FAILED_DEPENDENCIES", "REJECTED_ALREADY_BUILT", "SYSTEM_ERROR", "DONE_WITH_ERRORS"]
        if old_status not in allowed_values:
            raise ValueError(
                "Invalid value for `old_status`, must be one of {0}"
                .format(allowed_values)
            )
        self._old_status = old_status

    @property
    def new_status(self):
        """
        Gets the new_status of this BuildStatusChangedEventRest.


        :return: The new_status of this BuildStatusChangedEventRest.
        :rtype: str
        """
        return self._new_status

    @new_status.setter
    def new_status(self, new_status):
        """
        Sets the new_status of this BuildStatusChangedEventRest.


        :param new_status: The new_status of this BuildStatusChangedEventRest.
        :type: str
        """
        allowed_values = ["NEW", "WAITING_FOR_DEPENDENCIES", "BUILDING", "BUILD_COMPLETED", "DONE", "REJECTED", "REJECTED_FAILED_DEPENDENCIES", "REJECTED_ALREADY_BUILT", "SYSTEM_ERROR", "DONE_WITH_ERRORS"]
        if new_status not in allowed_values:
            raise ValueError(
                "Invalid value for `new_status`, must be one of {0}"
                .format(allowed_values)
            )
        self._new_status = new_status

    @property
    def build_task_id(self):
        """
        Gets the build_task_id of this BuildStatusChangedEventRest.


        :return: The build_task_id of this BuildStatusChangedEventRest.
        :rtype: int
        """
        return self._build_task_id

    @build_task_id.setter
    def build_task_id(self, build_task_id):
        """
        Sets the build_task_id of this BuildStatusChangedEventRest.


        :param build_task_id: The build_task_id of this BuildStatusChangedEventRest.
        :type: int
        """
        self._build_task_id = build_task_id

    @property
    def user_id(self):
        """
        Gets the user_id of this BuildStatusChangedEventRest.


        :return: The user_id of this BuildStatusChangedEventRest.
        :rtype: int
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this BuildStatusChangedEventRest.


        :param user_id: The user_id of this BuildStatusChangedEventRest.
        :type: int
        """
        self._user_id = user_id

    @property
    def build_configuration_id(self):
        """
        Gets the build_configuration_id of this BuildStatusChangedEventRest.


        :return: The build_configuration_id of this BuildStatusChangedEventRest.
        :rtype: int
        """
        return self._build_configuration_id

    @build_configuration_id.setter
    def build_configuration_id(self, build_configuration_id):
        """
        Sets the build_configuration_id of this BuildStatusChangedEventRest.


        :param build_configuration_id: The build_configuration_id of this BuildStatusChangedEventRest.
        :type: int
        """
        self._build_configuration_id = build_configuration_id

    @property
    def build_configuration_name(self):
        """
        Gets the build_configuration_name of this BuildStatusChangedEventRest.


        :return: The build_configuration_name of this BuildStatusChangedEventRest.
        :rtype: str
        """
        return self._build_configuration_name

    @build_configuration_name.setter
    def build_configuration_name(self, build_configuration_name):
        """
        Sets the build_configuration_name of this BuildStatusChangedEventRest.


        :param build_configuration_name: The build_configuration_name of this BuildStatusChangedEventRest.
        :type: str
        """
        self._build_configuration_name = build_configuration_name

    @property
    def build_start_time(self):
        """
        Gets the build_start_time of this BuildStatusChangedEventRest.


        :return: The build_start_time of this BuildStatusChangedEventRest.
        :rtype: datetime
        """
        return self._build_start_time

    @build_start_time.setter
    def build_start_time(self, build_start_time):
        """
        Sets the build_start_time of this BuildStatusChangedEventRest.


        :param build_start_time: The build_start_time of this BuildStatusChangedEventRest.
        :type: datetime
        """
        self._build_start_time = build_start_time

    @property
    def build_end_time(self):
        """
        Gets the build_end_time of this BuildStatusChangedEventRest.


        :return: The build_end_time of this BuildStatusChangedEventRest.
        :rtype: datetime
        """
        return self._build_end_time

    @build_end_time.setter
    def build_end_time(self, build_end_time):
        """
        Sets the build_end_time of this BuildStatusChangedEventRest.


        :param build_end_time: The build_end_time of this BuildStatusChangedEventRest.
        :type: datetime
        """
        self._build_end_time = build_end_time

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
