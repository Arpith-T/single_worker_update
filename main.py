import time
import requests
import json
import os

tenant_name = "az-manual"


# tenant_name = os.getenv("AZURE_TENANT")


def ziat001_trm_token():
    url = "https://ziat001.authentication.eu20.hana.ondemand.com/oauth/token?grant_type=client_credentials"

    payload = {}
    headers = {
        'Authorization': 'Basic c2ItaXQhYjIxMjpkNTU5ZjIwNi01ZDgyLTRlZDUtODE4OC1jNjlmMDJkZjBmNGQkTW42SXlWNkRWQkgyX08xeVpMMHRmdXVHQXNnTC1jNFVKTkNocEE3N2FVTT0='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    res_in_dict = json.loads(response.text)
    return res_in_dict["access_token"]


az_trm_token = ziat001_trm_token()


def force_worker_update():
    url = f"https://it-ziat001-trm.cfapps.eu20.hana.ondemand.com/api/trm/v1/tenant-softwares/tenants?tenantNames={tenant_name}"

    payload = json.dumps({
        "softwareUpdateOperationType": "SCHEDULE",
        "scheduledUtc": "",
        "completeSystem": False,
        "tenants": [
            {
                "tenantId": "az-manual",
                "pin": False
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {az_trm_token}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.json())


def monitor_worker_update():
    import requests
    import json

    url = f"https://it-ziat001-trm.cfapps.eu20.hana.ondemand.com/api/trm/v1/tenant-softwares/tasks?tenantNames={tenant_name} "

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {az_trm_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.json())

    in_progress = response.json()["inProgress"]
    return in_progress


start_time = time.time()
force_worker_update()

while monitor_worker_update() != 0:
    print("\n worker update is in progress")
    time.sleep(30)

end_time = time.time()
total_time_taken = start_time - end_time
print(f"\n{tenant_name} - update got completed in {total_time_taken}")
