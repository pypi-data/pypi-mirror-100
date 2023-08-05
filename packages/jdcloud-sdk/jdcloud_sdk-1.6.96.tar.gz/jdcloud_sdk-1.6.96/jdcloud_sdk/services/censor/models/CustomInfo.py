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


class CustomInfo(object):

    def __init__(self, libId=None, websiteInstanceId=None, resourceType=None, matchType=None, name=None, scenes=None, suggestion=None, status=None, updateTime=None, itemNumber=None):
        """
        :param libId: (Optional) 敏感库id
        :param websiteInstanceId: (Optional) 站点检查实例Id，多个以 , 分割
        :param resourceType: (Optional) 文件类型，text-文本，image-图片，audio-音频，video-视频
        :param matchType: (Optional) 匹配方式，exact:精确匹配，fuzzy:模糊匹配；仅限文本类型
        :param name: (Optional) 敏感库名
        :param scenes: (Optional) 文本/语音支持 antispam-反垃圾，视频/图片支持 porn-涉黄，terrorism-涉政暴恐
        :param suggestion: (Optional) white 白名单，black 黑名单，suspect 疑似名单
        :param status: (Optional) 状态 1启用，0禁用
        :param updateTime: (Optional) 更新时间
        :param itemNumber: (Optional) 该敏感库下包含的item条数
        """

        self.libId = libId
        self.websiteInstanceId = websiteInstanceId
        self.resourceType = resourceType
        self.matchType = matchType
        self.name = name
        self.scenes = scenes
        self.suggestion = suggestion
        self.status = status
        self.updateTime = updateTime
        self.itemNumber = itemNumber
