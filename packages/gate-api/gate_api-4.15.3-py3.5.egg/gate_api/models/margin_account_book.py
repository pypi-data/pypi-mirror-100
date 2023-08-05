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


class MarginAccountBook(object):
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
    openapi_types = {
        'id': 'str',
        'time': 'str',
        'currency': 'str',
        'currency_pair': 'str',
        'change': 'str',
        'balance': 'str',
    }

    attribute_map = {
        'id': 'id',
        'time': 'time',
        'currency': 'currency',
        'currency_pair': 'currency_pair',
        'change': 'change',
        'balance': 'balance',
    }

    def __init__(
        self,
        id=None,
        time=None,
        currency=None,
        currency_pair=None,
        change=None,
        balance=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        # type: (str, str, str, str, str, str, Configuration) -> None
        """MarginAccountBook - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._time = None
        self._currency = None
        self._currency_pair = None
        self._change = None
        self._balance = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if time is not None:
            self.time = time
        if currency is not None:
            self.currency = currency
        if currency_pair is not None:
            self.currency_pair = currency_pair
        if change is not None:
            self.change = change
        if balance is not None:
            self.balance = balance

    @property
    def id(self):
        """Gets the id of this MarginAccountBook.  # noqa: E501

        Balance change record ID  # noqa: E501

        :return: The id of this MarginAccountBook.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MarginAccountBook.

        Balance change record ID  # noqa: E501

        :param id: The id of this MarginAccountBook.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def time(self):
        """Gets the time of this MarginAccountBook.  # noqa: E501

        Balance changed timestamp  # noqa: E501

        :return: The time of this MarginAccountBook.  # noqa: E501
        :rtype: str
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this MarginAccountBook.

        Balance changed timestamp  # noqa: E501

        :param time: The time of this MarginAccountBook.  # noqa: E501
        :type: str
        """

        self._time = time

    @property
    def currency(self):
        """Gets the currency of this MarginAccountBook.  # noqa: E501

        Currency changed  # noqa: E501

        :return: The currency of this MarginAccountBook.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this MarginAccountBook.

        Currency changed  # noqa: E501

        :param currency: The currency of this MarginAccountBook.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def currency_pair(self):
        """Gets the currency_pair of this MarginAccountBook.  # noqa: E501

        Account currency pair  # noqa: E501

        :return: The currency_pair of this MarginAccountBook.  # noqa: E501
        :rtype: str
        """
        return self._currency_pair

    @currency_pair.setter
    def currency_pair(self, currency_pair):
        """Sets the currency_pair of this MarginAccountBook.

        Account currency pair  # noqa: E501

        :param currency_pair: The currency_pair of this MarginAccountBook.  # noqa: E501
        :type: str
        """

        self._currency_pair = currency_pair

    @property
    def change(self):
        """Gets the change of this MarginAccountBook.  # noqa: E501

        Amount changed. Positive value means transferring in, while negative out  # noqa: E501

        :return: The change of this MarginAccountBook.  # noqa: E501
        :rtype: str
        """
        return self._change

    @change.setter
    def change(self, change):
        """Sets the change of this MarginAccountBook.

        Amount changed. Positive value means transferring in, while negative out  # noqa: E501

        :param change: The change of this MarginAccountBook.  # noqa: E501
        :type: str
        """

        self._change = change

    @property
    def balance(self):
        """Gets the balance of this MarginAccountBook.  # noqa: E501

        Balance after change  # noqa: E501

        :return: The balance of this MarginAccountBook.  # noqa: E501
        :rtype: str
        """
        return self._balance

    @balance.setter
    def balance(self, balance):
        """Sets the balance of this MarginAccountBook.

        Balance after change  # noqa: E501

        :param balance: The balance of this MarginAccountBook.  # noqa: E501
        :type: str
        """

        self._balance = balance

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
        if not isinstance(other, MarginAccountBook):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MarginAccountBook):
            return True

        return self.to_dict() != other.to_dict()
