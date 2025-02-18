import subprocess
import csv
import argparse

# Default placeholder values (replace with your actual values)
DEFAULT_FIREWALL_POLICY = "poc"
DEFAULT_CSV_FILE = "a.csv"

def create_firewall_rule(row, firewall_policy_var, global_policy):
    """Creates a gcloud firewall rule based on a CSV row."""

    priority = row.get('PRIORITY')
    action = row.get('ACTION')
    description = row.get('DESCRIPTION')
    target_secure_tags = row.get('TARGET_SECURE_TAGS')
    src_secure_tags = row.get('SRC_SECURE_TAGS')
    direction = row.get('DIRECTION')
    src_networks = row.get('SRC_NETWORKS')
    src_ip_ranges = row.get('SRC_IP_RANGES')
    dest_ip_ranges = row.get('DEST_IP_RANGES')
    layer4_configs = row.get('LAYER4_CONFIGS')
    enable_logging = row.get('ENABLE_LOGGING')
    disabled = row.get('DISABLED')
    src_address_groups = row.get('SRC_ADDRESS_GROUPS')
    dest_address_groups = row.get('DEST_ADDRESS_GROUPS')

    print(f"Processing row: {row}")

    if not priority or not action or not description:
        print(f"Skipping row due to missing required fields (PRIORITY, ACTION, DESCRIPTION): {row}")
        return

    command = [
        "gcloud", "beta", "compute", "network-firewall-policies", "rules", "create", priority,
        "--action", action,
        "--firewall-policy", firewall_policy_var,
        "--description", description,
        "--global-firewall-policy",
    ]

    print(f"Initial command: {command}")

    if global_policy:
        command.append("--global-firewall-policy")

    # Correctly handle multiple target secure tags (comma-separated in brackets)
    if target_secure_tags:
        tags = target_secure_tags.strip('')  # Remove brackets only
        command.extend(["--target-secure-tags", tags])  # Add all tags at once

    # Correctly handle multiple source secure tags (comma-separated in brackets)
    if src_secure_tags:
        tags = src_secure_tags.strip('')  # Remove brackets only
        command.extend(["--src-secure-tags", tags])  # Add all tags at once

    if direction:
        command.extend(["--direction", direction])

    if src_networks:
        command.extend(["--src-networks", src_networks])

    if src_ip_ranges:
        command.extend(["--src-ip-ranges", src_ip_ranges])

    if dest_ip_ranges:
        command.extend(["--dest-ip-ranges", dest_ip_ranges])

    if layer4_configs:
        command.extend(["--layer4-configs", layer4_configs])

    if enable_logging and enable_logging.lower() == "true":
        command.append("--enable-logging")
    elif enable_logging and enable_logging.lower() == "false":
        command.append("--no-enable-logging")

    if disabled and disabled.lower() == "true":
        command.append("--disabled")
    elif disabled and disabled.lower() == "false":
        command.append("--no-disabled")

    # Correctly handle multiple address groups (comma-separated in brackets)
    if src_address_groups:
        groups = src_address_groups.strip('')  # Remove brackets only
        command.extend(["--src-address-groups", groups])  # Add all groups at once

    if dest_address_groups:
        groups = dest_address_groups.strip('')  # Remove brackets only
        command.extend(["--dest-address-groups", groups])  # Add all groups at once

    print(f"Final command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
        print(f"Firewall rule created successfully: {priority}")
    except subprocess.CalledProcessError as e:
        if "Cannot have rules with the same priorities" in str(e):
            print(f"Error: Firewall rule with priority {priority} already exists.")
        else:
            print(f"Error creating firewall rule: {e}")
        print(f"Command executed: {' '.join(command)}")

def main():
    parser = argparse.ArgumentParser(description="Create gcloud firewall rules from CSV.")
    parser.add_argument("csv_file", nargs='?', default=DEFAULT_CSV_FILE, help="Path to the CSV file.")
    parser.add_argument("firewall_policy_var", nargs='?', default=DEFAULT_FIREWALL_POLICY, help="Name of the firewall policy.")
    parser.add_argument("--global_policy", action="store_true", help="Use global firewall policy.")
    args = parser.parse_args()

    try:
        with open(args.csv_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                create_firewall_rule(row, args.firewall_policy_var, args.global_policy)
    except FileNotFoundError:
        print(f"Error: CSV file not found: {args.csv_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()