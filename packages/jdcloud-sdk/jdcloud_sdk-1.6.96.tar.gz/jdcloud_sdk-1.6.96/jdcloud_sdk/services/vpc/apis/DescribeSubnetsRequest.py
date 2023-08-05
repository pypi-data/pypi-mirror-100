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


class DescribeSubnetsRequest(JDCloudRequest):
    """
    查询子网列表
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeSubnetsRequest, self).__init__(
            '/regions/{regionId}/subnets/', 'GET', header, version)
        self.parameters = parameters


class DescribeSubnetsParameters(object):

    def __init__(self, regionId, ):
        """
        :param regionId: Region ID
        """

        self.regionId = regionId
        self.pageNumber = None
        self.pageSize = None
        self.filters = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码, 默认为1, 取值范围：[1,∞), 页码超过总页数时, 显示最后一页
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小，默认为20，取值范围：[10,100]
        """
        self.pageSize = pageSize

    def setFilters(self, filters):
        """
        :param filters: (Optional) subnetIds - subnet ID列表，支持多个
subnetNames - subnet名称列表，支持多个
routeTableId	- 子网关联路由表Id，支持单个
aclId - 子网关联acl Id，支持单个
vpcId - 子网所属VPC Id，支持单个
subnetType - 子网类型，取值：all(全部类型)，standard(标准子网)，edge(边缘子网)，默认standard ，支持单个
azs - 可用区，支持多个

        """
        self.filters = filters

