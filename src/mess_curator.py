import sys
import subprocess
import xml.etree.ElementTree as ET
import os
import yaml
from tabulate import tabulate
import argparse
import shutil # For file copying
import zipfile # For creating dummy zips
import csv # For CSV output
from pathlib import Path
import re
import urllib.request
import ssl

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

# === Global Debug Flag ===
DEBUG_MODE_ENABLED = False 

def debug_print(message):
    """Prints debug messages only if DEBUG_MODE_ENABLED is True."""
    if DEBUG_MODE_ENABLED:
        print(f"[DEBUG] {message}")

# === Configuration Management ===
CONFIG_FILE = BASE_DIR.parent / "config.yaml"

APP_CONFIG = {
    "mame_executable": "",
    "softlist_rom_sources_dir": "",
    "out_romset_dir": "",
    "mess_ini_path": "",
    "system_softlist_yaml_file": "system_softlist.yml",
    "mess_version": "",
    "mess_xml_file": ""
}

def _load_yaml_file(file_path):
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    except yaml.YAMLError as e:
        print(f"[ERROR] Error loading YAML data from '{file_path}': {e}")
        return {}
    except Exception as e:
        print(f"[ERROR] Unexpected error loading YAML file '{file_path}': {e}")
        return {}

def save_configuration():
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            yaml.dump(APP_CONFIG, f, default_flow_style=False, sort_keys=False)
        debug_print(f"Configuration saved to '{CONFIG_FILE}'.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save configuration to '{CONFIG_FILE}': {e}")
        return False

def load_configuration():
    if not CONFIG_FILE.exists():
        print(f"[ERROR] Config file not found: {CONFIG_FILE}")
        return False

    config_data = _load_yaml_file(CONFIG_FILE)
    if not config_data:
        print(f"[WARNING] '{CONFIG_FILE}' is empty or invalid. Please run the setup wizard or use the 'config' command.")
        return False

    config_dir = CONFIG_FILE.parent

    def resolve_path(val):
        path = Path(val)
        return str(path) if path.is_absolute() else str((config_dir / path).resolve())

    for key in APP_CONFIG:
        if key in config_data:
            value = config_data[key]
            # If it's a path-like value, resolve it
            if isinstance(value, str) and ("\\" in value or "/" in value):
                APP_CONFIG[key] = resolve_path(value)
            else:
                APP_CONFIG[key] = value

    print(f"[INFO] Configuration loaded from '{CONFIG_FILE}'.")
    return True

def run_initial_setup_wizard():
    print("=" * 60)
    print(" MAME MESS Curator Tool - Initial Setup Wizard")
    print("=" * 60)
    print(f"\nConfiguration file '{CONFIG_FILE}' not found.")
    print("Let's set up the necessary paths to get started.")

    temp_config = {}

    while True:
        prompt = "\n[1/4] Please enter the full path to your MAME executable (e.g., C:\\MAME\\mame.exe):\n> "
        path = input(prompt).strip().replace('"', '')
        if os.path.isfile(path) and path.lower().endswith("mame.exe"):
            temp_config["mame_executable"] = path
            break
        print("[!] Invalid path. Please ensure the path points to 'mame.exe' and the file exists.")

    # Auto-detect MAME version from path
    detected_version = "".join(re.findall(r'\d', os.path.basename(os.path.dirname(temp_config["mame_executable"]))))
    if detected_version:
        print(f"\n[INFO] Auto-detected MAME version: {detected_version}")
        temp_config["mess_version"] = detected_version
    else:
        while True:
            prompt = "\n[NEW] Please enter your MAME version number (e.g., 278, 277):\n> "
            version = input(prompt).strip()
            if version.isdigit():
                temp_config["mess_version"] = version
                break
            print("[!] Invalid input. Please enter only the version number.")        

    while True:
        prompt = "\n[2/4] Please enter the path to your MAME 'softlist' ROMs directory:\n      (This is where subfolders like 'nes', 'ekara_cart', etc., are located)\n> "
        path = input(prompt).strip().replace('"', '')
        if os.path.isdir(path):
            temp_config["softlist_rom_sources_dir"] = path
            break
        print("[!] Invalid path. Please ensure the directory exists.")

    while True:
        prompt = "\n[3/4] Please enter the path for the curated output ROMsets:\n      (This directory will be created if it doesn't exist)\n> "
        path = input(prompt).strip().replace('"', '')
        if path:
            temp_config["out_romset_dir"] = path
            break
        print("[!] Path cannot be empty.")

    temp_config["system_softlist_yaml_file"] = "system_softlist.yml"
    print(f"\n[4/4] The generated platform metadata will be saved as '{temp_config['system_softlist_yaml_file']}' in the current directory.")
    
    temp_config["mess_xml_file"] = "mess.xml"

    print("\n" + "=" * 20 + " Configuration Summary " + "=" * 20)
    for key, value in temp_config.items():
        print(f"{key+':':<30} {value}")
    print("=" * 60)

    confirm = input("\nSave this configuration? [Y/n]: ").strip().lower()
    if confirm in ['', 'y', 'yes']:
        for key, value in temp_config.items():
            APP_CONFIG[key] = value
        if save_configuration():
            print(f"\n[SUCCESS] Configuration saved to '{CONFIG_FILE}'. You can now run the tool.")
        else:
            print("\n[FATAL] Could not save configuration. Exiting.")
            sys.exit(1)
    else:
        print("\nSetup cancelled. Exiting.")
        sys.exit(0)

def initialize_application():
    if not load_configuration():
        run_initial_setup_wizard()

        # After wizard, we need to load the config again to populate APP_CONFIG
        if not load_configuration():
            print("[FATAL] Could not load configuration after setup. Exiting.")
            sys.exit(1)
    
    # This function now handles the check, download, and sets the dynamic path
    ensure_mess_xml_exists()

MAME_ALL_MACHINES_XML_CACHE = BASE_DIR.parent / "mame.xml"
MESS_XML_FILE = BASE_DIR.parent / "mess.xml"
MESS_SOFTLIST_XML_FILE = BASE_DIR.parent / "mess-softlist.xml"
MESS_NOSOFTLIST_XML_FILE = BASE_DIR.parent / "mess-nosoftlist.xml"
TMP_SOFTWARE_XML_FILE = BASE_DIR.parent / "tmp_software.xml"

def run_mame_command(args, output_file, use_cache=False): 
    if use_cache and os.path.exists(output_file):
        print(f"[INFO] Using cached XML file: '{output_file}'. Skipping MAME execution.")
        return True

    try:
        cmd = [APP_CONFIG['mame_executable']] + args
        debug_print(f"Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=os.path.dirname(APP_CONFIG['mame_executable'])
        )

        if not result.stdout.strip():
            print(f"[!] MAME output for command '{' '.join(args)}' is empty or invalid.")
            if result.returncode != 0:
                print(f"[!] MAME exited with error code {result.returncode}. Output:\n{result.stdout}")
            return False

        is_xml_output = False
        if "-listxml" in args and (("<mame" in result.stdout) or ("<machine" in result.stdout)):
            is_xml_output = True
        elif "-listsoftware" in args and (("<softwarelist" in result.stdout) or ("<mame" in result.stdout) or ("<softwarelists" in result.stdout)):
            is_xml_output = True
        
        if not is_xml_output:
            print(f"[!] No valid XML content found in MAME output for '{' '.join(args)}'. Raw output snippet:\n{result.stdout[:500]}...")
            if "unknown system" in result.stdout.lower() or "not supported" in result.stdout.lower():
                print(f"[!] Error: System '{args[-1]}' not found or does not support software lists.")
            return False

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        return True

    except FileNotFoundError:
        print(f"[!] Error: MAME executable not found at '{APP_CONFIG['mame_executable']}'")
        return False
    except Exception as e:
        print(f"[!] Exception running MAME command '{' '.join(args)}': {e}")
        return False


def get_parsed_mame_xml_root(xml_filepath):
    if not os.path.exists(xml_filepath):
        print(f"[INFO] Generating '{xml_filepath}' using MAME. This may take a moment...")
        if not run_mame_command(["-listxml"], xml_filepath, use_cache=False): 
            print(f"[ERROR] Failed to generate '{xml_filepath}'.")
            return None
    else: 
        print(f"[INFO] Using existing XML file: '{xml_filepath}'.")

    try:
        tree = ET.parse(xml_filepath)
        return tree.getroot()
    except ET.ParseError as pe:
        print(f"[ERROR] XML parse error for '{xml_filepath}': {pe}. File might be corrupted. Consider deleting it and rerunning.")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error parsing XML file '{xml_filepath}': {e}")
        return None


def get_all_mame_systems_from_xml_file(xml_filepath):
    machines = set()
    root = get_parsed_mame_xml_root(xml_filepath)
    if root is None:
        return machines

    try:
        for machine_element in root.findall("machine"):
            machine_name = machine_element.get("name")
            if machine_name:
                machines.add(machine_name)
        print(f"[INFO] Loaded {len(machines)} machines from '{xml_filepath}'.")
    except Exception as e:
        print(f"[ERROR] Error extracting machines from '{xml_filepath}': {e}")
    return machines


def get_all_mame_systems_by_prefix_from_root(prefix, xml_root):
    matching_systems = []
    debug_print(f"Filtering machines from provided XML by prefix '{prefix}'.")
    try:
        for machine_element in xml_root.findall("machine"):
            machine_name = machine_element.get("name")
            if machine_name and machine_name.startswith(prefix):
                matching_systems.append(machine_name)
        debug_print(f"Found {len(matching_systems)} systems matching prefix '{prefix}'.")
    except Exception as e:
        print(f"[ERROR] Error during fuzzy search from XML root: {e}")
    return matching_systems


