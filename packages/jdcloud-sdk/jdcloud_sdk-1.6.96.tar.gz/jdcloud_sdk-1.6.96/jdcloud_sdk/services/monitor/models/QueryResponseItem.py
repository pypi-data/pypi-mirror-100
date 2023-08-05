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


class QueryResponseItem(object):

    def __init__(self, aggregateTags=None, annotations=None, dps=None, globalAnnotations=None, metric=None, tags=None):
        """
        :param aggregateTags: (Optional) 如果结果集中包含多个时间序列，即它们被聚合
则会显示在所有时间序列中共同发现的标记名称列表
        :param annotations: (Optional) 如果查询检索到时间序列在所请求的时间范围内的注释, 则它们将在该组中返回
每个时间序列的注释将被合并到一个集合中，并按start_time进行排序
        :param dps: (Optional) 由聚合器处理后检索的数据点
每个数据点由一个时间戳和一个值组成
        :param globalAnnotations: (Optional) 查询将在时间范围内扫描全局注释，并在该组中返回结果
        :param metric: (Optional) metric名称
        :param tags: (Optional) 仅当结果为单时间序列时才返回标签列表
如果是聚合则返回空
        """

        self.aggregateTags = aggregateTags
        self.annotations = annotations
        self.dps = dps
        self.globalAnnotations = globalAnnotations
        self.metric = metric
        self.tags = tags
