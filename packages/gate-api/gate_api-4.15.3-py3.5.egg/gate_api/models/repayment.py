# coding: utf-8

"""
    Gate API v4

    APIv4 provides spot, margin and futures trading operations. There are public APIs to retrieve the real-time market statistics, and private APIs which needs authentication to trade on user's behalf.  # noqa: E501

    Contact: support@mail.gate.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from gate_api.configuration import Configuration


class Repayment(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {'id': 'str', 'create_time': 'str', 'principal': 'str', 'interest': 'str'}

    attribute_map = {'id': 'id', 'create_time': 'create_time', 'principal': 'principal', 'interest': 'interest'}

    def __init__(
        self, id=None, create_time=None, principal=None, interest=None, local_vars_configuration=None
    ):  # noqa: E501
        # type: (str, str, str, str, Configuration) -> None
        """Repayment - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._create_time = None
        self._principal = None
        self._interest = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if create_time is not None:
            self.create_time = create_time
        if principal is not None:
            self.principal = principal
        if interest is not None:
            self.interest = interest

    @property
    def id(self):
        """Gets the id of this Repayment.  # noqa: E501

        Loan record ID  # noqa: E501

        :return: The id of this Repayment.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Repayment.

        Loan record ID  # noqa: E501

        :param id: The id of this Repayment.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def create_time(self):
        """Gets the create_time of this Repayment.  # noqa: E501

        Repayment time  # noqa: E501

        :return: The create_time of this Repayment.  # noqa: E501
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this Repayment.

        Repayment time  # noqa: E501

        :param create_time: The create_time of this Repayment.  # noqa: E501
        :type: str
        """

        self._create_time = create_time

    @property
    def principal(self):
        """Gets the principal of this Repayment.  # noqa: E501

        Repaid principal  # noqa: E501

        :return: The principal of this Repayment.  # noqa: E501
        :rtype: str
        """
        return self._principal

    @principal.setter
    def principal(self, principal):
        """Sets the principal of this Repayment.

        Repaid principal  # noqa: E501

        :param principal: The principal of this Repayment.  # noqa: E501
        :type: str
        """

        self._principal = principal

    @property
    def interest(self):
        """Gets the interest of this Repayment.  # noqa: E501

        Repaid interest  # noqa: E501

        :return: The interest of this Repayment.  # noqa: E501
        :rtype: str
        """
        return self._interest

    @interest.setter
    def interest(self, interest):
        """Sets the interest of this Repayment.

        Repaid interest  # noqa: E501

        :param interest: The interest of this Repayment.  # noqa: E501
        :type: str
        """

        self._interest = interest

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], "to_dict") else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Repayment):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Repayment):
            return True

        return self.to_dict() != other.to_dict()
