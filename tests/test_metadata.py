#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""augur-core unit tests

Unit tests for data_api/metadata.se.

@author Jack Peterson (jack@tinybike.net)

"""
import sys
import os
import unittest
from ethereum import tester

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(HERE))

from contract import ContractTest

def bin2ascii(bytearr):
    return ''.join(map(chr, bytearr))

class TestComments(ContractTest):

    def setUp(self):
        ContractTest.setUp(self, "data_api", "metadata.se")
        self.market = 0xdeadbeef
        self.params = {
            "setMetadata": {
                "market": self.market,
                "tags": ["testing", "Presidential Election", "metadata etc"],
                "source": "http://www.answers.com",
                "links": "https://api.github.com/gists/3a934aaf7aa54ec9d759debe6a0765b4"
            },
        }
        retval = self.contract.setMetadata(
            self.params["setMetadata"]["market"],
            self.params["setMetadata"]["tags"],
            self.params["setMetadata"]["source"],
            self.params["setMetadata"]["links"]
        )
        assert(retval == 1)

    def test_setMetadata(self):
        retval2 = self.contract.setMetadata(
            self.params["setMetadata"]["market"],
            self.params["setMetadata"]["tags"],
            self.params["setMetadata"]["source"],
            self.params["setMetadata"]["links"]
        )
        assert(retval2 == 0)

    def test_getMetadata(self):
        metadata = self.contract.getMetadata(self.market)
        for i in range(len(self.params["setMetadata"]["tags"])):
            assert(self.params["setMetadata"]["tags"][i] == hex(metadata[i] % 2**256)[2:-1].decode("hex"))
        sourceLength = metadata[3]
        linksLength = metadata[4]
        assert(sourceLength == len(self.params["setMetadata"]["source"]))
        assert(linksLength == len(self.params["setMetadata"]["links"]))
        assert(self.params["setMetadata"]["source"] == bin2ascii(metadata[5:5+sourceLength]))
        assert(self.params["setMetadata"]["links"] == bin2ascii(metadata[5+sourceLength:]))

    def test_getTags(self):
        tags = self.contract.getTags(self.market)
        assert(len(tags) == len(self.params["setMetadata"]["tags"]))
        for i, tag in enumerate(tags):
            assert(self.params["setMetadata"]["tags"][i] == hex(tag % 2**256)[2:-1].decode("hex"))

    def test_getSource(self):
        source = self.contract.getSource(self.market)
        assert(source == self.params["setMetadata"]["source"])

    def test_getLinks(self):
        links = self.contract.getLinks(self.market)
        assert(links == self.params["setMetadata"]["links"])

    def test_getSourceLength(self):
        sourceLength = self.contract.getSourceLength(self.market)
        assert(sourceLength == len(self.params["setMetadata"]["source"]))

    def test_getLinksLength(self):
        linksLength = self.contract.getLinksLength(self.market)
        assert(linksLength == len(self.params["setMetadata"]["links"]))

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestComments)
    unittest.TextTestRunner(verbosity=2).run(suite)