def get_machine_details_and_filters_from_root(system_name, source_xml_root): 
    filters = {}
    machine_metadata = {"description": "N/A", "manufacturer": "N/A", "year": "N/A", "status": "N/A", "emulation": "N/A", "sourcefile": "N/A"}
    
    debug_print(f"Extracting details for '{system_name}' from provided XML root.")
    
    try:
        machine_element = source_xml_root.find(f"machine[@name='{system_name}']")
        if machine_element is None:
            debug_print(f"Machine '{system_name}' not found in the provided XML root.")
            return filters, machine_metadata

        machine_metadata["description"] = machine_element.findtext("description", "N/A").strip()
        machine_metadata["manufacturer"] = machine_element.findtext("manufacturer", "N/A").strip()
        machine_metadata["year"] = machine_element.findtext("year", "N/A").strip()
        machine_metadata["sourcefile"] = machine_element.get("sourcefile", "N/A")

        driver_element = machine_element.find("driver")
        if driver_element is not None:
            machine_metadata["status"] = driver_element.get("status", "N/A")
            machine_metadata["emulation"] = driver_element.get("emulation", "N/A")

        found_swlist_tags = False
        for swlist_tag in machine_element.findall("softwarelist"):
            found_swlist_tags = True
            softlist_name = swlist_tag.get("name")
            softlist_filter = swlist_tag.get("filter")
            if softlist_name:
                filters[softlist_name] = softlist_filter.upper() if softlist_filter else None
                debug_print(f"-> Found softlist tag for '{softlist_name}' with filter: '{filters[softlist_name]}'")
            else:
                debug_print(f"-> Found a softwarelist tag without a 'name' attribute in machine '{system_name}'. Skipping.")
        
        if not found_swlist_tags:
            debug_print(f"No <softwarelist> tags found within machine '{system_name}' definition.")

    except Exception as e:
        print(f"[ERROR] Unexpected error extracting details for '{system_name}' from XML root: {e}")
    return filters, machine_metadata


def parse_software_list_from_file(search="", expected_softlist_name=None, system_name="", machine_softlist_filters=None, include_softlist=None, exclude_softlist=None):
    if machine_softlist_filters is None:
        machine_softlist_filters = {}
    if exclude_softlist is None:
        exclude_softlist = []

    try:
        tree = ET.parse(TMP_SOFTWARE_XML_FILE)
        root = tree.getroot()
    except Exception as e:
        print(f"[!] XML parse error for '{TMP_SOFTWARE_XML_FILE}': {e}")
        return []

    results = []
    software_lists_elements = []
    
    if root.tag == "mame":
        software_lists_elements = root.findall("softwarelist")
    elif root.tag == "softwarelist":
        software_lists_elements = [root]
    elif root.tag == "softwarelists":
        software_lists_elements = root.findall("softwarelist")
    else:
        print(f"[!] Unexpected XML root tag: {root.tag}. Expected 'mame', 'softwarelist', or 'softwarelists'.")
        return []

    debug_print(f"Parsing software list XML for '{system_name}'.")
    debug_print(f"Machine-defined filters: {machine_softlist_filters}")

    processed_softlists_count = 0
    for swlist_elem in software_lists_elements:
        current_softlist_name_from_xml = swlist_elem.get("name")
        if not current_softlist_name_from_xml:
            debug_print(f"Skipping softwarelist element without 'name' attribute.")
            continue

        # Filter for inclusion first. If the include list is not empty, the softlist MUST be in it.
        if include_softlist and current_softlist_name_from_xml not in include_softlist:
            debug_print(f"Skipping softlist '{current_softlist_name_from_xml}' as it is not in the --include-softlist.")
            continue

        # Then filter for exclusion
        if current_softlist_name_from_xml in exclude_softlist:
            debug_print(f"Skipping softlist '{current_softlist_name_from_xml}' due to --exclude-softlist.")
            continue

        processed_softlists_count += 1
        debug_print(f"- Processing softlist '{current_softlist_name_from_xml}' from -listsoftware XML.")

        required_compatibility_filter = machine_softlist_filters.get(current_softlist_name_from_xml)
        
        if required_compatibility_filter:
            debug_print(f"  Applying sharedfeat compatibility filter for '{current_softlist_name_from_xml}': '{required_compatibility_filter}'.")
        else:
            debug_print(f"  No specific sharedfeat compatibility filter found for '{current_softlist_name_from_xml}' from machine definition. Software from this list will NOT be sharedfeat-filtered.")

        for sw in swlist_elem.findall("software"):
            swid = sw.get("name", "")
            desc = sw.findtext("description", default="").strip()
            publisher = sw.findtext("publisher", default="N/A").strip()

            is_compatible = True
            if required_compatibility_filter:
                compatibility_feat = sw.find('sharedfeat[@name="compatibility"]')
                if compatibility_feat is not None: # Only perform check if the feature tag exists
                    sharedfeat_values_str = compatibility_feat.get("value", "").upper()
                    sharedfeat_values = [v.strip() for v in sharedfeat_values_str.split(',') if v.strip()]
                    if required_compatibility_filter not in sharedfeat_values:
                        is_compatible = False

            if not is_compatible:
                continue

            if search.lower() in swid.lower() or search.lower() in desc.lower():
                results.append((current_softlist_name_from_xml, system_name, swid, desc, publisher))
    
    if processed_softlists_count == 0:
        debug_print(f"No softwarelist elements found in {TMP_SOFTWARE_XML_FILE}.")

    return results

def output_to_csv_file(headers, data, output_file_path):
    try:
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"\n[SUCCESS] Data successfully written to '{output_file_path}'.")
    except IOError as e:
        print(f"[ERROR] Failed to write to CSV file '{output_file_path}': {e}")

### --- MODIFICATION START --- ###
def output_to_yaml_file(input_systems, all_software_entries, platform_key, platform_name_full, platform_categories, media_type,
                         enable_custom_cmd_per_title, emu_name, default_emu, default_emu_cmd_params,
                         output_file_path=None, softlist_configs_to_add=None, software_configs_to_add=None):
    if softlist_configs_to_add is None:
        softlist_configs_to_add = {}

    if software_configs_to_add is None:
        software_configs_to_add = {}
    
    software_info_by_system = {}

    # <--- CHANGE 1: Go back to using a simple set to collect unique software IDs.
    for softlist_name_xml, sys_name, swid, desc, publisher in all_software_entries:
        if sys_name not in software_info_by_system:
            software_info_by_system[sys_name] = {'softlists_data': {}}
        
        if softlist_name_xml not in software_info_by_system[sys_name]['softlists_data']:
            software_info_by_system[sys_name]['softlists_data'][softlist_name_xml] = set()
        
        software_info_by_system[sys_name]['softlists_data'][softlist_name_xml].add(swid)

    system_list_for_yaml = []
    for sys_name in input_systems:
        system_details = {} 

        if sys_name in software_info_by_system:
            software_lists_array = []
            # <--- CHANGE 2: Create a new dictionary to hold the configs for just this system.
            configs_for_this_system = {} 

            for softlist_name, soft_ids_set in sorted(software_info_by_system[sys_name]['softlists_data'].items()):
                # <--- CHANGE 3: Build the simple software_lists block first.
                softlist_entry = {"softlist_name": softlist_name}
                if soft_ids_set:
                    # The software_id list is now always a simple, sorted list of strings.
                    softlist_entry["software_id"] = sorted(list(soft_ids_set))
                software_lists_array.append(softlist_entry)

                # <--- CHANGE 4: Now, iterate through the software again to find matching custom configs.
                # Check for a default config for this softlist
                if softlist_name in softlist_configs_to_add:
                    if softlist_name not in configs_for_this_system:
                        configs_for_this_system[softlist_name] = {}
                    configs_for_this_system[softlist_name]['_default_config'] = softlist_configs_to_add[softlist_name]

                # Check for per-title configs
                for swid in soft_ids_set:
                    custom_config = software_configs_to_add.get(softlist_name, {}).get(swid)
                    if custom_config:
                        if softlist_name not in configs_for_this_system:
                            configs_for_this_system[softlist_name] = {}
                        configs_for_this_system[softlist_name][swid] = custom_config
            
            if software_lists_array:
                system_details["software_lists"] = software_lists_array
            
            # <--- CHANGE 5: If we found any configs, add the whole software_configs block.
            if configs_for_this_system:
                # Create a new, sorted dictionary
                sorted_configs = {}
                # First, sort the softlist names (e.g., coco_cart, coco_flop)
                for softlist_name in sorted(configs_for_this_system.keys()):
                    sorted_configs[softlist_name] = {}
                    softlist_content = configs_for_this_system[softlist_name]
                    
                    # Inside each softlist, sort the software IDs, ensuring '_default_config' is always first
                    # The key function here sorts '_default_config' before any other string.
                    for swid in sorted(softlist_content.keys(), key=lambda k: (k != '_default_config', k)):
                        sorted_configs[softlist_name][swid] = softlist_content[swid]

                system_details["software_configs"] = sorted_configs
        
        if system_details:
            system_list_for_yaml.append({sys_name: system_details})
        else:
            system_list_for_yaml.append(sys_name)
            print(f"[INFO] No detailed info (software_lists or software_id) for system '{sys_name}'. Will be listed as a simple string in YAML.")
