import requests
import json

def getCIcount(): #Error when processing request - null
    url = "http://10.3.1.220:443/api/cmdb/ci/count/all"
    headers = {"authtoken":"7C6702E0-321E-417D-BF35-8DD79B1BE8FD"}
    data = {'OPERATION_NAME' : 'read','format' : 'json'}
    response = requests.get(url,headers=headers,data=data,verify=False)
    return response

def getAsset():
    url = "http://10.3.1.220:443/api/v3/assets/89104"
    headers = {"authtoken":"7C6702E0-321E-417D-BF35-8DD79B1BE8FD"}
    response = requests.get(url,headers=headers,verify=False)
    return response

ck = getAsset()
asset = json.loads(ck.text)

def getMetainfo(id):
    url = "http://10.3.1.220:443/api/v3/assets/metainfo"
    headers = {"authtoken":"7C6702E0-321E-417D-BF35-8DD79B1BE8FD"}
    input_data1 = '''{
    "template": {
        "id": "'''
    input_data2 = '''"
        }
    }'''

    input_data = input_data1 + id + input_data2
    params = {'input_data': input_data}
    response = requests.get(url,headers=headers,params=params,verify=False)
    asset = json.loads(response.text)
    asset = asset["metainfo"]
    return asset


# x: how many assets to get, y: starting index, returns list of assets
def getAssets(x, y=1): #can get maximum 100 assets
    url = "http://10.3.1.220:443/api/v3/assets"
    headers = {"authtoken":"7C6702E0-321E-417D-BF35-8DD79B1BE8FD"}
    i1 = '''{
        "list_info": {
            "row_count": '''
    i2 = ''',
            "start_index": '''
    i3 = ''',
            "sort_field": "id",
            "sort_order": "asc",
            "get_total_count": true
        }
    }'''
    input_data = i1 + str(x) + i2 + str(y) + i3
    params = {'input_data': input_data}
    response = requests.get(url,headers=headers,params=params,verify=False)
    assets = json.loads(response.text)
    assets = assets["assets"]
    return assets

# x: how many assets to get, y: starting index, returns list of assets
def getAssetsResponse(x, y=1): #can get maximum 100 assets
    url = "http://10.3.1.220:443/api/v3/assets"
    headers = {"authtoken":"7C6702E0-321E-417D-BF35-8DD79B1BE8FD"}
    i1 = '''{
        "list_info": {
            "row_count": '''
    i2 = ''',
            "start_index": '''
    i3 = ''',
            "sort_field": "id",
            "sort_order": "asc",
            "get_total_count": true
        }
    }'''
    input_data = i1 + str(x) + i2 + str(y) + i3
    params = {'input_data': input_data}
    response = requests.get(url,headers=headers,params=params,verify=False)
    return response


#returns all assets in a dict
def allAssets():
    response = getAssetsResponse(100)
    response_dict = json.loads(response.text)
    assets_list = []
    assets_list += response_dict["assets"]
    count = 100
    print(response_dict['list_info'])
    print(len(assets_list))
    while response_dict['list_info']['has_more_rows']:
        response = getAssetsResponse(100, count)
        response_dict = json.loads(response.text)
        assets_list += response_dict["assets"]
        print(response_dict['list_info'])
        print(len(assets_list))
        count += 100

    return assets_list


def getWorkstations(x, y=0):
    url = "http://10.3.1.220:443/api/v3/workstations"
    headers = {"authtoken":"7C6702E0-321E-417D-BF35-8DD79B1BE8FD"}
    list_info = {
        "list_info": {
            "row_count": x,
            "start_index": y,
            "sort_field": "id",
            "sort_order": "asc",
            "get_total_count": True
        }
    }
    params = {'input_data': json.dumps(list_info)}
    response = requests.get(url,headers=headers,params=params,verify=False)
    return response


def AllWorkstations():
    res = getWorkstations(100)
    res_dict = json.loads(res.text)
    workstations = []
    workstations += res_dict["workstations"]
    count = 100
    print(res_dict["list_info"])
    print(len(workstations))
    while res_dict["list_info"]["has_more_rows"]:
        res = getWorkstations(100, count)
        res_dict = json.loads(res.text)
        workstations += res_dict["workstations"]
        print(res_dict["list_info"])
        print(len(workstations))
        count += 100

    return workstations


#takes in a dict of assets, prints each asset on a new line
def listAssets(assets):
    count = 0
    for item in assets:
        if item["user"]:
            print(count, item["product_type"]['name'], ":", item["product"]["name"], "-", item["name"], "-", item["user"]["name"])
        else:
            print(count, item["product_type"]['name'], item["product"]["name"], "-", item["name"], "-", item["user"])

        count += 1

#takes in a dict of assets, returns a dict of all products
def getAllProductNames(assets):
    productNames = {}
    for item in assets:
        if item["product_type"]["name"] not in productNames:
            productNames[item["product_type"]["name"]] = []

        if item["product"]["name"] not in productNames[item["product_type"]["name"]]:
            productNames[item["product_type"]["name"]].append(item["product"]["name"])

    return productNames

