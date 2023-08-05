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


class UpdateVideoRequest(JDCloudRequest):
    """
    修改视频信息
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateVideoRequest, self).__init__(
            '/videos/{videoId}', 'PUT', header, version)
        self.parameters = parameters


class UpdateVideoParameters(object):

    def __init__(self, videoId, ):
        """
        :param videoId: 视频ID
        """

        self.videoId = videoId
        self.name = None
        self.categoryId = None
        self.tags = None
        self.coverUrl = None
        self.description = None

    def setName(self, name):
        """
        :param name: (Optional) 视频名称
        """
        self.name = name

    def setCategoryId(self, categoryId):
        """
        :param categoryId: (Optional) 分类ID
        """
        self.categoryId = categoryId

    def setTags(self, tags):
        """
        :param tags: (Optional) 标签
        """
        self.tags = tags

    def setCoverUrl(self, coverUrl):
        """
        :param coverUrl: (Optional) 封面地址
        """
        self.coverUrl = coverUrl

    def setDescription(self, description):
        """
        :param description: (Optional) 视频描述信息
        """
        self.description = description