### --- MODIFICATION END --- ###

    new_platform_entry = {
        "platform": {
            "name": platform_name_full
        }
    }
    
    if platform_categories:
        new_platform_entry["platform_category"] = platform_categories

    new_platform_entry["media_type"] = media_type
    new_platform_entry["enable_custom_command_line_param_per_software_id"] = enable_custom_cmd_per_title

    if emu_name:
        emulator_details = {"name": emu_name}
        emulator_details["default_emulator"] = default_emu
        if default_emu_cmd_params:
            emulator_details["default_command_line_parameters"] = default_emu_cmd_params
        new_platform_entry["emulator"] = emulator_details

    new_platform_entry["system"] = system_list_for_yaml

    target_file = output_file_path or APP_CONFIG['system_softlist_yaml_file']
    existing_data = _load_yaml_file(target_file)
    existing_data[platform_key] = new_platform_entry
    
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            yaml.dump(existing_data, f, default_flow_style=False, sort_keys=False)
        print(f"\nSuccessfully generated/updated '{target_file}' with platform '{platform_key}'.")
        print("\n--- Current YAML content for this platform ---")
        print(yaml.dump({platform_key: new_platform_entry}, default_flow_style=False, sort_keys=False))
        print("---------------------------------------------")
    except Exception as e:
        print(f"[ERROR] Failed to write YAML to '{target_file}': {e}")


def update_platform_metadata_only(platform_key, platform_name_full, platform_categories, media_type,
                                  enable_custom_cmd_per_title, emu_name, default_emu, default_emu_cmd_params,
                                  output_file_path, **kwargs):
    """Updates only the metadata of an existing platform entry in the YAML, leaving the system list untouched."""
    print(f"[INFO] Starting metadata-only update for platform '{platform_key}' in '{output_file_path}'.")
    
    existing_data = _load_yaml_file(output_file_path)
    if platform_key not in existing_data:
        print(f"[ERROR] Platform key '{platform_key}' not found in '{output_file_path}'. Cannot update metadata.")
        return
        
    platform_entry = existing_data[platform_key]
    
    # Update platform info
    platform_entry['platform'] = {'name': platform_name_full}
    if platform_categories:
        platform_entry['platform_category'] = platform_categories
    elif 'platform_category' in platform_entry:
        del platform_entry['platform_category']
        
    platform_entry['media_type'] = media_type
    platform_entry['enable_custom_command_line_param_per_software_id'] = enable_custom_cmd_per_title
    
    # Update emulator info
    if emu_name:
        if 'emulator' not in platform_entry:
            platform_entry['emulator'] = {}
        platform_entry['emulator']['name'] = emu_name
        platform_entry['emulator']['default_emulator'] = default_emu
        if default_emu_cmd_params:
            platform_entry['emulator']['default_command_line_parameters'] = default_emu_cmd_params
    elif 'emulator' in platform_entry:
        del platform_entry['emulator']
        
    # Save the modified data back to the file
    try:
        with open(output_file_path, "w", encoding="utf-8") as f:
            yaml.dump(existing_data, f, default_flow_style=False, sort_keys=False)
        print(f"[SUCCESS] Metadata for platform '{platform_key}' updated in '{output_file_path}'.")
    except Exception as e:
        print(f"[ERROR] Failed to save updated YAML: {e}")

# === ROM Copying Functions ===

def _copy_single_rom(softid, softlist_name_for_copy, system_name, platform_key, create_dummy=False, dry_run=False):
    """
    Copies a single software ROM or creates a dummy zip if not found.
    """
    copied = 0
    missing = 0
    
    softlist_rom_dir = APP_CONFIG['softlist_rom_sources_dir']
    out_romset_dir = APP_CONFIG['out_romset_dir']
    
    rom_src_path = os.path.join(softlist_rom_dir, softlist_name_for_copy, f"{softid}.zip")
    rom_dst_dir = os.path.join(out_romset_dir, platform_key, system_name, softlist_name_for_copy)
    rom_dst_path = os.path.join(rom_dst_dir, f"{softid}.zip")

    if not dry_run:
        os.makedirs(rom_dst_dir, exist_ok=True)

    # If forced dummy creation is ON, OR if the source file doesn't exist, create a dummy.
    if create_dummy or not os.path.exists(rom_src_path):
        if create_dummy:
            # New message for when dummy creation is forced by the user flag.
            print(f"[○] Placeholder (Dummy) Zip requested: Creating placeholder for {softid}.zip at {rom_dst_path}")
        else:
            # This is the original "missing file" message.
            print(f"[✗] Missing ROM: {softid}.zip from '{softlist_name_for_copy}'. Creating placeholder zip at {rom_dst_path}")
        
        _create_dummy_zip_for_rom(rom_dst_path, softid, dry_run=dry_run)
        missing = 1 # We use the 'missing' counter to track all created dummies.
    else:
        # This block only runs if create_dummy is False AND the file exists.
        try:
            print(f"[✓] Copied ROM: {softid}.zip → {rom_dst_path}")
            if not dry_run:
                shutil.copy2(rom_src_path, rom_dst_path)
            copied = 1
        except Exception as e:
            print(f"[ERROR] Failed to copy {softid}.zip from {rom_src_path} to {rom_dst_path}: {e}")
            _create_dummy_zip_for_rom(rom_dst_path, softid)
            missing = 1
    
    return copied, missing

def _create_dummy_zip_for_rom(zip_path, softid, dry_run=False):
    """Creates an empty zip file for a specific software ID."""
    if not dry_run:
        try:
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                pass
        except Exception as e:
            print(f"[ERROR] Failed to create dummy zip {softid}.zip at {zip_path}: {e}")

