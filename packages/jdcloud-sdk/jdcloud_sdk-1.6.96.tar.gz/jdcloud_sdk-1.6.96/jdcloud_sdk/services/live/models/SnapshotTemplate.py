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


class SnapshotTemplate(object):

    def __init__(self, format=None, width=None, height=None, fillType=None, snapshotInterval=None, saveMode=None, saveBucket=None, saveEndpoint=None, template=None):
        """
        :param format: (Optional) 截图格式

        :param width: (Optional) 截图宽度
- 单位: 像素

        :param height: (Optional) 截图高度
- 单位: 像素

        :param fillType: (Optional) 截图与设定的宽高不匹配时的处理规则
  1: 拉伸
  2: 留黑
  3: 留白
  4: 高斯模糊

        :param snapshotInterval: (Optional) 截图周期
- 单位: 秒

        :param saveMode: (Optional) 存储模式
  1: 覆盖
  2: 顺序编号存储

        :param saveBucket: (Optional) 存储桶
        :param saveEndpoint: (Optional) 存储地址
        :param template: (Optional) 截图模板自定义名称

        """

        self.format = format
        self.width = width
        self.height = height
        self.fillType = fillType
        self.snapshotInterval = snapshotInterval
        self.saveMode = saveMode
        self.saveBucket = saveBucket
        self.saveEndpoint = saveEndpoint
        self.template = template
