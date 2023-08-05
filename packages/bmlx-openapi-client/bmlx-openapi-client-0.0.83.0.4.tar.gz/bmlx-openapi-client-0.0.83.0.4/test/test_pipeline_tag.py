# coding: utf-8

"""
    bmlx api-server.

    Documentation of bmlx api-server apis. To find more info about generating spec from source, please refer to https://goswagger.io/use/spec.html  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import openapi_client
from openapi_client.models.pipeline_tag import PipelineTag  # noqa: E501
from openapi_client.rest import ApiException

class TestPipelineTag(unittest.TestCase):
    """PipelineTag unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PipelineTag
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.pipeline_tag.PipelineTag()  # noqa: E501
        if include_optional :
            return PipelineTag(
                name = '0'
            )
        else :
            return PipelineTag(
        )

    def testPipelineTag(self):
        """Test PipelineTag"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
