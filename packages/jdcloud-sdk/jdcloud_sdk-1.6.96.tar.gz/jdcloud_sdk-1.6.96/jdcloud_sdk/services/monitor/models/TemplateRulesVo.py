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


class TemplateRulesVo(object):

    def __init__(self, calculateUnit=None, calculation=None, createTime=None, deleted=None, downSample=None, id=None, metric=None, metricId=None, metricName=None, noticeLevel=None, noticePeriod=None, operation=None, period=None, ruleType=None, serviceCode=None, tag=None, tags=None, threshold=None, times=None, updateTime=None, uuid=None):
        """
        :param calculateUnit: (Optional) 监控项单位
        :param calculation: (Optional) 统计方法：平均值=avg、最大值=max、最小值=min
        :param createTime: (Optional) 
        :param deleted: (Optional) 是否删除 1正常，0删除
        :param downSample: (Optional) downSample
        :param id: (Optional) 触发条件ID
        :param metric: (Optional) 监控项
        :param metricId: (Optional) 监控项ID
        :param metricName: (Optional) 监控项名称
        :param noticeLevel: (Optional) 
        :param noticePeriod: (Optional) 通知周期
        :param operation: (Optional) 报警比较符，只能为以下几种lte(<=),lt(<),gt(>),gte(>=),eq(==),ne(!=)
        :param period: (Optional) 统计周期（单位：分钟）
        :param ruleType: (Optional) 规则类型
        :param serviceCode: (Optional) 规则所属资源类型
        :param tag: (Optional) 监控项附属信息
        :param tags: (Optional) 多值标签
        :param threshold: (Optional) 阈值
        :param times: (Optional) 连续多少次后报警
        :param updateTime: (Optional) 
        :param uuid: (Optional) 触发条件UUID
        """

        self.calculateUnit = calculateUnit
        self.calculation = calculation
        self.createTime = createTime
        self.deleted = deleted
        self.downSample = downSample
        self.id = id
        self.metric = metric
        self.metricId = metricId
        self.metricName = metricName
        self.noticeLevel = noticeLevel
        self.noticePeriod = noticePeriod
        self.operation = operation
        self.period = period
        self.ruleType = ruleType
        self.serviceCode = serviceCode
        self.tag = tag
        self.tags = tags
        self.threshold = threshold
        self.times = times
        self.updateTime = updateTime
        self.uuid = uuid
