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


class MultiChainAddressItem(object):
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
        'chain': 'str',
        'address': 'str',
        'payment_id': 'str',
        'payment_name': 'str',
        'obtain_failed': 'int',
    }

    attribute_map = {
        'chain': 'chain',
        'address': 'address',
        'payment_id': 'payment_id',
        'payment_name': 'payment_name',
        'obtain_failed': 'obtain_failed',
    }

    def __init__(
        self,
        chain=None,
        address=None,
        payment_id=None,
        payment_name=None,
        obtain_failed=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        # type: (str, str, str, str, int, Configuration) -> None
        """MultiChainAddressItem - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._chain = None
        self._address = None
        self._payment_id = None
        self._payment_name = None
        self._obtain_failed = None
        self.discriminator = None

        if chain is not None:
            self.chain = chain
        if address is not None:
            self.address = address
        if payment_id is not None:
            self.payment_id = payment_id
        if payment_name is not None:
            self.payment_name = payment_name
        if obtain_failed is not None:
            self.obtain_failed = obtain_failed

    @property
    def chain(self):
        """Gets the chain of this MultiChainAddressItem.  # noqa: E501

        Name of the chain  # noqa: E501

        :return: The chain of this MultiChainAddressItem.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this MultiChainAddressItem.

        Name of the chain  # noqa: E501

        :param chain: The chain of this MultiChainAddressItem.  # noqa: E501
        :type: str
        """

        self._chain = chain

    @property
    def address(self):
        """Gets the address of this MultiChainAddressItem.  # noqa: E501

        Deposit address  # noqa: E501

        :return: The address of this MultiChainAddressItem.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this MultiChainAddressItem.

        Deposit address  # noqa: E501

        :param address: The address of this MultiChainAddressItem.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def payment_id(self):
        """Gets the payment_id of this MultiChainAddressItem.  # noqa: E501

        Notes that some currencies required(e.g., Tag, Memo) when depositing  # noqa: E501

        :return: The payment_id of this MultiChainAddressItem.  # noqa: E501
        :rtype: str
        """
        return self._payment_id

    @payment_id.setter
    def payment_id(self, payment_id):
        """Sets the payment_id of this MultiChainAddressItem.

        Notes that some currencies required(e.g., Tag, Memo) when depositing  # noqa: E501

        :param payment_id: The payment_id of this MultiChainAddressItem.  # noqa: E501
        :type: str
        """

        self._payment_id = payment_id

    @property
    def payment_name(self):
        """Gets the payment_name of this MultiChainAddressItem.  # noqa: E501

        Note type, `Tag` or `Memo`  # noqa: E501

        :return: The payment_name of this MultiChainAddressItem.  # noqa: E501
        :rtype: str
        """
        return self._payment_name

    @payment_name.setter
    def payment_name(self, payment_name):
        """Sets the payment_name of this MultiChainAddressItem.

        Note type, `Tag` or `Memo`  # noqa: E501

        :param payment_name: The payment_name of this MultiChainAddressItem.  # noqa: E501
        :type: str
        """

        self._payment_name = payment_name

    @property
    def obtain_failed(self):
        """Gets the obtain_failed of this MultiChainAddressItem.  # noqa: E501

        Whether address is obtained. 0 means success. 1 is failure, which needs retries  # noqa: E501

        :return: The obtain_failed of this MultiChainAddressItem.  # noqa: E501
        :rtype: int
        """
        return self._obtain_failed

    @obtain_failed.setter
    def obtain_failed(self, obtain_failed):
        """Sets the obtain_failed of this MultiChainAddressItem.

        Whether address is obtained. 0 means success. 1 is failure, which needs retries  # noqa: E501

        :param obtain_failed: The obtain_failed of this MultiChainAddressItem.  # noqa: E501
        :type: int
        """

        self._obtain_failed = obtain_failed

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
        if not isinstance(other, MultiChainAddressItem):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MultiChainAddressItem):
            return True

        return self.to_dict() != other.to_dict()
