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


class DeleteLiveRecordingsRequest(JDCloudRequest):
    """
    删除录制文件

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DeleteLiveRecordingsRequest, self).__init__(
            '/recordings:delete', 'DELETE', header, version)
        self.parameters = parameters


class DeleteLiveRecordingsParameters(object):

    def __init__(self, fileUrl, ):
        """
        :param fileUrl: 需要删除的录制文件在oss的url

        """

        self.fileUrl = fileUrl
        self.completely = None

    def setCompletely(self, completely):
        """
        :param completely: (Optional) 是否深度删除所有的ts文件，仅对.m3u8录制文件生效。默认: true

        """
        self.completely = completely

