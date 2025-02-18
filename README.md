# GCP NGFW Firewall Policy Rule Creator

This Python script automates the creation of firewall rules in Google Cloud using a CSV file as input. It simplifies the process of defining and applying firewall rules to your network, especially when you have a large number of rules to manage.

## Features

* **CSV-driven:** Define firewall rules in a CSV file with clear headers, making it easy to manage and update your rules.
* **Global and Regional Policies:** Supports both global and regional firewall policies.
* **Multiple Secure Tags and Address Groups:** Allows you to specify multiple secure tags and address groups for each rule using comma-separated values enclosed in brackets.
* **Error Handling:** Includes robust error handling to catch common issues like duplicate priorities or invalid formats.
* **Detailed Logging:** Provides clear logging of the processed rows, initial commands, and final commands for debugging and auditing.

## Prerequisites

* **Google Cloud Project:** You need an active Google Cloud project with the necessary permissions to create firewall rules.
* **gcloud CLI:** Make sure you have the gcloud CLI installed and configured with your project.
* **Python 3:** The script requires Python 3 to be installed.

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

2. **Prepare the CSV file:**
Create a CSV file with the following headers:

```
PRIORITY,ACTION,DESCRIPTION,TARGET_SECURE_TAGS,DIRECTION,SRC_IP_RANGES,DEST_IP_RANGES,LAYER4_CONFIGS,ENABLE_LOGGING,DISABLED,SRC_ADDRESS_GROUPS,DEST_ADDRESS_GROUPS
```
* **PRIORITY**: Priority of the rule (lower numbers have higher priority).

* **ACTION**: `allow` or `deny`.

* **DESCRIPTION**: Description of the rule.

* **TARGET_SECURE_TAGS**: Target secure tags (comma-separated in brackets).

* **SRC_SECURE_TAGS**: Source secure tags (comma-separated in brackets).

* **DIRECTION**: `INGRESS` or `EGRESS`.

* **SRC_NETWORKS**: Source networks (comma-separated).

* **SRC_IP_RANGES**: Source IP ranges (comma-separated).

* **DEST_IP_RANGES**: Destination IP ranges (comma-separated).

* **LAYER4_CONFIGS**: Layer 4 configurations (e.g., `tcp:80,tcp:443`).

* **ENABLE_LOGGING**: `TRUE` or `FALSE` to enable logging.

* **DISABLED**: `TRUE` or `FALSE` to disable the rule.

* **SRC_ADDRESS_GROUPS**: Source address groups (comma-separated in brackets).

* **DEST_ADDRESS_GROUPS**: Destination address groups (comma-separated in brackets).

**Example CSV:**
```
PRIORITY,ACTION,DESCRIPTION,TARGET_SECURE_TAGS,DIRECTION,SRC_IP_RANGES,DEST_IP_RANGES,LAYER4_CONFIGS,ENABLE_LOGGING,DISABLED,SRC_ADDRESS_GROUPS,DEST_ADDRESS_GROUPS
1000,allow,allow,"poc/app name/ad,poc/env/prod",INGRESS,10.0.0.0/8,10.0.0.0/16,"tcp:80,tcp:443",TRUE,FALSE,"projects/poc/locations/global/addressGroups/utk-test-app-vm,projects/poc/locations/global/addressGroups/utk-poc-ag",
1001,deny,Deny SSH from public internet,"poc/app name/ad,poc/env/prod",INGRESS,0.0.0.0/0,,tcp:22,FALSE,FALSE,"projects/poc/locations/global/addressGroups/utk-test-app-vm,projects/poc/locations/global/addressGroups/utk-poc-ag",
2000,allow,Allow ICMP from specific IPs,"poc/app name/ad,poc/env/prod",INGRESS,"192.168.1.10,192.168.1.11",,"icmp,tcp,udp:22-30",TRUE,FALSE,"projects/poc/locations/global/addressGroups/utk-test-app-vm,projects/poc/locations/global/addressGroups/utk-poc-ag",
3000,allow,Allow internal database access,"poc/app name/ad,poc/env/prod",EGRESS,,"10.0.0.0/8,10.1.1.1/32",tcp:3306,TRUE,FALSE,,"projects/poc/locations/global/addressGroups/utk-test-app-vm,projects/poc/locations/global/addressGroups/utk-poc-ag"
4000,deny,Deny all other traffic,"poc/app name/ad,poc/env/prod",EGRESS,,0.0.0.0/0,all,FALSE,FALSE,,"projects/poc/locations/global/addressGroups/utk-test-app-vm,projects/poc/locations/global/addressGroups/utk-poc-ag"
```

3. **Run the Script:**
```
python main.py <csv_file> <firewall_policy_name> [--global_policy]
OR
python main.py <csv_file>  #Where the firewall_policy_name is defined in the script
```
* `<csv_file>`: Path to the CSV file.
* `<firewall_policy_name>`: Name of the firewall policy.
* `--global_policy`: (Optional) Use this flag if you are using a global firewall policy.

**Example**
```
python main.py a.csv my-abc-firewall-policy --global_policy

```
**Notes**
* Make sure to replace the default placeholder values in the script with your actual values. (CSV File Name, Policy Name)
* The script assumes that the gcloud CLI is configured correctly with your project.
* If you encounter any issues, check the detailed logging output for debugging information.

* **Contributing**
Contributions are welcome! Feel free to open issues or submit pull requests to improve the script.
```
This README file provides a comprehensive guide to using the script, including its features, prerequisites, usage instructions, and an example. It also encourages contributions and provides information on how to get involved.
```