#takes in a dict of assets, returns a dict of all products with IDs
def getAllProductIDs(assets):
    products = {}
    for item in assets:
        if item["product_type"]["name"] not in products:
            products[item["product_type"]["name"]] = []

        if {item["product"]["name"]:item["product"]["product_type"]["id"]} not in products[item["product_type"]["name"]]:
            products[item["product_type"]["name"]].append({item["product"]["name"]:item["product"]["product_type"]["id"]})
            

    return products

#takes in dict of product names and print them in a readable format 
def ppNames(names):
    for cat in names:
        print(cat)
        for item in names[cat]:
            print(" | " + item)


def ppDict(input, depth = 0):
    tabs = " |" * depth
    if input == None:
        print(tabs + " None")
    elif type(input) is dict:
        for key in input:
            print(tabs + " " + key)
            ppDict(input[key], depth + 1)
    
    elif type(input) is list:
        for item in input:
            ppDict(item, depth + 1)

    else:
        print(tabs + " " + str(input))


def exportJSON(data, name):
    with open(name + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

        
laptop = getAssets(1, 0)
laptopInfo = getMetainfo(laptop[0]["product"]["product_type"]["id"])
laptop2 = getAssets(1, 1)
laptopInfo2 = getMetainfo(laptop[0]["product"]["product_type"]["id"])
phone = getAssets(1, 655)
phoneInfo = getMetainfo(phone[0]["product"]["product_type"]["id"])



def testAdd():
    url = "http://10.3.1.220:443/api/v3/assets"
    headers = {"authtoken":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"}
    input_data = '''{
        "asset": {
        "total_cost": "0.00",
        "ip_addresses": "",
        "primary_ip": null,
        "org_serial_number": "FK1D9GZDN72J",
        "description": "",
        "type": {
            "name": "Asset",
            "id": "1"
        },
        "manufacturer": "Apple",
        "acquisition_date": null,
        "ci_default_fields": {
            "udf_pickref_1": null
        },
        "current_cost": null,
        "vendor": null,
        "id": "1694",
        "purchase_cost": "0.00",
        "state": {
            "is_scan_required": true,
            "name": "In Use",
            "id": "2",
            "is_ownership_mandatory": true
        },
        "department": {
            "site": null,
            "name": "Inspection",
            "id": "13"
        },
        "barcode": null,
        "product_depreciation": null,
        "depreciation": null,
        "operational_cost": null,
        "loan_end": null,
        "asset_tag": "",
        "product": {
            "part_no": null,
            "product_type": {
                "id": "14"
            },
            "name": "iPhone 11",
            "computer_group": null,
            "id": "15",
            "type": {
                "id": "1"
            },
            "category": {
                "id": "2"
            },
            "manufacturer": "Apple"
        },
        "expiry_date": null,
        "used_by_asset": null,
        "sys_description": null,
        "warranty_expiry": null,
        "is_personal": false,
        "part_no": null,
        "site": null,
        "product_type": {
            "internal_name": "Smart Phone",
            "name": "iPhone",
            "id": "14",
            "type": {
                "name": "Asset",
                "id": "1"
            }
        },
        "name": "Angad Rooprai iPhone",
        "udf_fields": {
            "udf_sline_301": "",
            "udf_sline_4": "356573080287671",
            "udf_sline_5": "",
            "udf_sline_6": "16472815143",
            "udf_sline_3": ""
        },
        "discovered_serial_number": null,
        "location": "-",
        "is_loaned": false,
        "region": null,
        "user": {
            "email_id": "arooprai@tssa.org",
            "phone": null,
            "name": "Angad Rooprai",
            "mobile": "+1 647-281-5143",
            "profile_pic": {
                "content-url": "/images/default-profile-pic2.svg",
                "name": "default-profile-pic2.svg"
            },
            "is_vipuser": false,
            "id": "841",
            "department": {
                "site": null,
                "name": "Inspection",
                "id": 13
            }
        }
    }'''
    data = {'input_data': input_data}
    response = requests.post(url,headers=headers,data=data,verify=False)

    return response

def getAllProducts():
    url = "http://10.3.1.220:443/api/v3/product_types"
    headers = {"authtoken":"7C6702E0-321E-417D-BF35-8DD79B1BE8FD"}
    input_data = '''{
        "list_info": {
            "row_count": 20,
            "start_index": 0,
            "sort_field": "id",
            "sort_order": "asc",
            "get_total_count": true
        }
    }'''
    params = {'input_data': input_data}
    response = requests.get(url,headers=headers,params=params,verify=False)
    return response



def updateWorkstation():
    url = "http://10.3.1.220:443/api/v3/workstations/1"
    headers = {"authtoken":"7C6702E0-321E-417D-BF35-8DD79B1BE8FD"}

    item_dict = {
        "workstation": {
            "workstation_udf_fields": {
            "udf_sline_601": "super idol 2"
            }
        }
    }

    item_json = json.dumps(item_dict)

    data = {'input_data': item_json}
    response = requests.put(url,headers=headers,data=data,verify=False)
    return response


def allWorkstations():
    url = "http://10.3.1.220:443/api/v3/workstations"
    headers = {"authtoken":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"}
    input_data = {
        "list_info": {
            "row_count": 5,
            "start_index": 0,
            "sort_field": "id",
            "sort_order": "asc",
            "get_total_count": true
        }
    }
    params = {'input_data': input_data}
    response = requests.get(url,headers=headers,params=params,verify=False)

# update = updateAsset().text
# update = json.loads(update)