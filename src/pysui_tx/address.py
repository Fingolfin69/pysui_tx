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

"""Sui Address Type."""

import base64
import hashlib
from typing import Union
from deprecated.sphinx import deprecated, versionchanged
from pysui_tx.client_types import SuiBaseType
from pysui_tx.scalars import SuiString


def valid_sui_address(address: str) -> bool:
    return True

class SuiAddress(SuiBaseType):
    """Sui Address Type."""

    @versionchanged(version="0.76.0", reason="Moved validation to commons.")
    def __init__(self, identifier: Union[SuiString, str]) -> None:
        """Initialize address."""
        testvalid: str = identifier if isinstance(identifier, str) else identifier.value
        if valid_sui_address(testvalid):
            testvalid = (
                testvalid if testvalid.startswith("0x") else format(f"0x{testvalid}")
            )
            super().__init__(SuiString(testvalid))
        else:
            raise ValueError(f"{testvalid} is not valid address string")
        # Alias for transaction validation
        self.address = testvalid

    @property
    def signer(self) -> str:
        """Alias for signer in transaction validation."""
        return self.address

    @property
    def owner(self) -> str:
        """Alias for signer in transaction validation."""
        return self.address

    @property
    def sender(self) -> str:
        """Alias for signer in transaction validation."""
        return self.address

    @property
    def sender_address(self) -> str:
        """Alias for sender in transaction validation."""
        return self.address

    @property
    def recipient(self) -> str:
        """Alias for recipient in transaction validation."""
        return self.address

    @property
    def validator(self) -> str:
        """Alias for recipient in transaction validation."""
        return self.address

    @property
    def recipients(self) -> str:
        """Alias for recipients in transaction validation."""
        return self.address

    @classmethod
    def from_keypair_string(cls, keystring: str) -> "SuiAddress":
        """Address from base64 encoded keypair string with no validation."""
        return cls.from_bytes(base64.b64decode(keystring))

    @classmethod
    def from_bytes(cls, in_bytes: bytes) -> "SuiAddress":
        """Create address from bytes."""
        digest = in_bytes[0:33] if in_bytes[0] == 0 else in_bytes[0:34]
        hash_bytes = hashlib.blake2b(digest, digest_size=32).hexdigest()
        return cls(hash_bytes)