def _create_dummy_zip_for_system(system_name, platform_key, dry_run=False):
    """Creates an empty zip file for a standalone system (no software_id specified)."""
    out_romset_dir = APP_CONFIG['out_romset_dir']
    dst_dir = os.path.join(out_romset_dir, platform_key, system_name)
    os.makedirs(dst_dir, exist_ok=True)
    zip_path = os.path.join(dst_dir, f"{system_name}.zip")

    print(f"[○] Created empty zip for standalone system: {zip_path}")

    if not dry_run:
        try:
            os.makedirs(dst_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                pass
            return 1
        except Exception as e:
            print(f"[ERROR] Failed to create empty zip for system {system_name} at {zip_path}: {e}")
            return 0
            
    return 1 # In a dry run, we simulate success

def perform_rom_copy_operation(args):
    """
    Parses the system_softlist.yml file and copies/creates ROM zips based on its content.
    """
    print(f"\n===== Starting ROM Copy Operation =====")
    if args.dry_run:
        print("********** DRY RUN MODE ENABLED **********")
        print("*** No files or directories will be created or modified. ***")

    print(f"Source MAME Softlist ROMs: {APP_CONFIG['softlist_rom_sources_dir']}")
    print(f"Destination Curated ROMset: {APP_CONFIG['out_romset_dir']}")

    input_file = args.input_file or APP_CONFIG['system_softlist_yaml_file']
    system_softlist_data = _load_yaml_file(input_file)
    
    if not system_softlist_data:
        print(f"[ERROR] No data found in '{input_file}'. Nothing to copy.")
        return
    
    platforms_to_process = {}
    if args.platform_key:
        if args.platform_key in system_softlist_data:
            print(f"[INFO] Filtering copy operation for platform key: '{args.platform_key}'")
            platforms_to_process[args.platform_key] = system_softlist_data[args.platform_key]
        else:
            print(f"[ERROR] Platform key '{args.platform_key}' not found in '{input_file}'. Nothing to copy.")
            print(f"Available platforms are: {', '.join(system_softlist_data.keys())}")
            return
    else:
        print("[INFO] No platform key specified. Processing all platforms.")
        platforms_to_process = system_softlist_data    

    total_systems_processed = 0
    total_software_copied = 0
    total_software_missing = 0
    total_empty_system_zips = 0
    missing_roms_summary = [] # New list to track missing ROMs

    for platform_key, platform_data in platforms_to_process.items():
        platform_name = platform_data.get("platform", {}).get("name", platform_key)
        media_type = platform_data.get("media_type", "unknown")
        systems_in_platform = platform_data.get("system", [])

        print(f"\n[>>>] Processing Platform: '{platform_name}' (Key: '{platform_key}', Media: '{media_type}')")

        for system_entry in systems_in_platform:
            total_systems_processed += 1
            if isinstance(system_entry, str):
                system_name = system_entry
                print(f"  [>] Processing standalone system: '{system_name}'")
                total_empty_system_zips += _create_dummy_zip_for_system(system_name, platform_key, dry_run=args.dry_run)
            elif isinstance(system_entry, dict):
                for system_name, details in system_entry.items():
                    print(f"  [>] Processing system with details: '{system_name}'")
                    
                    software_lists_for_system = details.get("software_lists", [])
                    
                    if not software_lists_for_system:
                        print(f"  [INFO]   No 'software_lists' found in YAML for system '{system_name}'. Creating dummy zip for system.")
                        total_empty_system_zips += _create_dummy_zip_for_system(system_name, platform_key)
                        continue

                    for softlist_detail in software_lists_for_system:
                        softlist_name_for_copy = softlist_detail.get("softlist_name")
                        software_ids_for_softlist = softlist_detail.get("software_id", [])

                        if not softlist_name_for_copy:
                            print(f"[ERROR]   Softlist entry for '{system_name}' missing 'softlist_name'. Cannot copy ROMs for this entry.")
                            continue

                        if not software_ids_for_softlist:
                            print(f"  [INFO]   No 'software_id's listed for softlist '{softlist_name_for_copy}' under system '{system_name}'. No ROMs to copy for this specific softlist.")
                            continue

                        print(f"  [INFO]   Copying ROMs from softlist '{softlist_name_for_copy}' for system '{system_name}'.")
                        
                        ### --- MODIFICATION START --- ###
                        # This loop now handles both simple strings and dictionaries in the `software_id` list.
                        for software_entry in software_ids_for_softlist:
                            swid = ""
                            if isinstance(software_entry, str):
                                swid = software_entry
                            elif isinstance(software_entry, dict) and 'id' in software_entry:
                                swid = software_entry['id']
                            
                            if swid:
                                copied, missing = _copy_single_rom(swid, softlist_name_for_copy, system_name, platform_key, args.create_placeholder_zip, dry_run=args.dry_run)
                                total_software_copied += copied
                                total_software_missing += missing
                                if missing > 0:
                                    missing_roms_summary.append([swid, softlist_name_for_copy, system_name, platform_key])
                            else:
                                print(f"[WARNING]   Skipping invalid software entry in YAML for '{softlist_name_for_copy}': {software_entry}")
                        ### --- MODIFICATION END --- ###
            else:
                print(f"[WARNING] Invalid system entry type in YAML: {system_entry}. Skipping.")

    print(f"\n===== ROM Copy Operation Summary =====")
    print(f"  Total Platforms Processed: {len(platforms_to_process)}")
    print(f"  Total Systems Processed: {total_systems_processed}")
    print(f"  Total Software ROMs Copied: {total_software_copied}")
    print(f"  Total Software ROMs Missing (Placeholder (Dummy) Zip Created): {total_software_missing}")
    print(f"  Total Empty System Zips Created: {total_empty_system_zips}")
    print(f"======================================")
    
    if missing_roms_summary:
        print("\n===== Missing ROMs Summary =====")
        headers = ["Software ID", "From Softlist", "For System", "In Platform"]
        print(tabulate(sorted(missing_roms_summary), headers=headers, tablefmt="github"))
        print(f"==============================")

def perform_mame_search_and_output(systems_to_process, search_term, output_format, platform_key, platform_name_full, platform_categories, media_type, 
                                   enable_custom_cmd_per_title, emu_name, default_emu, default_emu_cmd_params, 
                                   output_file_path, driver_status_filter=None, emulation_status_filter=None, 
                                   show_systems_only=False, show_extra_info=False, source_xml_root=None, sort_by=None, search_mode=None,
                                   include_softlist=None, exclude_softlist=None, softlist_configs_to_add=None, software_configs_to_add=None):
    """
    Performs the MAME listsoftware search and outputs results as table or YAML.
    """
    if include_softlist is None:
        include_softlist = []    
    if exclude_softlist is None:
        exclude_softlist = []
    all_software_entries_for_yaml_processing = []
    
    processed_system_info = {} 

    if not systems_to_process:
        print("[ERROR] No systems were determined for processing. Please check your arguments.")
        sys.exit(1)

    total_systems = len(systems_to_process)
    for i, current_system in enumerate(systems_to_process, 1):
        print(f"\n--- Processing system: ({i}/{total_systems}) {current_system} ---")
        
        machine_softlist_filters, machine_metadata = get_machine_details_and_filters_from_root(current_system, source_xml_root)
        
        if driver_status_filter and machine_metadata["status"] != driver_status_filter:
            print(f"[INFO] Skipping system '{current_system}': Driver status '{machine_metadata['status']}' does not match required '{driver_status_filter}'.")
            continue
        if emulation_status_filter and machine_metadata["emulation"] != emulation_status_filter:
            print(f"[INFO] Skipping system '{current_system}': Emulation status '{machine_metadata['emulation']}' does not match required '{emulation_status_filter}'.")
            continue
        
        processed_system_info[current_system] = {
            'machine_metadata': machine_metadata,
            'software_entries': []
        }

        listsoftware_succeeded = run_mame_command(["-listsoftware", current_system], TMP_SOFTWARE_XML_FILE)

        entries_from_parse_func = []
        if listsoftware_succeeded:
            entries_from_parse_func = parse_software_list_from_file(
                search=search_term,
                system_name=current_system,
                machine_softlist_filters=machine_softlist_filters,
                include_softlist=include_softlist,
                exclude_softlist=exclude_softlist
            )
            if entries_from_parse_func:
                processed_system_info[current_system]['software_entries'].extend(entries_from_parse_func)
            else:
                print(f"[INFO] No software entries found/matched for system '{current_system}' after parsing and filtering.")
        else:
            print(f"[INFO] MAME did not provide software list for '{current_system}' or command failed. It will be represented in the table and YAML.")

        if os.path.exists(TMP_SOFTWARE_XML_FILE):
            os.remove(TMP_SOFTWARE_XML_FILE)


    print("\n--- Finished processing all systems ---")

    for sys_name, sys_data in processed_system_info.items():
        all_software_entries_for_yaml_processing.extend(sys_data['software_entries'])

    if systems_to_process:
        if output_format == "table" or output_format == "csv":
            table_display_data = []
            
            headers = ["System"]
            if show_extra_info:
                headers.extend(["Description", "Manufacturer", "Year"])
            headers.extend(["Softlist", "Software ID", "Title"])
            if show_extra_info:
                headers.append("Publisher")
            headers.extend(["Driver Status", "Emulation Status"])
            if show_extra_info or search_mode == 'by-sourcefile':
                headers.append("Source File")

            for sys_name in systems_to_process:
                system_data_info = processed_system_info.get(sys_name)
                
                if system_data_info:
                    machine_metadata = system_data_info['machine_metadata']
                    driver_status = machine_metadata['status']
                    emulation_status = machine_metadata['emulation']
                    machine_description = machine_metadata['description']
                    machine_manufacturer = machine_metadata['manufacturer']
                    machine_year = machine_metadata['year']
                    source_file = machine_metadata['sourcefile']

                    if show_systems_only:
                        row = [sys_name]
                        if show_extra_info:
                            row.extend([machine_description, machine_manufacturer, machine_year])
                        row.extend(["N/A", "N/A", machine_description])
                        if show_extra_info:
                            row.append("N/A")
                        row.extend([driver_status, emulation_status])
                        if show_extra_info or search_mode == 'by-sourcefile':
                            row.append(source_file)
                        table_display_data.append(row)
                    elif system_data_info['software_entries']:
                        for softlist_name, _, swid, desc, publisher in system_data_info['software_entries']:
                            row = [sys_name] 
                            if show_extra_info:
                                row.extend([machine_description, machine_manufacturer, machine_year])
                            row.extend([softlist_name, swid, desc])
                            if show_extra_info:
                                row.append(publisher)
                            row.extend([driver_status, emulation_status])
                            if show_extra_info or search_mode == 'by-sourcefile':
                                row.append(source_file)
                            table_display_data.append(row)
                    else:
                        row = [sys_name]
                        if show_extra_info:
                            row.extend([machine_description, machine_manufacturer, machine_year])
                        row.extend(["N/A", "N/A", machine_description])
                        if show_extra_info:
                            row.append("N/A")
                        row.extend([driver_status, emulation_status])
                        if show_extra_info or search_mode == 'by-sourcefile':
                            row.append(source_file)
                        table_display_data.append(row)
            
            if sort_by and table_display_data:
                key_to_header = {
                    'system_name': 'System', 'system_desc': 'Description', 'manufacturer': 'Manufacturer', 'year': 'Year',
                    'softlist': 'Softlist', 'software_id': 'Software ID', 'title': 'Title',
                    'publisher': 'Publisher', 'driver_status': 'Driver Status', 'emulation_status': 'Emulation Status',
                    'sourcefile': 'Source File'
                }
                sort_key = sort_by.lower()
                if sort_key in key_to_header:
                    header_to_find = key_to_header[sort_key]
                    if header_to_find in headers:
                        sort_index = headers.index(header_to_find)
                        table_display_data.sort(key=lambda row: str(row[sort_index]).lower())
                        print(f"\n[INFO] Table sorted by '{sort_key}'.")
                    else:
                        print(f"\n[WARNING] Cannot sort by '{sort_key}'. Column not visible in current view.")
                else:
                    print(f"\n[WARNING] Invalid sort key '{sort_by}'.")

            if not table_display_data:
                print("[i] No matching software items found for table display after all filters.")
                return
            
            if output_format == "table":
                print(tabulate(table_display_data, headers=headers, tablefmt="github"))
                print(f"\nTotal rows across all systems: {len(table_display_data)}")
            elif output_format == "csv":
                output_to_csv_file(headers, table_display_data, output_file_path)

        elif output_format == "yaml":
            output_to_yaml_file(
                input_systems=systems_to_process,
                all_software_entries=all_software_entries_for_yaml_processing,
                platform_key=platform_key,
                platform_name_full=platform_name_full,
                platform_categories=platform_categories,
                media_type=media_type,
                enable_custom_cmd_per_title=enable_custom_cmd_per_title,
                emu_name=emu_name,
                default_emu=default_emu,
                default_emu_cmd_params=default_emu_cmd_params,
                output_file_path=output_file_path,
                softlist_configs_to_add=softlist_configs_to_add,
                software_configs_to_add=software_configs_to_add
            )
    else:
        print(f"[i] No systems found for output after initial filtering or no matching software items found across any specified systems "
              f"with search term '{search_term}'." if search_term else "[i] No systems or matching software items found.")

def parse_mess_ini_machines(ini_path):
    """
    Parses the MESS.ini file and extracts machine names from the [ROOT_FOLDER] section.
    """
    machines = set()
    if not os.path.exists(ini_path):
        print(f"[ERROR] MESS.ini file not found at '{ini_path}'. Cannot filter by MESS.ini.")
        return machines

    try:
        in_root_folder_section = False
        with open(ini_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line.upper().startswith('[ROOT_FOLDER]'):
                    in_root_folder_section = True
                    continue
                elif line.startswith('[') and line.endswith(']'):
                    in_root_folder_section = False
                
                if in_root_folder_section and line and not line.startswith(';'):
                    machines.add(line.split(';')[0].strip())
        print(f"[INFO] Loaded {len(machines)} machines from '{ini_path}'.")
    except Exception as e:
        print(f"[ERROR] Error parsing MESS.ini file '{ini_path}': {e}")
    return machines

def split_mame_xml_by_ini(mess_ini_path, full_mame_xml_path, output_mess_xml_file):
    """
    Filters the full mame -listxml output by machines listed in MESS.ini.
    """
    print("=== Processing Phase 1/2: Filtering mame.xml by MESS.ini entries ===")
    
    mess_machines_from_ini = parse_mess_ini_machines(mess_ini_path)
    if not mess_machines_from_ini:
        return False

    print(f"[INFO] Fetching full MAME machine list ('{full_mame_xml_path}')... This may take a moment.")
    full_mame_root = get_parsed_mame_xml_root(full_mame_xml_path)
    if full_mame_root is None:
        return False

    filtered_machines_count = 0
    try:
        filtered_root = ET.Element("mame")
        for attr in ['build', 'debug', 'emulator', 'mameconfig']:
            if full_mame_root.get(attr) is not None:
                filtered_root.set(attr, full_mame_root.get(attr))

        for machine_element in full_mame_root.findall("machine"):
            machine_name = machine_element.get("name")
            if machine_name in mess_machines_from_ini:
                filtered_root.append(machine_element)
                filtered_machines_count += 1
        
        filtered_tree = ET.ElementTree(filtered_root)
        filtered_tree.write(output_mess_xml_file, encoding="utf-8", xml_declaration=True)
        
        print(f"[INFO] Phase 1 complete: Filtered {filtered_machines_count} machines into '{output_mess_xml_file}'.")
        return True

    except Exception as e:
        print(f"[ERROR] Unexpected error during Phase 1: {e}")
    return False

def split_mess_xml_by_softwarelist(input_mess_xml_file, softlist_output_file, nosoftlist_output_file):
    """
    Splits an XML file into two new XML files based on softwarelist capability.
    """
    print("=== Processing Phase 2/2: Splitting mess.xml by softwarelist capability ===")
    
    mess_root = get_parsed_mame_xml_root(input_mess_xml_file)
    if mess_root is None:
        return False

    softlist_count = 0
    nosoftlist_count = 0

    softlist_root = ET.Element("mame")
    nosoftlist_root = ET.Element("mame")

    try:
        for attr in ['build', 'debug', 'emulator', 'mameconfig']:
            if mess_root.get(attr) is not None:
                softlist_root.set(attr, mess_root.get(attr))
                nosoftlist_root.set(attr, mess_root.get(attr))

        for machine_element in mess_root.findall("machine"):
            if machine_element.find("softwarelist") is not None:
                softlist_root.append(machine_element)
                softlist_count += 1
            else:
                nosoftlist_root.append(machine_element)
                nosoftlist_count += 1
        
        ET.ElementTree(softlist_root).write(softlist_output_file, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] Phase 2 complete: Written {softlist_count} softlist-capable machines to '{softlist_output_file}'.")

        ET.ElementTree(nosoftlist_root).write(nosoftlist_output_file, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] Phase 2 complete: Written {nosoftlist_count} non-softlist-capable machines to '{nosoftlist_output_file}'.")
        
        return True

    except Exception as e:
        print(f"[ERROR] Unexpected error during Phase 2: {e}")
    return False

def run_split_command(args):
    """Orchestrates the splitting of mame.xml based on mess.ini."""
    if not APP_CONFIG.get("mess_version"):
        print("[ERROR] MAME version is not set. Please run 'config --set-mess-version <num>' first.")
        return

    version = APP_CONFIG["mess_version"]
    version_folder_name = f"0.{version}"
    version_dir = DATA_DIR / version_folder_name
    os.makedirs(version_dir, exist_ok=True)
    
    mess_xml_output_file = version_dir / "mess.xml"
    mess_softlist_xml_file = version_dir / "mess-softlist.xml"
    mess_nosoftlist_xml_file = version_dir / "mess-nosoftlist.xml"
    
    mess_ini_path = args.mess_ini or APP_CONFIG.get('mess_ini_path')
    if not mess_ini_path or not os.path.exists(mess_ini_path):
        print(f"[ERROR] mess.ini path is not configured or not found. Cannot run split.")
        return

    # --- NEW LOGIC FOR DETERMINING SOURCE XML ---
    full_mame_xml_source_path = None
    cleanup_temp_xml = False
    
    if args.input_xml:
        if not os.path.exists(args.input_xml):
            print(f"[ERROR] The specified --input-xml file does not exist: {args.input_xml}")
            return
        full_mame_xml_source_path = args.input_xml
        print(f"[INFO] Using provided XML file as source: {full_mame_xml_source_path}")
    
    elif args.from_mame_exe:
        print("[INFO] Generating a fresh 'mame.xml' from the configured MAME executable...")
        # Define a temporary path for the generated file
        temp_xml_path = DATA_DIR / "mame-temp.xml"
        if run_mame_command(["-listxml"], temp_xml_path, use_cache=False):
            full_mame_xml_source_path = temp_xml_path
            cleanup_temp_xml = True # Mark this file for deletion after the process
        else:
            print("[ERROR] Failed to generate mame.xml from the MAME executable. Aborting split.")
            return

    if not full_mame_xml_source_path:
        print("[ERROR] Could not determine the source for the full MAME XML. Aborting.")
        return
    # --- END NEW LOGIC ---

    if not split_mame_xml_by_ini(mess_ini_path, full_mame_xml_source_path, mess_xml_output_file):
        print("[ERROR] Phase 1 failed. Aborting splitting process.")
        if cleanup_temp_xml and os.path.exists(full_mame_xml_source_path):
            os.remove(full_mame_xml_source_path)
        return

    if not split_mess_xml_by_softwarelist(mess_xml_output_file, mess_softlist_xml_file, mess_nosoftlist_xml_file):
        print("[ERROR] Phase 2 failed. Aborting splitting process.")
        if cleanup_temp_xml and os.path.exists(full_mame_xml_source_path):
            os.remove(full_mame_xml_source_path)
        return
    
    print("\n=== Splitting process complete! ===")
    print(f"All output files have been saved in: '{version_dir}'")
    # ... (rest of the print statements) ...
    
    # Clean up the large temporary mame.xml if it was generated
    if cleanup_temp_xml and os.path.exists(full_mame_xml_source_path):
        os.remove(full_mame_xml_source_path)
        print(f"\n[INFO] Cleaned up temporary file: '{full_mame_xml_source_path}'")

def display_yaml_table(args, source_xml_root):
    """
    Parses the system_softlist.yml file and displays its content in a detailed table format.
    """
    input_file = args.input_file or APP_CONFIG['system_softlist_yaml_file']
    print(f"\n===== Displaying Platforms from '{input_file}' in Table Format =====")
    
    system_softlist_data = _load_yaml_file(input_file)
    if not system_softlist_data:
        print(f"[ERROR] No data found in '{input_file}'. Nothing to display.")
        return

    platforms_to_process  = {}
    if args.platform_key:
        if args.platform_key in system_softlist_data:
            print(f"[INFO] Filtering copy operation for platform key: '{args.platform_key}'")
            platforms_to_process [args.platform_key] = system_softlist_data[args.platform_key]
        else:
            print(f"[ERROR] Platform key '{args.platform_key}' not found in '{input_file}'. Nothing to copy.")
            print(f"Available platforms are: {', '.join(system_softlist_data.keys())}")
            return
    else:
        print("[INFO] No platform key specified. Processing all platforms.")
        platforms_to_process = system_softlist_data

    table_display_data = []
    
    headers = ["System"]
    if args.show_extra_info:
        headers.extend(["Description", "Manufacturer", "Year"])
    headers.extend(["Softlist", "Software ID", "Title"])
    if args.show_extra_info:
        headers.append("Publisher")
    headers.extend(["Driver Status", "Emulation Status"])
    if args.show_extra_info:
        headers.append("Source File")

    for platform_key, platform_data in platforms_to_process.items():
        print(f"\n--- Platform: {platform_data.get('platform',{}).get('name',platform_key)} (Key: {platform_key}) ---")
        
        systems_in_platform = platform_data.get("system", [])
        if not systems_in_platform:
            print("  [INFO] No systems defined for this platform.")
            continue

        for system_entry in systems_in_platform:
            system_name = system_entry
            if isinstance(system_entry, dict):
                system_name = next(iter(system_entry))

            machine_metadata = {"description": "N/A", "manufacturer": "N/A", "status": "N/A", "emulation": "N/A", "sourcefile": "N/A"}
            if source_xml_root:
                _, machine_metadata = get_machine_details_and_filters_from_root(system_name, source_xml_root)
            
            driver_status = machine_metadata['status']
            emulation_status = machine_metadata['emulation']
            machine_description = machine_metadata['description']
            machine_manufacturer = machine_metadata['manufacturer']
            machine_year = machine_metadata['year']
            source_file = machine_metadata['sourcefile']

            if args.show_systems_only:
                row = [system_name]
                if args.show_extra_info:
                    row.extend([machine_description, machine_manufacturer, machine_year])
                row.extend(["N/A", "N/A", machine_description])
                if args.show_extra_info:
                    row.append("N/A")
                row.extend([driver_status, emulation_status])
                if args.show_extra_info:
                    row.append(source_file)
                table_display_data.append(row)
            elif isinstance(system_entry, dict) and system_entry.get(system_name, {}).get("software_lists"):
                for softlist_detail in system_entry[system_name]["software_lists"]:
                    softlist_name = softlist_detail.get("softlist_name", "N/A")
                    software_ids = softlist_detail.get("software_id", [])
                    
                    if software_ids:
                        for swid in software_ids:
                            publisher = "N/A (YAML Source)" 
                            row = [system_name]
                            if args.show_extra_info:
                                row.extend([machine_description, machine_manufacturer, machine_year])
                            row.extend([softlist_name, swid, "N/A (YAML Source)"])
                            if args.show_extra_info:
                                row.append(publisher)
                            row.extend([driver_status, emulation_status])
                            if args.show_extra_info:
                                row.append(source_file)
                            table_display_data.append(row)
                    else:
                        row = [system_name]
                        if args.show_extra_info:
                            row.extend([machine_description, machine_manufacturer, machine_year])
                        row.extend([softlist_name, "N/A", "N/A (No IDs)", "N/A"])
                        if args.show_extra_info:
                            row.append("N/A")
                        row.extend([driver_status, emulation_status])
                        if args.show_extra_info:
                            row.append(source_file)
                        table_display_data.append(row)
            else:
                row = [system_name]
                if args.show_extra_info:
                    row.extend([machine_description, machine_manufacturer, machine_year])
                row.extend(["N/A", "N/A", machine_description])
                if args.show_extra_info:
                    row.append("N/A")
                row.extend([driver_status, emulation_status])
                if args.show_extra_info:
                    row.append(source_file)
                table_display_data.append(row)

    if args.sort_by and table_display_data:
        key_to_header = {
            'system_name': 'System', 'system_desc': 'Description', 'manufacturer': 'Manufacturer', 'year': 'Year',
            'softlist': 'Softlist', 'software_id': 'Software ID', 'title': 'Title',
            'publisher': 'Publisher', 'driver_status': 'Driver Status', 'emulation_status': 'Emulation Status',
            'sourcefile': 'Source File'
        }
        sort_key = args.sort_by.lower()
        if sort_key in key_to_header:
            header_to_find = key_to_header[sort_key]
            if header_to_find in headers:
                sort_index = headers.index(header_to_find)
                table_display_data.sort(key=lambda row: str(row[sort_index]).lower())
                print(f"\n[INFO] Table sorted by '{sort_key}'.")
            else:
                print(f"\n[WARNING] Cannot sort by '{sort_key}'. Column not visible in current view.")
        else:
            print(f"\n[WARNING] Invalid sort key '{sort_by}'.")
    
    if not table_display_data:
        print("[i] No data found for table display based on provided criteria.")
        return
        
    if args.output_format == "table":
        print(tabulate(table_display_data, headers=headers, tablefmt="github"))
        print(f"\nTotal rows across displayed platforms: {len(table_display_data)}")
    elif args.output_format == "csv":
        output_to_csv_file(headers, table_display_data, args.output_file)

def display_platform_info(args):
    """
    Parses the system_softlist.yml file and displays summary information for platforms.
    """
    input_file = args.input_file or APP_CONFIG['system_softlist_yaml_file']
    print(f"\n===== Displaying Platform Information from '{input_file}' =====")
    
    system_softlist_data = _load_yaml_file(input_file)
    if not system_softlist_data:
        print(f"[ERROR] No data found in '{input_file}'. Nothing to display.")
        return

    platforms_to_display = {}
    if args.platform_key:
        if args.platform_key in system_softlist_data:
            platforms_to_display[args.platform_key] = system_softlist_data[args.platform_key]
        else:
            print(f"[ERROR] Platform '{args.platform_key}' not found in '{input_file}'.")
            return
    else:
        platforms_to_display = system_softlist_data

    platform_info_rows = []
    headers = [
        "Platform Key", "Platform Name", "Platform Category", "Media Type", "Custom CMD per Title",
        "Emulator Name", "Default Emu", "Default Emu Cmd Params",
        "# Systems", "# Softlists", "# Software IDs"
    ]

    for p_key, p_data in platforms_to_display.items():
        platform_name = p_data.get("platform", {}).get("name", "N/A")
        
        categories = p_data.get("platform_category", [])
        category_str = ", ".join(categories) if categories else "N/A"
        
        media_type = p_data.get("media_type", "N/A")
        enable_custom_cmd = p_data.get("enable_custom_command_line_param_per_software_id", False)
        
        emulator_name = p_data.get("emulator", {}).get("name", "N/A")
        default_emulator = p_data.get("emulator", {}).get("default_emulator", False)
        default_emu_cmd = p_data.get("emulator", {}).get("default_command_line_parameters", "N/A")

        systems_list = p_data.get("system", [])
        num_systems = len(systems_list)
        
        num_softlists = 0
        num_software_ids = 0

        for sys_entry in systems_list:
            if isinstance(sys_entry, dict):
                for sys_name, details in sys_entry.items():
                    softlist_array = details.get("software_lists", [])
                    num_softlists += len(softlist_array)
                    for softlist_detail in softlist_array:
                        num_software_ids += len(softlist_detail.get("software_id", []))

        platform_info_rows.append([
            p_key, platform_name, category_str, media_type, enable_custom_cmd,
            emulator_name, default_emulator, default_emu_cmd,
            num_systems, num_softlists, num_software_ids
        ])
    
    if args.sort_by_col_num is not None and platform_info_rows:
        col_num = args.sort_by_col_num
        num_cols = len(headers)
        if 1 <= col_num <= num_cols:
            sort_index = col_num - 1
            platform_info_rows.sort(key=lambda row: row[sort_index])
            print(f"\n[INFO] Table sorted by column {col_num}: '{headers[sort_index]}'.")
        else:
            print(f"[WARNING] Invalid column number {col_num}. Must be between 1 and {num_cols}. Sorting skipped.")

    if platform_info_rows:
        print(tabulate(platform_info_rows, headers=headers, tablefmt="github"))
        print(f"\nTotal platforms displayed: {len(platform_info_rows)}")
    else:
        print("[i] No platform information found for display based on criteria.")

def run_config_command(args):
    """Handles the 'config' subcommand to show or update configuration."""
    config_updated = False

    if args.set_mame_exe_path:
        if os.path.isfile(args.set_mame_exe_path):
            APP_CONFIG["mame_executable"] = args.set_mame_exe_path
            config_updated = True
        else:
            print(f"[ERROR] Path not valid for mame_executable: {args.set_mame_exe_path}")
    
    if args.set_softlist_rom_dir:
        if os.path.isdir(args.set_softlist_rom_dir):
            APP_CONFIG["softlist_rom_sources_dir"] = args.set_softlist_rom_dir
            config_updated = True
        else:
            print(f"[ERROR] Path not valid for softlist_rom_sources_dir: {args.set_softlist_rom_dir}")

    if args.set_output_rom_dir:
        APP_CONFIG["out_romset_dir"] = args.set_output_rom_dir
        config_updated = True

    if args.set_mess_ini_path:
        if os.path.isfile(args.set_mess_ini_path):
            APP_CONFIG["mess_ini_path"] = args.set_mess_ini_path
            config_updated = True
        else:
            print(f"[ERROR] Path not valid for mess_ini_path: {args.set_mess_ini_path}")

    if args.set_system_softlist_yaml_file:
        APP_CONFIG["system_softlist_yaml_file"] = args.set_system_softlist_yaml_file
        config_updated = True
      
    if args.set_mess_version:
        APP_CONFIG["mess_version"] = args.set_mess_version
        config_updated = True

    if config_updated:
        if save_configuration():
            print(f"[SUCCESS] Configuration updated in '{CONFIG_FILE}'.")
        else:
            print("[ERROR] Failed to save updated configuration.")

    if args.show or not config_updated:
        print("\n" + "=" * 20 + " Current Configuration " + "=" * 21)
        config_table = [[key, value] for key, value in APP_CONFIG.items()]
        print(tabulate(config_table, headers=["Key", "Value"], tablefmt="github"))
        print("=" * 60)

def _download_reporthook(count, block_size, total_size):
    """A simple reporthook for urllib to show download progress."""
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write(f"\r[INFO] Downloading... {percent}%")
    sys.stdout.flush()

def ensure_mess_xml_exists():
    """
    Checks if the MESS-specific XML exists for the configured version.
    If not, it prompts the user to download and extract it.
    """
    if not APP_CONFIG.get("mess_version"):
        print("[WARNING] MAME version is not set in the configuration.")
        while True:
            prompt = "          Please enter your MAME version number (e.g., 278, 277) to continue: "
            version_input = input(prompt).strip()
            if version_input.isdigit():
                APP_CONFIG["mess_version"] = version_input
                save_configuration() 
                break
            else:
                print("[!] Invalid input. Please enter only the version number.")

    version = APP_CONFIG["mess_version"]
    version_folder_name = f"0.{version}"
    version_dir = DATA_DIR / version_folder_name
    mess_xml_path = version_dir / "mess.xml"
    
    APP_CONFIG["mess_xml_file"] = str(mess_xml_path)

    if mess_xml_path.exists():
        print(f"[INFO] Found MESS XML for version {version} at: '{mess_xml_path}'")
        return True

    print(f"[WARNING] MESS XML for version {version} not found.")
    prompt = "          Would you like to download it from progetto-snaps.net? [Y/n]: "
    if input(prompt).strip().lower() not in ['', 'y', 'yes']:
        print("[INFO] Skipping download. Some features may not work correctly without the mess.xml file.")
        return False # This is a "soft" failure, the program can continue.

    # --- Download Logic ---
    url = f"https://www.progettosnaps.net/download/?tipo=mess_xml&file=/mess/packs/xml/mess{version}.zip"
    temp_zip_path = DATA_DIR / f"mess{version}_temp.zip"
    
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        print(f"[INFO] Attempting to download from: {url}")
        
        # --- REVISED, MORE COMPATIBLE SSL HANDLING ---
        # Temporarily set the default context for this operation
        # This is a widely used and compatible way to handle unverified SSL contexts
        ssl._create_default_https_context = ssl._create_unverified_context
        
        urllib.request.urlretrieve(url, temp_zip_path, _download_reporthook)
        
        # Restore the original context function after the download is done
        ssl._create_default_https_context = ssl.create_default_context
        
        sys.stdout.write("\n[INFO] Download complete.\n")
    except Exception as e:
        print(f"\n[ERROR] Failed to download file: {e}")
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)
        # --- CRITICAL FIX: Exit if download fails ---
        print("[FATAL] Cannot proceed without the MESS XML file. Please check your connection or download manually.")
        sys.exit(1) # This is a "hard" failure. Stop the program.
    # --- END REVISED SSL HANDLING ---
    
    # --- Extraction Logic ---
    try:
        print(f"[INFO] Extracting '{temp_zip_path}' to '{version_dir}'...")
        os.makedirs(version_dir, exist_ok=True)
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            xml_filename = next((name for name in zip_ref.namelist() if name.lower().endswith('.xml')), None)
            if not xml_filename:
                raise FileNotFoundError("No .xml file found inside the downloaded zip.")
            
            extracted_path = zip_ref.extract(xml_filename, path=version_dir)
            full_extracted_path = Path(extracted_path)
            mess_xml_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(full_extracted_path), str(mess_xml_path))
            
            print(f"[SUCCESS] MESS XML for version {version} is now available at '{mess_xml_path}'.")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to extract or move file: {e}")
        # --- CRITICAL FIX: Exit if extraction fails ---
        print("[FATAL] Cannot proceed without the MESS XML file.")
        sys.exit(1) # This is also a "hard" failure.
    finally:
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)   

