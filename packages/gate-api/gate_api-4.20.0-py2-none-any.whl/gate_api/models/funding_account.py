# coding: utf-8

"""
    Gate API v4

    Welcome to Gate.io API  APIv4 provides spot, margin and futures trading operations. There are public APIs to retrieve the real-time market statistics, and private APIs which needs authentication to trade on user's behalf.  # noqa: E501

    Contact: support@mail.gate.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from gate_api.configuration import Configuration


class FundingAccount(object):
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
    openapi_types = {'currency': 'str', 'available': 'str', 'locked': 'str', 'lent': 'str', 'total_lent': 'str'}

    attribute_map = {
        'currency': 'currency',
        'available': 'available',
        'locked': 'locked',
        'lent': 'lent',
        'total_lent': 'total_lent',
    }

    def __init__(
        self, currency=None, available=None, locked=None, lent=None, total_lent=None, local_vars_configuration=None
    ):  # noqa: E501
        # type: (str, str, str, str, str, Configuration) -> None
        """FundingAccount - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._currency = None
        self._available = None
        self._locked = None
        self._lent = None
        self._total_lent = None
        self.discriminator = None

        if currency is not None:
            self.currency = currency
        if available is not None:
            self.available = available
        if locked is not None:
            self.locked = locked
        if lent is not None:
            self.lent = lent
        if total_lent is not None:
            self.total_lent = total_lent

    @property
    def currency(self):
        """Gets the currency of this FundingAccount.  # noqa: E501

        Currency name  # noqa: E501

        :return: The currency of this FundingAccount.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this FundingAccount.

        Currency name  # noqa: E501

        :param currency: The currency of this FundingAccount.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def available(self):
        """Gets the available of this FundingAccount.  # noqa: E501

        Available assets to lend, which is identical to spot account `available`  # noqa: E501

        :return: The available of this FundingAccount.  # noqa: E501
        :rtype: str
        """
        return self._available

    @available.setter
    def available(self, available):
        """Sets the available of this FundingAccount.

        Available assets to lend, which is identical to spot account `available`  # noqa: E501

        :param available: The available of this FundingAccount.  # noqa: E501
        :type: str
        """

        self._available = available

    @property
    def locked(self):
        """Gets the locked of this FundingAccount.  # noqa: E501

        Locked amount. i.e. amount in `open` loans  # noqa: E501

        :return: The locked of this FundingAccount.  # noqa: E501
        :rtype: str
        """
        return self._locked

    @locked.setter
    def locked(self, locked):
        """Sets the locked of this FundingAccount.

        Locked amount. i.e. amount in `open` loans  # noqa: E501

        :param locked: The locked of this FundingAccount.  # noqa: E501
        :type: str
        """

        self._locked = locked

    @property
    def lent(self):
        """Gets the lent of this FundingAccount.  # noqa: E501

        Amount that is loaned but not repaid  # noqa: E501

        :return: The lent of this FundingAccount.  # noqa: E501
        :rtype: str
        """
        return self._lent

    @lent.setter
    def lent(self, lent):
        """Sets the lent of this FundingAccount.

        Amount that is loaned but not repaid  # noqa: E501

        :param lent: The lent of this FundingAccount.  # noqa: E501
        :type: str
        """

        self._lent = lent

    @property
    def total_lent(self):
        """Gets the total_lent of this FundingAccount.  # noqa: E501

        Amount used for lending. total_lent = lent + locked  # noqa: E501

        :return: The total_lent of this FundingAccount.  # noqa: E501
        :rtype: str
        """
        return self._total_lent

    @total_lent.setter
    def total_lent(self, total_lent):
        """Sets the total_lent of this FundingAccount.

        Amount used for lending. total_lent = lent + locked  # noqa: E501

        :param total_lent: The total_lent of this FundingAccount.  # noqa: E501
        :type: str
        """

        self._total_lent = total_lent

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
        if not isinstance(other, FundingAccount):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FundingAccount):
            return True

        return self.to_dict() != other.to_dict()
