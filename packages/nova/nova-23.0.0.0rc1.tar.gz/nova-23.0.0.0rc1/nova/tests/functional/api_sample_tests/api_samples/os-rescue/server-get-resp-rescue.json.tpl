{
    "server": {
        "accessIPv4": "%(access_ip_v4)s",
        "accessIPv6": "%(access_ip_v6)s",
        "addresses": {
            "private": [
                {
                    "addr": "%(ip)s",
                    "version": 4,
                    "OS-EXT-IPS-MAC:mac_addr": "00:0c:29:0d:11:74",
                    "OS-EXT-IPS:type": "fixed"
                }
            ]
        },
        "created": "%(isotime)s",
        "flavor": {
            "id": "1",
            "links": [
                {
                    "href": "%(compute_endpoint)s/flavors/1",
                    "rel": "bookmark"
                }
            ]
        },
        "hostId": "%(hostid)s",
        "id": "%(id)s",
        "image": {
            "id": "%(uuid)s",
            "links": [
                {
                    "href": "%(compute_endpoint)s/images/%(uuid)s",
                    "rel": "bookmark"
                }
            ]
        },
        "links": [
            {
                "href": "%(versioned_compute_endpoint)s/servers/%(id)s",
                "rel": "self"
            },
            {
                "href": "%(compute_endpoint)s/servers/%(id)s",
                "rel": "bookmark"
            }
        ],
        "metadata": {
            "My Server Name": "Apache1"
        },
        "name": "new-server-test",
        "status": "%(status)s",
        "tenant_id": "6f70656e737461636b20342065766572",
        "updated": "%(isotime)s",
        "user_id": "fake",
        "key_name": null,
        "config_drive": "%(cdrive)s",
        "OS-DCF:diskConfig": "AUTO",
        "OS-EXT-AZ:availability_zone": "us-west",
        "OS-EXT-STS:power_state": 4,
        "OS-EXT-STS:task_state": null,
        "OS-EXT-STS:vm_state": "rescued",
        "os-extended-volumes:volumes_attached": [],
        "OS-SRV-USG:launched_at": "%(strtime)s",
        "OS-SRV-USG:terminated_at": null,
        "security_groups": [
            {
                "name": "default"
            }
        ]
    }
}
