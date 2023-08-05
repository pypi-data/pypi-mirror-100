# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ConnectivityRemoteHost(object):
    """NOTE: This class is auto generated by the swagger code generator program.

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
        'host_id': 'str',
        'l2_connectivity': 'list[L2Connectivity]',
        'l3_connectivity': 'list[L3Connectivity]'
    }

    attribute_map = {
        'host_id': 'host_id',
        'l2_connectivity': 'l2_connectivity',
        'l3_connectivity': 'l3_connectivity'
    }

    def __init__(self, host_id=None, l2_connectivity=None, l3_connectivity=None):  # noqa: E501
        """ConnectivityRemoteHost - a model defined in Swagger"""  # noqa: E501

        self._host_id = None
        self._l2_connectivity = None
        self._l3_connectivity = None
        self.discriminator = None

        if host_id is not None:
            self.host_id = host_id
        if l2_connectivity is not None:
            self.l2_connectivity = l2_connectivity
        if l3_connectivity is not None:
            self.l3_connectivity = l3_connectivity

    @property
    def host_id(self):
        """Gets the host_id of this ConnectivityRemoteHost.  # noqa: E501


        :return: The host_id of this ConnectivityRemoteHost.  # noqa: E501
        :rtype: str
        """
        return self._host_id

    @host_id.setter
    def host_id(self, host_id):
        """Sets the host_id of this ConnectivityRemoteHost.


        :param host_id: The host_id of this ConnectivityRemoteHost.  # noqa: E501
        :type: str
        """

        self._host_id = host_id

    @property
    def l2_connectivity(self):
        """Gets the l2_connectivity of this ConnectivityRemoteHost.  # noqa: E501


        :return: The l2_connectivity of this ConnectivityRemoteHost.  # noqa: E501
        :rtype: list[L2Connectivity]
        """
        return self._l2_connectivity

    @l2_connectivity.setter
    def l2_connectivity(self, l2_connectivity):
        """Sets the l2_connectivity of this ConnectivityRemoteHost.


        :param l2_connectivity: The l2_connectivity of this ConnectivityRemoteHost.  # noqa: E501
        :type: list[L2Connectivity]
        """

        self._l2_connectivity = l2_connectivity

    @property
    def l3_connectivity(self):
        """Gets the l3_connectivity of this ConnectivityRemoteHost.  # noqa: E501


        :return: The l3_connectivity of this ConnectivityRemoteHost.  # noqa: E501
        :rtype: list[L3Connectivity]
        """
        return self._l3_connectivity

    @l3_connectivity.setter
    def l3_connectivity(self, l3_connectivity):
        """Sets the l3_connectivity of this ConnectivityRemoteHost.


        :param l3_connectivity: The l3_connectivity of this ConnectivityRemoteHost.  # noqa: E501
        :type: list[L3Connectivity]
        """

        self._l3_connectivity = l3_connectivity

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
            else:
                result[attr] = value
        if issubclass(ConnectivityRemoteHost, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ConnectivityRemoteHost):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
