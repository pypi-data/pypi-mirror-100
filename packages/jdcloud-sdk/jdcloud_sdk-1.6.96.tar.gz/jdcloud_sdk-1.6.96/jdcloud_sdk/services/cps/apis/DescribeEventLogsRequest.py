# coding=utf8

# Copyright 2018 JDCLOUD.COM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE: This class is auto generated by the jdcloud code generator program.

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class DescribeEventLogsRequest(JDCloudRequest):
    """
    查询云物理服务器监控报警日志信息
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeEventLogsRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}/describeEventLogs', 'GET', header, version)
        self.parameters = parameters


class DescribeEventLogsParameters(object):

    def __init__(self, regionId, instanceId, ):
        """
        :param regionId: 地域ID，可调用接口（describeRegiones）获取云物理服务器支持的地域
        :param instanceId: 云物理服务器ID
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.pageNumber = None
        self.pageSize = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码；默认为1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小；默认为20；取值范围[20, 100]
        """
        self.pageSize = pageSize

