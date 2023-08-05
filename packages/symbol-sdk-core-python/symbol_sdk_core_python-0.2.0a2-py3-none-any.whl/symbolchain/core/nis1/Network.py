import base64

import sha3

from ..ByteArray import ByteArray
from ..Network import Network as BasicNetwork


class Address(ByteArray):
    """Represents a nis address."""

    # pylint: disable=too-few-public-methods

    def __init__(self, address):
        """Creates an address from a decoded or encoded address."""
        raw_bytes = address
        if isinstance(raw_bytes, str):
            raw_bytes = base64.b32decode(raw_bytes)

        super().__init__(25, raw_bytes, Address)

    def __str__(self):
        return base64.b32encode(self.bytes).decode('utf8')


class Network(BasicNetwork):
    """Represents a nis network."""

    def address_hasher(self):
        return sha3.keccak_256()

    def create_address(self, address_without_checksum, checksum):
        return Address(address_without_checksum + checksum)


Network.MAINNET = Network('mainnet', 0x68)
Network.TESTNET = Network('testnet', 0x98)
Network.NETWORKS = [Network.MAINNET, Network.TESTNET]
