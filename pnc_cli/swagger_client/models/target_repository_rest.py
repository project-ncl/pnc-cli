# coding: utf-8

"""

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from datetime import datetime
from pprint import pformat
from six import iteritems
import re


class TargetRepositoryRest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'temporary_repo': 'bool',
        'identifier': 'str',
        'repository_type': 'str',
        'repository_path': 'str',
        'artifact_ids': 'list[int]'
    }

    attribute_map = {
        'id': 'id',
        'temporary_repo': 'temporaryRepo',
        'identifier': 'identifier',
        'repository_type': 'repositoryType',
        'repository_path': 'repositoryPath',
        'artifact_ids': 'artifactIds'
    }

    def __init__(self, id=None, temporary_repo=False, identifier=None, repository_type=None, repository_path=None, artifact_ids=None):
        """
        TargetRepositoryRest - a model defined in Swagger
        """

        self._id = None
        self._temporary_repo = None
        self._identifier = None
        self._repository_type = None
        self._repository_path = None
        self._artifact_ids = None

        if id is not None:
          self.id = id
        if temporary_repo is not None:
          self.temporary_repo = temporary_repo
        if identifier is not None:
          self.identifier = identifier
        if repository_type is not None:
          self.repository_type = repository_type
        if repository_path is not None:
          self.repository_path = repository_path
        if artifact_ids is not None:
          self.artifact_ids = artifact_ids

    @property
    def id(self):
        """
        Gets the id of this TargetRepositoryRest.

        :return: The id of this TargetRepositoryRest.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this TargetRepositoryRest.

        :param id: The id of this TargetRepositoryRest.
        :type: int
        """

        self._id = id

    @property
    def temporary_repo(self):
        """
        Gets the temporary_repo of this TargetRepositoryRest.

        :return: The temporary_repo of this TargetRepositoryRest.
        :rtype: bool
        """
        return self._temporary_repo

    @temporary_repo.setter
    def temporary_repo(self, temporary_repo):
        """
        Sets the temporary_repo of this TargetRepositoryRest.

        :param temporary_repo: The temporary_repo of this TargetRepositoryRest.
        :type: bool
        """

        self._temporary_repo = temporary_repo

    @property
    def identifier(self):
        """
        Gets the identifier of this TargetRepositoryRest.

        :return: The identifier of this TargetRepositoryRest.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this TargetRepositoryRest.

        :param identifier: The identifier of this TargetRepositoryRest.
        :type: str
        """

        self._identifier = identifier

    @property
    def repository_type(self):
        """
        Gets the repository_type of this TargetRepositoryRest.

        :return: The repository_type of this TargetRepositoryRest.
        :rtype: str
        """
        return self._repository_type

    @repository_type.setter
    def repository_type(self, repository_type):
        """
        Sets the repository_type of this TargetRepositoryRest.

        :param repository_type: The repository_type of this TargetRepositoryRest.
        :type: str
        """
        allowed_values = ["MAVEN", "NPM", "COCOA_POD", "GENERIC_PROXY"]
        if repository_type not in allowed_values:
            raise ValueError(
                "Invalid value for `repository_type` ({0}), must be one of {1}"
                .format(repository_type, allowed_values)
            )

        self._repository_type = repository_type

    @property
    def repository_path(self):
        """
        Gets the repository_path of this TargetRepositoryRest.

        :return: The repository_path of this TargetRepositoryRest.
        :rtype: str
        """
        return self._repository_path

    @repository_path.setter
    def repository_path(self, repository_path):
        """
        Sets the repository_path of this TargetRepositoryRest.

        :param repository_path: The repository_path of this TargetRepositoryRest.
        :type: str
        """

        self._repository_path = repository_path

    @property
    def artifact_ids(self):
        """
        Gets the artifact_ids of this TargetRepositoryRest.

        :return: The artifact_ids of this TargetRepositoryRest.
        :rtype: list[int]
        """
        return self._artifact_ids

    @artifact_ids.setter
    def artifact_ids(self, artifact_ids):
        """
        Sets the artifact_ids of this TargetRepositoryRest.

        :param artifact_ids: The artifact_ids of this TargetRepositoryRest.
        :type: list[int]
        """

        self._artifact_ids = artifact_ids

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
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, TargetRepositoryRest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
