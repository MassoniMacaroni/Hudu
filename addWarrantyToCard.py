import requests
import json


# your hudu api key
hudu_api_key = ""
# like your company https://domain/api/v1/
api_url = ""
# Name of the workstation asset layout
workstationALName = "Managed Workstation"
# the field name for warranty expiry date
fieldNameWarrantyExpiry = "Warranty Expiration Date"

def getAssetLayoutDetails():
    headers = {"x-api-key": hudu_api_key}
    response = requests.get(api_url + "asset_layouts?name=" + workstationALName, headers=headers)
    result = response.json()
    id = next((layout["id"] for layout in result["asset_layouts"] if layout["name"] == workstationALName), None)
    return str(id)
    
        
def getAssets(assetLayoutId):
    page_num = 0  
    processed_assets = []

    while True:  # Use an infinite loop and break when no more assets are pulled
        headers = {"x-api-key": hudu_api_key}
        response = requests.get(api_url + "assets", params={"asset_layout_id": assetLayoutId, "page": page_num, "page_size": 100}, headers=headers)
        pulledAssets = response.json().get("assets", [])  # Directly get the assets list; provide default empty list
        
        # Break the loop if pulledAssets is empty, indicating no more assets to process
        if not pulledAssets:
            break
        
        for asset in pulledAssets:
            if not asset.get("cards"):  # Use .get() for safer access
                continue
            
            warranty_expiration_date = None
            
            for card in asset["cards"]:
                if card.get("integrator_name") == "cw_manage":
                    warranty_expiration_date = card.get("data", {}).get("warrantyExpirationDate")
                    if warranty_expiration_date:
                        break  # Found the warranty expiration date
            
            if not warranty_expiration_date:
                continue  # Skip asset if no warranty expiration date found
            
            # Now, we have an asset with warranty expiration date
            asset_id = asset["id"]
            company_id = asset["company_id"]
            
            processed_assets.append({
                "asset_id": asset_id,
                "company_id": company_id,
                "warranty_expiration_date": warranty_expiration_date
            })
        
        page_num += 1  # Go to the next page

    return processed_assets


def updateWarrantyExpiry(asset_id,company_id,warranty_expiration_date):
    payload = {"asset": {"custom_fields": [{fieldNameWarrantyExpiry: warranty_expiration_date}]}}
    headers = {"x-api-key": hudu_api_key, "Content-Type": "application/json"} 
    url = f"{api_url}companies/{company_id}/assets/{asset_id}" 
    response = requests.put(url, json=payload, headers=headers) 
    # You can uncomment the below for testing
    # print(json.dumps(payload))  # To see what's being sent
    # # print(url)
    # # print(response.status_code)
    # try:
    #     print(response.json())
    # except ValueError:  # In case the response isn't JSON or is empty
    #     print(response.text)



assetLayoutId = getAssetLayoutDetails()
assetsWExpiry = getAssets(assetLayoutId)
for i in range(len(assetsWExpiry)):
    assetId = str(assetsWExpiry[i]['asset_id'])
    assetCompanyId = str(assetsWExpiry[i]['company_id'])
    assetWarrantyExpiration = str(assetsWExpiry[i]['warranty_expiration_date'])
    #print(assetId,assetCompanyId,assetWarrantyExpiration)
    updateWarrantyExpiry(assetId,assetCompanyId,assetWarrantyExpiration)


