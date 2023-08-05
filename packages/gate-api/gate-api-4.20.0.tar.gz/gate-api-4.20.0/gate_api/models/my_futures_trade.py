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


class MyFuturesTrade(object):
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
        'id': 'int',
        'create_time': 'float',
        'contract': 'str',
        'order_id': 'str',
        'size': 'int',
        'price': 'str',
        'role': 'str',
    }

    attribute_map = {
        'id': 'id',
        'create_time': 'create_time',
        'contract': 'contract',
        'order_id': 'order_id',
        'size': 'size',
        'price': 'price',
        'role': 'role',
    }

    def __init__(
        self,
        id=None,
        create_time=None,
        contract=None,
        order_id=None,
        size=None,
        price=None,
        role=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        # type: (int, float, str, str, int, str, str, Configuration) -> None
        """MyFuturesTrade - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._create_time = None
        self._contract = None
        self._order_id = None
        self._size = None
        self._price = None
        self._role = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if create_time is not None:
            self.create_time = create_time
        if contract is not None:
            self.contract = contract
        if order_id is not None:
            self.order_id = order_id
        if size is not None:
            self.size = size
        if price is not None:
            self.price = price
        if role is not None:
            self.role = role

    @property
    def id(self):
        """Gets the id of this MyFuturesTrade.  # noqa: E501

        Trade ID  # noqa: E501

        :return: The id of this MyFuturesTrade.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MyFuturesTrade.

        Trade ID  # noqa: E501

        :param id: The id of this MyFuturesTrade.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def create_time(self):
        """Gets the create_time of this MyFuturesTrade.  # noqa: E501

        Trading time  # noqa: E501

        :return: The create_time of this MyFuturesTrade.  # noqa: E501
        :rtype: float
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this MyFuturesTrade.

        Trading time  # noqa: E501

        :param create_time: The create_time of this MyFuturesTrade.  # noqa: E501
        :type: float
        """

        self._create_time = create_time

    @property
    def contract(self):
        """Gets the contract of this MyFuturesTrade.  # noqa: E501

        Futures contract  # noqa: E501

        :return: The contract of this MyFuturesTrade.  # noqa: E501
        :rtype: str
        """
        return self._contract

    @contract.setter
    def contract(self, contract):
        """Sets the contract of this MyFuturesTrade.

        Futures contract  # noqa: E501

        :param contract: The contract of this MyFuturesTrade.  # noqa: E501
        :type: str
        """

        self._contract = contract

    @property
    def order_id(self):
        """Gets the order_id of this MyFuturesTrade.  # noqa: E501

        Order ID related  # noqa: E501

        :return: The order_id of this MyFuturesTrade.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this MyFuturesTrade.

        Order ID related  # noqa: E501

        :param order_id: The order_id of this MyFuturesTrade.  # noqa: E501
        :type: str
        """

        self._order_id = order_id

    @property
    def size(self):
        """Gets the size of this MyFuturesTrade.  # noqa: E501

        Trading size  # noqa: E501

        :return: The size of this MyFuturesTrade.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this MyFuturesTrade.

        Trading size  # noqa: E501

        :param size: The size of this MyFuturesTrade.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def price(self):
        """Gets the price of this MyFuturesTrade.  # noqa: E501

        Trading price  # noqa: E501

        :return: The price of this MyFuturesTrade.  # noqa: E501
        :rtype: str
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this MyFuturesTrade.

        Trading price  # noqa: E501

        :param price: The price of this MyFuturesTrade.  # noqa: E501
        :type: str
        """

        self._price = price

    @property
    def role(self):
        """Gets the role of this MyFuturesTrade.  # noqa: E501

        Trade role. Available values are `taker` and `maker`  # noqa: E501

        :return: The role of this MyFuturesTrade.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this MyFuturesTrade.

        Trade role. Available values are `taker` and `maker`  # noqa: E501

        :param role: The role of this MyFuturesTrade.  # noqa: E501
        :type: str
        """
        allowed_values = ["taker", "maker"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and role not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `role` ({0}), must be one of {1}".format(role, allowed_values)  # noqa: E501
            )

        self._role = role

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
        if not isinstance(other, MyFuturesTrade):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MyFuturesTrade):
            return True

        return self.to_dict() != other.to_dict()
