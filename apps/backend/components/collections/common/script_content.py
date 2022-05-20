# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-节点管理(BlueKing-BK-NODEMAN) available.
Copyright (C) 2017-2022 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

REACHABLE_SCRIPT_TEMPLATE = """
is_target_reachable () {
    local ip=${1}
    local target_port=$2
    local _port err ret

    if [[ $target_port =~ [0-9]+-[0-9]+ ]]; then
        target_port=$(seq ${target_port//-/ })
    fi
    for _port in $target_port; do
        timeout 5 bash -c ">/dev/tcp/$ip/$_port" 2>/dev/null
        case $? in
            0) return 0 ;;
            1) ret=1 && echo "GSE server connect to proxy($ip:$_port) connection refused" ;;
            ## 超时的情况，只有要一个端口是超时的情况，认定为网络不通，不继续监测
            124) echo "GSE server connect to proxy($ip:$target_port) failed: NETWORK TIMEOUT %(msg)s" && return 124;;
        esac
    done

    return $ret;
}
ret=0
is_target_reachable %(proxy_ip)s %(btsvr_thrift_port)s || ret=$?
is_target_reachable %(proxy_ip)s %(bt_port)s-%(tracker_port)s || ret=$?
exit $ret
"""

INITIALIZE_SCRIPT = """
setup_path="$@"
cd $setup_path
for file in $(ls); do
    if echo $file | grep '.*sh$'; then
        chmod +x $setup_path/${file}
    fi
done
"""