def main():
    global DEBUG_MODE_ENABLED 

    parser = argparse.ArgumentParser(
        description="MAME Software & ROM Management Tool.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug messages for detailed output."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=False)

    config_parser = subparsers.add_parser("config", help="View or update the tool's configuration.")
    config_parser.add_argument("--show", action="store_true", help="Show the current configuration (default action).")
    config_parser.add_argument("--set-mame-exe-path", help="Set the path to mame.exe.")
    config_parser.add_argument("--set-softlist-rom-dir", help="Set the path to the softlist ROMs directory.")
    config_parser.add_argument("--set-output-rom-dir", help="Set the path for curated output ROMsets.")
    config_parser.add_argument("--set-mess-ini-path", help="Set the path to mess.ini.")
    config_parser.add_argument("--set-system-softlist-yaml-file", help="Set the output YAML filename (e.g., my_platforms.yml).")  
    config_parser.add_argument("--set-mess-version", help="Set the MAME version number (e.g., 278).")
        
    sort_by_choices = ['system_name', 'system_desc', 'manufacturer', 'year', 'software_id', 'title', 'publisher', 'driver_status', 'emulation_status', 'sourcefile']

    table_args_parser = argparse.ArgumentParser(add_help=False)
    table_args_parser.add_argument("--show-systems-only", action="store_true", help="[For Table] Only show one row per system.")
    table_args_parser.add_argument("--show-extra-info", action="store_true", help="[For Table Output] Show additional columns: Description, Manufacturer, Year, Publisher, and Source File.")
    table_args_parser.add_argument("--sort-by", choices=sort_by_choices, help="[For Table] Sort the output table by a specific column.")

    # Base parser for YAML output arguments, to avoid repetition
    yaml_args_parser = argparse.ArgumentParser(add_help=False)
    yaml_args_parser.add_argument("--platform-key", help="[Required for YAML] Top-level key for the platform in YAML.")
    yaml_args_parser.add_argument("--platform-name-full", help="[Required for YAML] Full, descriptive name of the platform.")
    yaml_args_parser.add_argument("--platform-category", nargs='+', help="[For YAML] One or more categories for the platform.")
    yaml_args_parser.add_argument("--media-type", help="[For YAML] Media type for the platform (e.g., 'cart').")
    yaml_args_parser.add_argument("-ect", "--enable-custom-cmd-per-title", action="store_true", help="Set 'enable_custom_command_line_param_per_software_id: true'.")
    yaml_args_parser.add_argument("-en", "--emu-name", help="Sets the 'emulator.name'.")
    yaml_args_parser.add_argument("-de", "--default-emu", action="store_true", help="Set 'emulator.default_emulator: true'.")
    yaml_args_parser.add_argument("-dec", "--default-emu-cmd-params", help="Sets 'emulator.default_command_line_parameters'.")
    yaml_args_parser.add_argument("--add-software-config", action="append", metavar='SOFTLIST:SWID:"PARAMETERS"', help="[For YAML] Add a custom command for a specific software ID. Format: softlist_name:software_id:\"command params\". Can be used multiple times.")
    yaml_args_parser.add_argument("--add-softlist-config", action="append", metavar='SOFTLIST:"PARAMETERS"', help="[For YAML] Add a default command for an entire softlist. Format: softlist_name:\"command params\". Can be used multiple times.")

    # Base parser for system inclusion/exclusion
    inclusion_args_parser = argparse.ArgumentParser(add_help=False)
    inclusion_args_parser.add_argument("--include-systems", default="", help="A space-separated string of MAME system short names to explicitly include (e.g., \"nes snes\").")
    inclusion_args_parser.add_argument("--exclude-systems", default="", help="A space-separated string of MAME system short names to explicitly exclude (e.g., \"nes snes\").")
    inclusion_args_parser.add_argument("--include-softlist", default="", help="A space-separated string of software lists to ONLY include (e.g., \"nes nes_vt_cart\").")
    inclusion_args_parser.add_argument("--exclude-softlist", default="", help="A space-separated string of software lists to explicitly exclude (e.g., \"nes_ade nes_datach\").")    

    search_parser = subparsers.add_parser("search", help="Search MAME systems and generate YAML/table/CSV output.", parents=[table_args_parser, yaml_args_parser, inclusion_args_parser])
    search_parser.add_argument("systems", nargs='*', default=[], help="[Optional] One or more MAME system short names (e.g., 'nes', 'snes'). If omitted, all systems from the input XML will be considered for filtering.")
    
    # --- New Filter Arguments ---
    search_parser.add_argument("--filter-machine-name-fuzzy", help="Filter machines by a name prefix (e.g., 'jak_').")
    search_parser.add_argument("--filter-machine-description", nargs='+', help="Filter machines where the description contains one or more of these terms.")
    search_parser.add_argument("--filter-machine-sourcefile", help="Filter machines by the driver source file (e.g., 'xavix.cpp').")
    search_parser.add_argument("--filter-software-description", help="Filter software by a term in its ID or description.")
    
    # --- Universal Arguments ---
    search_parser.add_argument("--input-xml", help=f"Path to source XML for machine definitions. Defaults to 'mess.xml' or '{MAME_ALL_MACHINES_XML_CACHE}'.")
    search_parser.add_argument("--limit", type=int, help="Limit the number of systems processed.")
    search_parser.add_argument("--output-format", choices=["table", "yaml", "csv"], default="table", help="Output format: 'table' (default), 'yaml', or 'csv'.")
    search_parser.add_argument("--output-file", help="Path to the output file (required for 'csv' format, optional for 'yaml').")
    search_parser.add_argument("--driver-status", choices=["good", "imperfect", "preliminary", "unsupported"], help="Filter machines by driver 'status'.")
    search_parser.add_argument("--emulation-status", choices=["good", "imperfect", "preliminary", "unsupported"], help="Filter machines by driver 'emulation' status.")   

    copy_parser = subparsers.add_parser("copy-roms", help="Copy/create ROM zips based on system_softlist.yml.")
    copy_parser.add_argument("--input-file", help="Path to the input YAML file. Defaults to config.")
    copy_parser.add_argument("--platform-key", help="Optional: Copy ROMs only for a specific platform by its key.")
    copy_parser.add_argument("--create-placeholder-zip", action="store_true", help="Always create empty placeholder (dummy) zips instead of copying from the source directory.")
    copy_parser.add_argument("--dry-run", action="store_true", help="Show what would be copied or created without modifying any files.")
    
    split_parser = subparsers.add_parser("split", help="Generate filtered MAME XMLs based on MESS.ini.")
    split_parser.add_argument("--mess-ini", help="Path to MESS.ini. Defaults to config.")

    # Use a mutually exclusive group to ensure only one source is provided
    source_group = split_parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--input-xml", help="Path to an existing full mame.xml to use as the source.")
    source_group.add_argument("--from-mame-exe", action="store_true", help="Generate a fresh mame.xml from the mame.exe defined in your config.")

    table_parser = subparsers.add_parser("table", help="Display data from system_softlist.yml in a table format.", parents=[table_args_parser])
    table_parser.add_argument("--platform-key", help="Optional: Display only a specific platform by its key.")
    table_parser.add_argument("--input-file", help="Path to the input YAML file. Defaults to config.")
    table_parser.add_argument("--mame-xml-source", help=f"Path to MAME XML for fetching machine info. Defaults to '{MAME_ALL_MACHINES_XML_CACHE}'.")
    table_parser.add_argument("--output-format", choices=["table", "csv"], default="table", help="Output format: 'table' (default) or 'csv'.")
    table_parser.add_argument("--output-file", help="Path to the output file (required for 'csv' format).")

    platform_info_parser = subparsers.add_parser("platform-info", help="Display high-level information about platforms in system_softlist.yml.")
    platform_info_parser.add_argument("--platform-key", help="Optional: Display info for a specific platform by key.")
    platform_info_parser.add_argument("--input-file", help="Path to the input YAML file. Defaults to config.")
    platform_info_parser.add_argument("--sort-by-col-num", type=int, help="[For Table] Sort the output table by a 1-based column number.")

    args = parser.parse_args()

    if args.debug:
        DEBUG_MODE_ENABLED = True
        debug_print("Debug mode enabled.")

    if args.command == "config":
        load_configuration()
        run_config_command(args)
        sys.exit(0)
    
    initialize_application()

    if not args.command:
        parser.print_help()
        print("\n[INFO] No command specified. Use 'config' to set up, or a command like 'search' to begin.")
        sys.exit(0)

    # default cmd line param that applies to all titles for a softlist
    softlist_configs_to_add = {}
    if hasattr(args, 'add_softlist_config') and args.add_softlist_config:
        for config_str in args.add_softlist_config:
            try:
                parts = config_str.split(':', 1)
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                softlist_name, params = parts
                params = params.strip('"')

                softlist_configs_to_add[softlist_name] = {"command_line_parameters": params}
                print(f"[INFO] Queued default command for softlist '{softlist_name}'.")

            except ValueError:
                print(f"[ERROR] Invalid format for --add-softlist-config: '{config_str}'. Expected SOFTLIST:\"PARAMETERS\". Aborting.")
                sys.exit(1)        

    # a per title cmd line param that will override add_softlist_config
    software_configs_to_add = {}
    if hasattr(args, 'add_software_config') and args.add_software_config:
        for config_str in args.add_software_config:
            try:
                parts = config_str.split(':', 2)
                if len(parts) != 3:
                    raise ValueError("Invalid format")
                
                softlist_name, swid, params = parts
                params = params.strip('"')

                if softlist_name not in software_configs_to_add:
                    software_configs_to_add[softlist_name] = {}
                
                software_configs_to_add[softlist_name][swid] = {"command_line_parameters": params}
                print(f"[INFO] Queued custom command for '{swid}' in softlist '{softlist_name}'.")

            except ValueError:
                print(f"[ERROR] Invalid format for --add-software-config: '{config_str}'. Expected SOFTLIST:SWID:\"PARAMETERS\". Aborting.")
                sys.exit(1)    

    if args.command == "search":
        # Determine the source XML file to use
        xml_source_path = args.input_xml or APP_CONFIG.get('mess_xml_file') or MAME_ALL_MACHINES_XML_CACHE
        source_xml_root = get_parsed_mame_xml_root(xml_source_path)
        if source_xml_root is None: 
            sys.exit(1)

        # 1. Build the initial pool of systems to consider
        systems_pool = set()
        
        # Check if the user is providing an explicit set of systems to start with
        user_provided_systems = bool(args.systems or args.filter_machine_name_fuzzy or (hasattr(args, 'include_systems') and args.include_systems))
        
        if user_provided_systems:
            print("[INFO] User has provided an explicit list of systems to process.")
            # Start with an empty set and only add what the user specifies.
            if args.systems:
                systems_pool.update(args.systems)
                print(f"[INFO] Added {len(args.systems)} system(s) from positional arguments.")
            
            if args.filter_machine_name_fuzzy:
                fuzzy_matches = get_all_mame_systems_by_prefix_from_root(args.filter_machine_name_fuzzy, source_xml_root)
                if fuzzy_matches:
                    print(f"[INFO] Adding {len(fuzzy_matches)} systems from fuzzy search for '{args.filter_machine_name_fuzzy}'.")
                    systems_pool.update(fuzzy_matches)
                else:
                    print(f"[INFO] No systems found matching '--filter-machine-name-fuzzy {args.filter_machine_name_fuzzy}'.")
            
            if hasattr(args, 'include_systems') and args.include_systems:
                include_systems_list = [item.strip() for item in args.include_systems.replace(',', ' ').split() if item.strip()]
                systems_pool.update(include_systems_list)
                print(f"[INFO] Added {len(include_systems_list)} system(s) from --include-systems.")
        else:
            # If no systems are specified, the pool is ALL systems from the XML, which will then be filtered.
            print(f"[INFO] No specific systems provided. Starting with all systems from '{os.path.basename(xml_source_path)}' for filtering.")
            systems_pool.update(get_all_mame_systems_from_xml_file(xml_source_path))

        # 2. Sequentially apply filters to the pool
        print(f"[INFO] Initial system pool size: {len(systems_pool)}")

        if args.filter_machine_description:
            initial_count = len(systems_pool)
            filtered_set = set()
            for machine_element in source_xml_root.findall("machine"):
                machine_name = machine_element.get("name")
                if machine_name in systems_pool: # Only check machines already in our pool
                    description = machine_element.findtext("description", "")
                    if all(term.lower() in description.lower() for term in args.filter_machine_description):
                        filtered_set.add(machine_name)
            systems_pool = filtered_set
            print(f"[INFO] After --filter-machine-description: {initial_count} -> {len(systems_pool)} systems.")

        if args.filter_machine_sourcefile:
            initial_count = len(systems_pool)
            filtered_set = set()
            for machine_element in source_xml_root.findall("machine"):
                machine_name = machine_element.get("name")
                if machine_name in systems_pool:
                    sourcefile = machine_element.get("sourcefile", "")
                    if args.filter_machine_sourcefile.lower() in sourcefile.lower():
                        filtered_set.add(machine_name)
            systems_pool = filtered_set
            print(f"[INFO] After --filter-machine-sourcefile: {initial_count} -> {len(systems_pool)} systems.")

        # 3. Apply manual includes and excludes
        if hasattr(args, 'include_systems') and args.include_systems:
            include_systems_list = [item.strip() for item in args.include_systems.replace(',', ' ').split() if item.strip()]
            initial_count = len(systems_pool)
            systems_pool.update(include_systems_list)
            print(f"[INFO] After --include-systems: {initial_count} -> {len(systems_pool)} systems.")

        if hasattr(args, 'exclude_systems') and args.exclude_systems:
            exclude_systems_list = [item.strip() for item in args.exclude_systems.replace(',', ' ').split() if item.strip()]
            initial_count = len(systems_pool)
            systems_pool -= set(exclude_systems_list)
            print(f"[INFO] After --exclude-systems: {initial_count} -> {len(systems_pool)} systems.")

        # 4. Prepare arguments for the core function
        systems_to_process = sorted(list(systems_pool))
        if hasattr(args, 'limit') and args.limit is not None: 
            systems_to_process = systems_to_process[:args.limit]
            print(f"[INFO] Limiting to first {len(systems_to_process)} systems.")

        # Consolidate YAML/CSV/Table arguments
        platform_key = getattr(args, 'platform_key', None)
        platform_name_full = getattr(args, 'platform_name_full', None)
        # (and all other platform/emu args...)

        # 5. Validation and Final Call
        if args.output_format == "csv" and not args.output_file:
            parser.error("--output-file is required when using --output-format csv")
        
        if args.output_format == "yaml":
            # ... (your existing YAML validation logic remains the same) ...
            if not all([platform_key, platform_name_full, args.media_type]):
                parser.error("For YAML output, --platform-key, --platform-name-full, and --media-type are required.")
            if not systems_to_process:
                print("[WARNING] No systems to process after all filters were applied.")
                sys.exit(0)

        # Call the core function with the final, curated list of systems
        perform_mame_search_and_output(
            systems_to_process,
            args.filter_software_description or "",
            args.output_format,
            # Pass all the other args as before
            platform_key, platform_name_full, args.platform_category, args.media_type,
            args.enable_custom_cmd_per_title, args.emu_name, args.default_emu, args.default_emu_cmd_params,
            args.output_file, args.driver_status, args.emulation_status,
            args.show_systems_only, args.show_extra_info, source_xml_root, sort_by=args.sort_by,
            exclude_softlist=[item.strip() for item in args.exclude_softlist.split()],
            include_softlist=[item.strip() for item in args.include_softlist.split()],
            software_configs_to_add=software_configs_to_add, # You'll need to re-add the logic for these dicts
            softlist_configs_to_add=softlist_configs_to_add
        )

    elif args.command == "copy-roms":
        perform_rom_copy_operation(args)
    elif args.command == "split":
        run_split_command(args)
    elif args.command == "table":
        if args.output_format == "csv" and not args.output_file:
            parser.error("--output-file is required when using --output-format csv")
        mame_xml_source = args.mame_xml_source or APP_CONFIG.get('mess_xml_file') or MAME_ALL_MACHINES_XML_CACHE
        table_source_xml_root = get_parsed_mame_xml_root(mame_xml_source)
        if table_source_xml_root:
            display_yaml_table(args, table_source_xml_root)
    elif args.command == "platform-info":
        display_platform_info(args)

    for tmp_file in [TMP_SOFTWARE_XML_FILE]: 
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

if __name__ == "__main__":
    main()