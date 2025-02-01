#    Copyright Frank V. Castellucci
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# -*- coding: utf-8 -*-

"""Utility functions."""

import math
import base64
import binascii
import base58

def hexstring_to_sui_id(indata: str, default_fill_length: int = 64) -> str:
    """Convert hexstring to valid full length sui address/object id."""

    if len(indata) < default_fill_length:
        if indata.count("x") or indata.count("X"):
            indata = indata[2:]
        indata = f"0x{indata.zfill(default_fill_length)}"
    return indata


def hexstring_to_list(indata: str, default_fill_length: int = 64) -> list[int]:
    """hexstring_to_list convert a hexstr (e.g. 0x...) into a list of ints.

    :param indata: Data to conver to list of ints
    :type indata: str
    :return: converted indata to int list
    :rtype: list[int]
    """
    return [int(x) for x in binascii.unhexlify(hexstring_to_sui_id(indata)[2:])]


def b64str_to_list(indata: str) -> list[int]:
    """b64str_to_list convert a base64 string into a list of ints.

    :param indata: Base64 encoded string
    :type indata: str
    :return: converted indata to int list
    :rtype: list[int]
    """
    b64bytes = base64.b64decode(indata)
    return [int(x) for x in b64bytes]


def from_list_to_b58str(indata: list) -> str:
    """From list to b58 string."""
    return base58.b58encode(bytearray(indata)).decode("utf-8")


def b58str_to_list(indata: str) -> list[int]:
    """b58str_to_list convert a base58 string into a list of ints.

    :param indata: Base58 encoded string
    :type indata: str
    :return: converted indata to int list
    :rtype: list[int]
    """
    try:
        decode_bytes = base58.b58decode(indata)
    # Fall back if invalid base58 str
    except ValueError:
        decode_bytes = base64.b64decode(indata)
    return [int(x) for x in decode_bytes]


def int_to_listu8(byte_count: int, in_el: int) -> list[int]:
    """int_to_listu8 converts integer to array of u8 bytes.

    :param byte_count: Expected byte count of integer
    :type byte_count: int
    :param in_el: The integer elements
    :type in_el: int
    :raises ValueError: If mismatch on expected and actual byte count
    :return: the integer value converted to list of int (u8)
    :rtype: list[int]
    """
    byte_res = math.ceil(in_el.bit_length() / 8)
    if byte_res == byte_count:
        return list(in_el.to_bytes(byte_res, "little"))
    raise ValueError(f"Expected byte count {byte_count} found byte count {byte_res}")
