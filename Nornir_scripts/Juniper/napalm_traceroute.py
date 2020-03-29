#!/usr/bin/python3
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from typing import Optional
from nornir.core.task import Result, Task
from nornir.core.filter import F

nr = InitNornir(
    inventory={
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        }
    }
)


def napalm_traceroute(
    task: Task,
    dest: str,
    source: Optional[str] = None,
    ttl: Optional[int] = 255,
    timeout: Optional[int] = 2,
    vrf: Optional[str] = None,
) -> Result:

    device = task.host.get_connection("napalm", task.nornir.config)
    result = device.traceroute(
        destination=dest,
        source=source,
        ttl=ttl,
        timeout=timeout,
        vrf=vrf,
    )
    return Result(host=task.host, result=result)

out = nr.filter(F(hostname='10.91.2.4'))
result = out.run(task=napalm_traceroute, dest='8.8.8.8', source='103.231.99.7')
print_result(result)
