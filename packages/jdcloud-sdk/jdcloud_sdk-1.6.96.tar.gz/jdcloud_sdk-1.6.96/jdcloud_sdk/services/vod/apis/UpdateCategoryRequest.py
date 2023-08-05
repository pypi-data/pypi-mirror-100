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


class UpdateCategoryRequest(JDCloudRequest):
    """
    修改分类
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateCategoryRequest, self).__init__(
            '/categories/{categoryId}', 'PUT', header, version)
        self.parameters = parameters


class UpdateCategoryParameters(object):

    def __init__(self, categoryId, ):
        """
        :param categoryId: 分类ID
        """

        self.categoryId = categoryId
        self.name = None
        self.parentId = None
        self.description = None

    def setName(self, name):
        """
        :param name: (Optional) 分类名称
        """
        self.name = name

    def setParentId(self, parentId):
        """
        :param parentId: (Optional) 父分类ID，取值为 0 或 null 时，表示该分类为一级分类

        """
        self.parentId = parentId

    def setDescription(self, description):
        """
        :param description: (Optional) 分类描述信息
        """
        self.description = description

