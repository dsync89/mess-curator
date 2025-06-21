import sys
import subprocess
import xml.etree.ElementTree as ET
import os
import yaml
from tabulate import tabulate
import argparse
import shutil # For file copying
import zipfile # For creating dummy zips

# === Configuration Paths ===
MAME_EXECUTABLE = r"c:\Programs\LaunchBox\Emulators\MAME 0.277\mame.exe"
# Directory where MAME's softlist ROMs are located (e.g., mame/roms/nes/, mame/roms/ekara_cart/)
# IMPORTANT: Adjust this path to your MAME installation's 'roms' directory.
SOFTLIST_ROM_SOURCES_DIR = r"c:\Programs\LaunchBox\Emulators\MAME 0.277\roms\softlist"
OUT_ROMSET_DIR = r"..\out\mame_curated_romset" # Where the curated ROMs will be copied to

# Path to your MESS.ini file (adjust as needed)
MESS_INI_PATH = r"..\data\mess.ini"

# === Configuration Files ===
SYSTEM_SOFTLIST_YAML_FILE = "system_softlist.yml" # Output YAML file for platform definitions

# === Temporary XML Files ===
TMP_SOFTWARE_XML_FILE = "tmp_software.xml"
TMP_MACHINE_XML_FILE = "tmp_machine.xml"
TMP_ALL_MACHINES_XML_FILE = "tmp_all_machines.xml" # This is the main one for caching -listxml output
# New temporary XML files for splitting
TMP_MESS_XML_FILE = "tmp_mess.xml"
TMP_MESS_SOFTLIST_XML_FILE = "mess-softlist.xml"
TMP_MESS_NOSOFTLIST_XML_FILE = "mess-nosoftlist.xml"


# === Helper Functions (YAML, XML Parsing, MAME Interaction) ===

def _load_yaml_file(file_path):
    """Loads YAML data from a given file path, returns empty dict if not found or invalid."""
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

def run_mame_command(args, output_file, use_cache=False): # Added use_cache parameter
    """
    Runs a MAME command and pipes output to a file.
    If use_cache is True, it checks if output_file already exists and skips MAME execution if so.
    """
    if use_cache and os.path.exists(output_file):
        print(f"[INFO] Using cached XML file: '{output_file}'. Skipping MAME execution.")
        return True # File exists, proceed as if MAME ran successfully

    try:
        cmd = [MAME_EXECUTABLE] + args
        print(f"[DEBUG] Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=os.path.dirname(MAME_EXECUTABLE)
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
        print(f"[!] Error: MAME executable not found at '{MAME_EXECUTABLE}'")
        return False
    except Exception as e:
        print(f"[!] Exception running MAME command '{' '.join(args)}': {e}")
        return False

def get_all_mame_systems_from_xml_file(xml_filepath):
    """
    Parses an XML file (like mess-softlist.xml) and extracts all machine names.
    Returns a set of machine names.
    """
    machines = set()
    if not os.path.exists(xml_filepath):
        print(f"[ERROR] XML file not found at '{xml_filepath}'. Cannot extract systems.")
        return machines

    try:
        tree = ET.parse(xml_filepath)
        root = tree.getroot() # Expects <mame> root

        for machine_element in root.findall("machine"):
            machine_name = machine_element.get("name")
            if machine_name:
                machines.add(machine_name)
        print(f"[INFO] Loaded {len(machines)} machines from '{xml_filepath}'.")
    except ET.ParseError as pe:
        print(f"[ERROR] XML parse error for '{xml_filepath}': {pe}.")
    except Exception as e:
        print(f"[ERROR] Unexpected error parsing XML file '{xml_filepath}': {e}")
    return machines


def get_all_mame_systems_by_prefix(prefix):
    """
    Runs mame -listxml to get all machine definitions
    and returns a list of machine names that start with the given prefix.
    """
    matching_systems = []
    print(f"[DEBUG] Fetching all MAME machines for fuzzy search with prefix '{prefix}'. This may take a moment...")
    # Use cache for TMP_ALL_MACHINES_XML_FILE
    if not run_mame_command(["-listxml"], TMP_ALL_MACHINES_XML_FILE, use_cache=True): 
        print(f"[DEBUG] Failed to get full MAME machine list. Cannot perform fuzzy search.")
        return matching_systems

    try:
        tree = ET.parse(TMP_ALL_MACHINES_XML_FILE)
        root = tree.getroot()

        for machine_element in root.findall("machine"):
            machine_name = machine_element.get("name")
            if machine_name and machine_name.startswith(prefix):
                matching_systems.append(machine_name)
        print(f"[DEBUG] Found {len(matching_systems)} systems matching prefix '{prefix}'.")

    except ET.ParseError as pe:
        print(f"[!] XML parse error for '{TMP_ALL_MACHINES_XML_FILE}': {pe}. Content might be malformed XML.")
        with open(TMP_ALL_MACHINES_XML_FILE, 'r', encoding='utf-8') as f:
            print(f"[!] File content (first 500 chars):\n{f.read(500)}...")
    except Exception as e:
        print(f"[!] Unexpected error parsing all machines XML '{TMP_ALL_MACHINES_XML_FILE}': {e}")
    finally:
        # Don't remove TMP_ALL_MACHINES_XML_FILE here if it's cached, as it's meant to persist.
        # It should only be removed if main() explicitly decides to clear all temp files.
        pass 
    return matching_systems

def get_machine_details_and_filters(system_name):
    """
    Runs mame -listxml <system_name> to get machine definition,
    extracts softwarelist filters and driver status info, and machine description.
    Returns a tuple: (filters_dict, machine_metadata_dict)
    machine_metadata_dict will contain description, manufacturer, driver status, and emulation status.
    """
    filters = {}
    machine_metadata = {"description": "N/A", "manufacturer": "N/A", "status": "N/A", "emulation": "N/A"} # Default values
    print(f"[DEBUG] Attempting to get machine details for '{system_name}'.")
    # Don't use cache for TMP_MACHINE_XML_FILE as it's specific to one system and overwritten.
    if not run_mame_command(["-listxml", system_name], TMP_MACHINE_XML_FILE):
        print(f"[DEBUG] Failed to get machine XML for '{system_name}'.")
        return filters, machine_metadata

    try:
        tree = ET.parse(TMP_MACHINE_XML_FILE)
        root = tree.getroot()

        machine_element = root.find(f"machine[@name='{system_name}']")
        if machine_element is None:
            print(f"[DEBUG] Machine '{system_name}' tag not found within '{TMP_MACHINE_XML_FILE}'. This is unexpected if -listxml succeeded.")
            return filters, machine_metadata

        # Extract machine description and manufacturer
        machine_metadata["description"] = machine_element.findtext("description", "N/A").strip()
        machine_metadata["manufacturer"] = machine_element.findtext("manufacturer", "N/A").strip()

        # Extract driver info
        driver_element = machine_element.find("driver")
        if driver_element is not None:
            machine_metadata["status"] = driver_element.get("status", "N/A")
            machine_metadata["emulation"] = driver_element.get("emulation", "N/A")

        # Extract softlist filters
        found_swlist_tags = False
        for swlist_tag in machine_element.findall("softwarelist"):
            found_swlist_tags = True
            softlist_name = swlist_tag.get("name")
            softlist_filter = swlist_tag.get("filter")
            if softlist_name:
                filters[softlist_name] = softlist_filter.upper() if softlist_filter else None
                print(f"[DEBUG] -> Found softlist tag for '{softlist_name}' with filter: '{filters[softlist_name]}'")
            else:
                print(f"[DEBUG] -> Found a softwarelist tag without a 'name' attribute in machine '{system_name}'. Skipping.")
        
        if not found_swlist_tags:
            print(f"[DEBUG] No <softwarelist> tags found within machine '{system_name}' definition.")

    except ET.ParseError as pe:
        print(f"[!] XML parse error for '{TMP_MACHINE_XML_FILE}': {pe}. Content might be malformed XML.")
        with open(TMP_MACHINE_XML_FILE, 'r', encoding='utf-8') as f:
            print(f"[!] File content (first 500 chars):\n{f.read(500)}...")
    except Exception as e:
        print(f"[!] Unexpected error parsing machine XML '{TMP_MACHINE_XML_FILE}': {e}")
    finally:
        if os.path.exists(TMP_MACHINE_XML_FILE):
            os.remove(TMP_MACHINE_XML_FILE)
    return filters, machine_metadata


def parse_software_list_from_file(search="", expected_softlist_name=None, system_name="", machine_softlist_filters=None):
    """
    Parses the software list XML, applying search and machine-defined compatibility filters.
    Returns a list of tuples: (softlist_name_from_xml, system_name, swid, desc, publisher)
    """
    if machine_softlist_filters is None:
        machine_softlist_filters = {}

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

    print(f"\n[DEBUG] Parsing software list XML for '{system_name}'.")
    print(f"[DEBUG] Machine-defined filters: {machine_softlist_filters}")

    processed_softlists_count = 0
    for swlist_elem in software_lists_elements:
        current_softlist_name_from_xml = swlist_elem.get("name")
        if not current_softlist_name_from_xml:
            print(f"[DEBUG] Skipping softwarelist element without 'name' attribute.")
            continue

        processed_softlists_count += 1
        print(f"[DEBUG] - Processing softlist '{current_softlist_name_from_xml}' from -listsoftware XML.")

        required_compatibility_filter = machine_softlist_filters.get(current_softlist_name_from_xml)
        
        if required_compatibility_filter:
            print(f"[DEBUG]   Applying sharedfeat compatibility filter for '{current_softlist_name_from_xml}': '{required_compatibility_filter}'.")
        else:
            print(f"[DEBUG]   No specific sharedfeat compatibility filter found for '{current_softlist_name_from_xml}' from machine definition. Software from this list will NOT be sharedfeat-filtered.")

        for sw in swlist_elem.findall("software"):
            swid = sw.get("name", "")
            desc = sw.findtext("description", default="").strip()
            publisher = sw.findtext("publisher", default="N/A").strip() # Extract publisher

            is_compatible = True
            if required_compatibility_filter:
                compatibility_feat = sw.find('sharedfeat[@name="compatibility"]')
                if compatibility_feat is None:
                    is_compatible = False
                else:
                    sharedfeat_values_str = compatibility_feat.get("value", "").upper()
                    sharedfeat_values = [v.strip() for v in sharedfeat_values_str.split(',') if v.strip()]
                    if required_compatibility_filter not in sharedfeat_values:
                        is_compatible = False

            if not is_compatible:
                continue

            if search.lower() in swid.lower() or search.lower() in desc.lower():
                # Store the actual softlist name this software came from for YAML output, AND publisher
                results.append((current_softlist_name_from_xml, system_name, swid, desc, publisher))
    
    if processed_softlists_count == 0:
        print(f"[DEBUG] No softwarelist elements found in {TMP_SOFTWARE_XML_FILE}.")

    return results

def output_to_yaml_file(input_systems, all_software_entries, platform_key, platform_name_full, media_type, 
                         enable_custom_cmd_per_title, emu_name, default_emu, default_emu_cmd_params, 
                         output_file_path=None):
    """
    Generates or updates the system_softlist.yml file with the platform and software IDs.
    'input_systems' is the list of system names passed via the command line (original or fuzzy-expanded).
    'all_software_entries' is a combined list of (softlist_name_from_xml, system_name, swid, desc, publisher) tuples.
    Args for platform details are passed directly.
    """
    # New structure to hold software info:
    # { 'system_name': { 'softlists_data': { 'softlist_name_A': set(id1, id2), 'softlist_name_B': set(id3, id4) } } }
    software_info_by_system = {} 

    # Note: all_software_entries now contains a publisher field (5th element)
    for softlist_name_xml, sys_name, swid, desc, publisher in all_software_entries:
        if sys_name not in software_info_by_system:
            software_info_by_system[sys_name] = {'softlists_data': {}}
        
        if softlist_name_xml not in software_info_by_system[sys_name]['softlists_data']:
            software_info_by_system[sys_name]['softlists_data'][softlist_name_xml] = set()
        
        software_info_by_system[sys_name]['softlists_data'][softlist_name_xml].add(swid)

    system_list_for_yaml = []
    for sys_name in input_systems: # Iterate based on original user input order
        system_details = {} 

        # Now, directly use the softlist_name captured from the MAME output
        if sys_name in software_info_by_system:
            # Prepare the list of software_lists for this system
            software_lists_array = []
            # Sort the softlists by name for consistent YAML output
            for softlist_name, soft_ids_set in sorted(software_info_by_system[sys_name]['softlists_data'].items()):
                softlist_entry = {"softlist_name": softlist_name}
                if soft_ids_set: # Only add software_id if there are IDs for this softlist
                    softlist_entry["software_id"] = sorted(list(soft_ids_set))
                software_lists_array.append(softlist_entry)
            
            # Add the 'software_lists' key (plural) to system_details
            if software_lists_array: # Only add if there are any softlists data
                system_details["software_lists"] = software_lists_array
        
        if system_details: # If we have any details (software_lists data)
            system_list_for_yaml.append({sys_name: system_details})
        else: # Fallback if no details (e.g., no software found/filtered for this system)
            system_list_for_yaml.append(sys_name)
            print(f"[INFO] No detailed info (software_lists or software_id) for system '{sys_name}'. Will be listed as a simple string in YAML.")

    # Build the main platform entry
    new_platform_entry = {
        "platform": {
            "name": platform_name_full
        },
        "media_type": media_type,
    }

    new_platform_entry["enable_custom_command_line_param_per_software_id"] = enable_custom_cmd_per_title

    if emu_name:
        emulator_details = {"name": emu_name}
        emulator_details["default_emulator"] = default_emu
        if default_emu_cmd_params:
            emulator_details["default_command_line_parameters"] = default_emu_cmd_params
        new_platform_entry["emulator"] = emulator_details

    new_platform_entry["system"] = system_list_for_yaml

    existing_data = _load_yaml_file(output_file_path or SYSTEM_SOFTLIST_YAML_FILE)
    existing_data[platform_key] = new_platform_entry

    target_file = output_file_path or SYSTEM_SOFTLIST_YAML_FILE
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            yaml.dump(existing_data, f, default_flow_style=False, sort_keys=False)
        print(f"\nSuccessfully generated/updated '{target_file}' with platform '{platform_key}'.")
        print("\n--- Current YAML content for this platform ---")
        print(yaml.dump({platform_key: new_platform_entry}, default_flow_style=False, sort_keys=False))
        print("---------------------------------------------")
    except Exception as e:
        print(f"[ERROR] Failed to write YAML to '{target_file}': {e}")

# === ROM Copying Functions ===

def _copy_single_rom(softid, softlist_name_for_copy, system_name, platform_key):
    """
    Copies a single software ROM or creates a dummy zip if not found.
    """
    copied = 0
    missing = 0
    
    # Source path: SOFTLIST_ROM_SOURCES_DIR / softlist_name_for_copy / softid.zip
    rom_src_path = os.path.join(SOFTLIST_ROM_SOURCES_DIR, softlist_name_for_copy, f"{softid}.zip")
    
    # Destination path: OUT_ROMSET_DIR / platform_key / system_name / softlist_name_for_copy / softid.zip
    rom_dst_dir = os.path.join(OUT_ROMSET_DIR, platform_key, system_name, softlist_name_for_copy)
    rom_dst_path = os.path.join(rom_dst_dir, f"{softid}.zip")

    os.makedirs(rom_dst_dir, exist_ok=True) # Ensure destination directory exists

    if os.path.exists(rom_src_path):
        try:
            shutil.copy2(rom_src_path, rom_dst_path)
            print(f"[✓] Copied ROM: {softid}.zip → {rom_dst_path}")
            copied = 1
        except Exception as e:
            print(f"[ERROR] Failed to copy {softid}.zip from {rom_src_path} to {rom_dst_path}: {e}")
            # If copy fails, treat as missing and create dummy
            _create_dummy_zip_for_rom(rom_dst_path, softid)
            missing = 1 # Still counted as missing from source
    else:
        print(f"[✗] Missing ROM: {softid}.zip from '{softlist_name_for_copy}'. Creating dummy at {rom_dst_path}")
        _create_dummy_zip_for_rom(rom_dst_path, softid)
        missing = 1
    
    return copied, missing

def _create_dummy_zip_for_rom(zip_path, softid):
    """Creates an empty zip file for a specific software ID."""
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            pass # Create empty zip
        print(f"[○] Created dummy zip: {os.path.basename(zip_path)}")
    except Exception as e:
        print(f"[ERROR] Failed to create dummy zip {softid}.zip at {zip_path}: {e}")

def _create_dummy_zip_for_system(system_name, platform_key):
    """Creates an empty zip file for a standalone system (no software_id specified)."""
    dst_dir = os.path.join(OUT_ROMSET_DIR, platform_key, system_name)
    os.makedirs(dst_dir, exist_ok=True)
    zip_path = os.path.join(dst_dir, f"{system_name}.zip")
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            pass
        print(f"[○] Created empty zip for standalone system: {zip_path}")
        return 1
    except Exception as e:
        print(f"[ERROR] Failed to create empty zip for system {system_name} at {zip_path}: {e}")
        return 0

def perform_rom_copy_operation(args):
    """
    Parses the system_softlist.yml file and copies/creates ROM zips based on its content.
    """
    print(f"\n===== Starting ROM Copy Operation =====")
    print(f"Source MAME Softlist ROMs: {SOFTLIST_ROM_SOURCES_DIR}")
    print(f"Destination Curated ROMset: {OUT_ROMSET_DIR}")

    system_softlist_data = _load_yaml_file(args.input_file or SYSTEM_SOFTLIST_YAML_FILE)
    
    if not system_softlist_data:
        print(f"[ERROR] No data found in '{args.input_file or SYSTEM_SOFTLIST_YAML_FILE}'. Nothing to copy.")
        return

    total_systems_processed = 0
    total_software_copied = 0
    total_software_missing = 0
    total_empty_system_zips = 0

    for platform_key, platform_data in system_softlist_data.items():
        platform_name = platform_data.get("platform", {}).get("name", platform_key)
        media_type = platform_data.get("media_type", "unknown")
        systems_in_platform = platform_data.get("system", [])

        print(f"\n[>>>] Processing Platform: '{platform_name}' (Key: '{platform_key}', Media: '{media_type}')")

        for system_entry in systems_in_platform:
            total_systems_processed += 1
            if isinstance(system_entry, str): # Simple system entry like 'popira'
                system_name = system_entry
                print(f"  [>] Processing standalone system: '{system_name}'")
                total_empty_system_zips += _create_dummy_zip_for_system(system_name, platform_key)
            elif isinstance(system_entry, dict): # System with nested details like '{sys_name: {software_lists: [...]}}'
                for system_name, details in system_entry.items():
                    print(f"  [>] Processing system with details: '{system_name}'")
                    
                    software_lists_for_system = details.get("software_lists", []) # Get the list of softlist dictionaries
                    
                    if not software_lists_for_system:
                        print(f"  [INFO]   No 'software_lists' found in YAML for system '{system_name}'. Creating dummy zip for system.")
                        total_empty_system_zips += _create_dummy_zip_for_system(system_name, platform_key)
                        continue

                    # Iterate through each softlist entry within the system
                    for softlist_detail in software_lists_for_system:
                        softlist_name_for_copy = softlist_detail.get("softlist_name")
                        software_ids_for_softlist = softlist_detail.get("software_id", [])

                        if not softlist_name_for_copy:
                            print(f"[ERROR]   Softlist entry for '{system_name}' missing 'softlist_name'. Cannot copy ROMs for this entry.")
                            continue # Skip malformed softlist entry

                        if not software_ids_for_softlist:
                            print(f"  [INFO]   No 'software_id's listed for softlist '{softlist_name_for_copy}' under system '{system_name}'. No ROMs to copy for this specific softlist.")
                            continue

                        print(f"  [INFO]   Copying ROMs from softlist '{softlist_name_for_copy}' for system '{system_name}'.")
                        for swid in software_ids_for_softlist:
                            copied, missing = _copy_single_rom(swid, softlist_name_for_copy, system_name, platform_key)
                            total_software_copied += copied
                            total_software_missing += missing
            else:
                print(f"[WARNING] Invalid system entry type in YAML: {system_entry}. Skipping.")

    print(f"\n===== ROM Copy Operation Summary =====")
    print(f"  Total Platforms Processed: {len(system_softlist_data)}")
    print(f"  Total Systems Processed: {total_systems_processed}")
    print(f"  Total Software ROMs Copied: {total_software_copied}")
    print(f"  Total Software ROMs Missing (Dummy Created): {total_software_missing}")
    print(f"  Total Empty System Zips Created: {total_empty_system_zips}")
    print(f"======================================")


def perform_mame_search_and_output(systems_to_process, search_term, output_format, platform_key, platform_name_full, media_type, 
                                   enable_custom_cmd_per_title, emu_name, default_emu, default_emu_cmd_params, 
                                   output_file_path, driver_status_filter=None, emulation_status_filter=None, 
                                   show_systems_only=False, show_extra_info=False):
    """
    Performs the MAME listsoftware search and outputs results as table or YAML.
    """
    all_software_entries_for_yaml_processing = []
    
    # This dictionary will store all the relevant info for each system processed, including driver info
    # Structure: {system_name: {'machine_metadata': {...}, 'software_entries': [...]}}
    processed_system_info = {} 

    if not systems_to_process:
        print("[ERROR] No systems were determined for processing. Please check your arguments.")
        sys.exit(1)

    for current_system in systems_to_process:
        print(f"\n--- Processing system: {current_system} ---")

        # Get machine details including softlist filters, driver status, and description
        machine_softlist_filters, machine_metadata = get_machine_details_and_filters(current_system)
        
        # Apply driver status filters
        if driver_status_filter and machine_metadata["status"] != driver_status_filter:
            print(f"[INFO] Skipping system '{current_system}': Driver status '{machine_metadata['status']}' does not match required '{driver_status_filter}'.")
            continue
        if emulation_status_filter and machine_metadata["emulation"] != emulation_status_filter:
            print(f"[INFO] Skipping system '{current_system}': Emulation status '{machine_metadata['emulation']}' does not match required '{emulation_status_filter}'.")
            continue

        # Store machine metadata for this system
        processed_system_info[current_system] = {
            'machine_metadata': machine_metadata,
            'software_entries': [] # This will store (softlist_name_xml, system_name, swid, desc, publisher) for this system
        }

        listsoftware_succeeded = run_mame_command(["-listsoftware", current_system], TMP_SOFTWARE_XML_FILE)

        entries_from_parse_func = []
        if listsoftware_succeeded:
            entries_from_parse_func = parse_software_list_from_file(
                search=search_term,
                system_name=current_system,
                machine_softlist_filters=machine_softlist_filters
            )
            if entries_from_parse_func:
                processed_system_info[current_system]['software_entries'].extend(entries_from_parse_func)
            else:
                print(f"[INFO] No software entries found/matched for system '{current_system}' after parsing and filtering.")
        else:
            print(f"[INFO] MAME did not provide software list for '{current_system}' or command failed. It will be represented in the table and YAML.")


        if os.path.exists(TMP_SOFTWARE_XML_FILE):
            os.remove(TMP_SOFTWARE_XML_FILE)
        if os.path.exists(TMP_MACHINE_XML_FILE):
            os.remove(TMP_MACHINE_XML_FILE)

    print("\n--- Finished processing all systems ---")

    # Flatten software entries for YAML output (this list only contains entries that *had* software found)
    for sys_name, sys_data in processed_system_info.items():
        all_software_entries_for_yaml_processing.extend(sys_data['software_entries'])


    if systems_to_process: # Check if there's anything to output at all (after initial filters)
        if output_format == "table":
            table_display_data = []
            
            # Dynamically build headers based on show_extra_info
            headers = ["System"]
            if show_extra_info:
                headers.append("Manufacturer") # 2nd column
            headers.extend(["Softlist", "Software ID", "Title"])
            if show_extra_info:
                headers.append("Publisher") # Before Driver Status
            headers.extend(["Driver Status", "Emulation Status"])


            for sys_name in systems_to_process: # Iterate over the original sorted list of systems
                system_data_info = processed_system_info.get(sys_name)
                
                if system_data_info: # If the system was processed (not filtered out by driver status)
                    machine_metadata = system_data_info['machine_metadata']
                    driver_status = machine_metadata['status']
                    emulation_status = machine_metadata['emulation']
                    machine_description = machine_metadata['description']
                    machine_manufacturer = machine_metadata['manufacturer'] 

                    if show_systems_only:
                        row = [sys_name]
                        if show_extra_info:
                            row.append(machine_manufacturer)
                        row.extend(["N/A", "N/A", machine_description]) # Title is machine description
                        if show_extra_info:
                            row.append("N/A") # No publisher for system-only row
                        row.extend([driver_status, emulation_status])
                        table_display_data.append(row)
                    elif system_data_info['software_entries']:
                        # Add each software entry with its system's driver/emulation status
                        # The tuple from parse_software_list_from_file is (softlist_name, system_name, swid, desc, publisher)
                        for softlist_name, current_sys_name_from_entry, swid, desc, publisher in system_data_info['software_entries']:
                            row = [sys_name] 
                            if show_extra_info:
                                row.append(machine_manufacturer)
                            row.extend([softlist_name, swid, desc])
                            if show_extra_info:
                                row.append(publisher) # Add publisher here
                            row.extend([driver_status, emulation_status])
                            table_display_data.append(row)
                    else:
                        # Add a standalone row for systems with no software entries found/matched
                        row = [sys_name]
                        if show_extra_info:
                            row.append(machine_manufacturer)
                        row.extend(["N/A", "N/A", machine_description]) # Title is machine description
                        if show_extra_info:
                            row.append("N/A") # No publisher for N/A software
                        row.extend([driver_status, emulation_status])
                        table_display_data.append(row)
                # Else: system was filtered out by driver/emulation status, so it's not in processed_system_info, and won't be in table.
            
            if table_display_data:
                print(tabulate(table_display_data, headers=headers, tablefmt="github"))
                print(f"\nTotal rows across all systems: {len(table_display_data)}")
            else:
                print("[i] No matching software items found for table display after all filters. Some systems may be included in YAML as standalone.")
        elif output_format == "yaml":
            output_to_yaml_file(
                input_systems=systems_to_process, # Use the original list of systems
                all_software_entries=all_software_entries_for_yaml_processing, # Contains only systems with found software
                platform_key=platform_key,
                platform_name_full=platform_name_full,
                media_type=media_type,
                enable_custom_cmd_per_title=enable_custom_cmd_per_title,
                emu_name=emu_name,
                default_emu=default_emu,
                default_emu_cmd_params=default_emu_cmd_params,
                output_file_path=output_file_path
            )
    else:
        print(f"[i] No systems found for output after initial filtering or no matching software items found across any specified systems "
              f"with search term '{search_term}'." if search_term else "[i] No systems or matching software items found.")


def parse_good_emulation_drivers(exclude_arcade=False, machines_to_filter=None):
    """
    Runs mame -listxml, filters for emulation='good' drivers,
    and prints a table of machine name, description, year, and manufacturer, sorted by Manufacturer.
    If machines_to_filter is provided, only processes machines in that list.
    """
    print("[INFO] Fetching MAME machine drivers...")
    # Use cache for TMP_ALL_MACHINES_XML_FILE
    if not run_mame_command(["-listxml"], TMP_ALL_MACHINES_XML_FILE, use_cache=True): 
        print("[ERROR] Failed to get full MAME machine list. Cannot list good emulation drivers.")
        return

    good_drivers_data = []
    try:
        tree = ET.parse(TMP_ALL_MACHINES_XML_FILE)
        root = tree.getroot()

        for machine_element in root.findall("machine"):
            machine_name = machine_element.get("name")

            # Apply machines_to_filter if provided
            if machines_to_filter is not None and machine_name not in machines_to_filter:
                continue

            driver_element = machine_element.find("driver")
            if driver_element is not None and driver_element.get("emulation") == "good":
                # Apply exclude_arcade filter if enabled
                if exclude_arcade:
                    if machine_element.find("softwarelist") is None:
                        continue # Skip this machine as it's a pure arcade game (no softlist support)

                name = machine_element.get("name", "N/A")
                description = machine_element.findtext("description", "N/A").strip()
                year = machine_element.findtext("year", "N/A").strip()
                manufacturer = machine_element.findtext("manufacturer", "N/A").strip()
                
                good_drivers_data.append([name, description, year, manufacturer])

    except ET.ParseError as pe:
        print(f"[!] XML parse error for '{TMP_ALL_MACHINES_XML_FILE}': {pe}. Content might be malformed XML.")
    except Exception as e:
        print(f"[!] Unexpected error parsing XML for good emulation drivers: {e}")
    finally:
        # Don't remove TMP_ALL_MACHINES_XML_FILE here if it's cached, as it's meant to persist.
        pass
    
    if good_drivers_data:
        good_drivers_data.sort(key=lambda x: x[3]) # Sort by Manufacturer
        
        info_string = ""
        if machines_to_filter is not None:
            info_string += " (Filtered by external list)"
        if exclude_arcade:
            info_string += " (Softlist Capable Only)"

        print(f"\n===== MAME Machines with 'Good' Emulation Status{info_string} =====")
        headers = ["Machine Name", "Description", "Year", "Manufacturer"]
        print(tabulate(good_drivers_data, headers=headers, tablefmt="github"))
        print(f"\nTotal 'Good' emulation drivers found: {len(good_drivers_data)}")
    else:
        print(f"[i] No MAME machines with 'good' emulation status found matching the criteria.")


def parse_mess_ini_machines(ini_path):
    """
    Parses the MESS.ini file and extracts machine names from the [ROOT_FOLDER] section.
    Returns a set of machine names.
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
                if line.upper().startswith('[ROOT_FOLDER]'): # Case-insensitive check
                    in_root_folder_section = True
                    continue
                elif line.startswith('[') and line.endswith(']'): # New section starts
                    in_root_folder_section = False
                
                if in_root_folder_section and line and not line.startswith(';'): # Not empty and not a comment
                    machines.add(line.split(';')[0].strip()) # Take part before comment
        print(f"[INFO] Loaded {len(machines)} machines from '{ini_path}'.")
    except Exception as e:
        print(f"[ERROR] Error parsing MESS.ini file '{ini_path}': {e}")
    return machines

def split_mame_xml_by_ini(mess_ini_path, output_xml_file):
    """
    Phase 1/3: Filters the full mame -listxml output by machines listed in MESS.ini.
    Outputs the filtered machines to a new XML file (e.g., tmp_mess.xml).
    """
    print("=== Processing Phase 1/3: Filtering mame.xml by MESS.ini entries ===")
    
    mess_machines_from_ini = parse_mess_ini_machines(mess_ini_path)
    if not mess_machines_from_ini:
        print("[ERROR] No machines loaded from MESS.ini or file not found. Cannot proceed with splitting.")
        return False

    # Use cache for TMP_ALL_MACHINES_XML_FILE
    print("[INFO] Fetching full MAME machine list (mame.xml)... This may take a moment.")
    if not run_mame_command(["-listxml"], TMP_ALL_MACHINES_XML_FILE, use_cache=True):
        print("[ERROR] Failed to get full MAME machine list. Cannot proceed with splitting.")
        return False

    filtered_machines_count = 0
    try:
        tree = ET.parse(TMP_ALL_MACHINES_XML_FILE)
        root = tree.getroot() # <mame> root

        filtered_root = ET.Element("mame")
        for attr in ['build', 'debug', 'emulator', 'mameconfig']:
            if root.get(attr) is not None:
                filtered_root.set(attr, root.get(attr))

        for machine_element in root.findall("machine"):
            machine_name = machine_element.get("name")
            if machine_name in mess_machines_from_ini:
                filtered_root.append(machine_element)
                filtered_machines_count += 1
        
        filtered_tree = ET.ElementTree(filtered_root)
        filtered_tree.write(output_xml_file, encoding="utf-8", xml_declaration=True)
        
        print(f"[INFO] Phase 1 complete: Filtered {filtered_machines_count} machines into '{output_xml_file}'.")
        return True

    except ET.ParseError as pe:
        print(f"[ERROR] XML parse error during Phase 1: {pe}. Problem with '{TMP_ALL_MACHINES_XML_FILE}'.")
    except Exception as e:
        print(f"[ERROR] Unexpected error during Phase 1: {e}")
    finally:
        # Don't remove TMP_ALL_MACHINES_XML_FILE here if it's cached, as it's meant to persist.
        pass
    return False

def split_mess_xml_by_softwarelist(input_xml_file, softlist_output_file, nosoftlist_output_file):
    """
    Phase 2/3: Splits an XML file (e.g., tmp_mess.xml) into two new XML files:
    - one for machines that contain a <softwarelist> tag (mess-softlist.xml)
    - one for machines that do not contain a <softwarelist> tag (mess-nosoftlist.xml)
    """
    print("=== Processing Phase 2/3: Splitting mess.xml by softwarelist capability ===")
    
    if not os.path.exists(input_xml_file):
        print(f"[ERROR] Input XML file '{input_xml_file}' not found. Cannot proceed with splitting by softwarelist.")
        return False

    softlist_count = 0
    nosoftlist_count = 0

    softlist_root = ET.Element("mame")
    nosoftlist_root = ET.Element("mame")

    try:
        tree = ET.parse(input_xml_file)
        root = tree.getroot()

        for attr in ['build', 'debug', 'emulator', 'mameconfig']:
            if root.get(attr) is not None:
                softlist_root.set(attr, root.get(attr))
                nosoftlist_root.set(attr, root.get(attr))

        for machine_element in root.findall("machine"):
            if machine_element.find("softwarelist") is not None:
                softlist_root.append(machine_element)
                softlist_count += 1
            else:
                nosoftlist_root.append(machine_element)
                nosoftlist_count += 1
        
        softlist_tree = ET.ElementTree(softlist_root)
        softlist_tree.write(softlist_output_file, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] Phase 2 complete: Written {softlist_count} softlist-capable machines to '{softlist_output_file}'.")

        nosoftlist_tree = ET.ElementTree(nosoftlist_root)
        nosoftlist_tree.write(nosoftlist_output_file, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] Phase 2 complete: Written {nosoftlist_count} non-softlist-capable machines to '{nosoftlist_output_file}'.")
        
        return True

    except ET.ParseError as pe:
        print(f"[ERROR] XML parse error during Phase 2: {pe}. Problem with '{input_xml_file}'.")
    except Exception as e:
        print(f"[ERROR] Unexpected error during Phase 2: {e}")
    finally:
        if os.path.exists(input_xml_file):
            os.remove(input_xml_file) # Clean up the intermediate tmp_mess.xml
    return False

# Function to run the entire splitting process
def run_split_command(args):
    """Orchestrates the splitting of mame.xml based on mess.ini and softwarelist capability."""
    # Phase 1
    if not split_mame_xml_by_ini(args.mess_ini, TMP_MESS_XML_FILE):
        print("[ERROR] Phase 1 failed. Aborting splitting process.")
        return

    # Phase 2
    if not split_mess_xml_by_softwarelist(TMP_MESS_XML_FILE, TMP_MESS_SOFTLIST_XML_FILE, TMP_MESS_NOSOFTLIST_XML_FILE):
        print("[ERROR] Phase 2 failed. Aborting splitting process.")
        return
    
    print("\n=== Splitting process complete! ===")
    print(f"Generated: '{TMP_MESS_SOFTLIST_XML_FILE}' (Softlist-capable machines from MESS.ini)")
    print(f"Generated: '{TMP_MESS_NOSOFTLIST_XML_FILE}' (Non-softlist machines from MESS.ini)")


def main():
    parser = argparse.ArgumentParser(
        description="MAME Software & ROM Management Tool.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # 1. 'search' subcommand (now has nested subparsers)
    search_parser = subparsers.add_parser("search", help="Search MAME systems and generate YAML/table.")
    search_subparsers = search_parser.add_subparsers(dest="search_mode", required=True, help="How to specify systems for search.")

    # 1a. 'search by-name' mode
    by_name_parser = search_subparsers.add_parser("by-name", help="Search systems by explicit names or fuzzy prefix.")
    by_name_parser.add_argument(
        "systems",
        nargs='*',
        default=[],
        help="One or more MAME system short names (e.g., 'ekara', 'nes')."
    )
    by_name_parser.add_argument(
        "search_term",
        nargs='?',
        default="",
        help="Optional: Search term for software ID or description. Applied to ALL specified systems."
    )
    by_name_parser.add_argument(
        "--fuzzy",
        help="Optional: Prefix to fuzzy match MAME system names (e.g., 'jak_'). All MAME machines starting with this prefix will be added to the list of systems to process. Can be used in conjunction with explicit 'systems' arguments."
    )
    by_name_parser.add_argument(
        "--exclude-systems",
        nargs='+',
        default=[],
        help="Space-separated list of MAME system short names to explicitly exclude from processing. These systems will be removed even if matched by --fuzzy or provided explicitly."
    )
    by_name_parser.add_argument(
        "--limit",
        type=int,
        help="Optional: Limit the number of systems processed to this integer value (for testing)."
    )
    # Common YAML Output Specific Arguments for 'search by-name'
    by_name_parser.add_argument(
        "--output-format",
        choices=["table", "yaml"],
        default="table",
        help="Output format: 'table' (default) or 'yaml'."
    )
    by_name_parser.add_argument(
        "--output-file",
        default=SYSTEM_SOFTLIST_YAML_FILE,
        help=f"Path to the output YAML file. Defaults to '{SYSTEM_SOFTLIST_YAML_FILE}'."
    )
    by_name_parser.add_argument(
        "--platform-key",
        help="[Required for YAML Output] The top-level key for the platform in the YAML (e.g., 'jakks-tv-game')."
    )
    by_name_parser.add_argument(
        "--platform-name-full",
        help="[Required for YAML Output] The full, descriptive name of the platform (e.g., 'JAKKS Pacific TV Game')."
    )
    by_name_parser.add_argument(
        "--media-type",
        help="[Required for YAML Output] The type of media used by the platform (e.g., 'cart', 'disk', 'cdrom')."
    )
    by_name_parser.add_argument(
        "-ect", "--enable-custom-cmd-per-title",
        action="store_true",
        help="Set 'enable_custom_command_line_param_per_software_id: true' for the platform entry. Defaults to false if not set."
    )
    by_name_parser.add_argument(
        "-en", "--emu-name",
        help="Sets the 'emulator.name' (e.g., 'MAME (Cartridge)'). If specified, the 'emulator' block is added."
    )
    by_name_parser.add_argument(
        "-de", "--default-emu",
        action="store_true",
        help="Set 'emulator.default_emulator: true'. Requires --emu-name. Defaults to false if not set."
    )
    by_name_parser.add_argument(
        "-dec", "--default-emu-cmd-params",
        help="Sets 'emulator.default_command_line_parameters' (e.g., '-keyboardprovider dinput'). Requires --emu-name."
    )
    # Arguments for driver status filtering (specific to search command overall)
    by_name_parser.add_argument(
        "--driver-status",
        choices=["good", "imperfect", "preliminary", "unsupported"],
        help="Filter machines by driver 'status' (e.g., 'good', 'preliminary')."
    )
    by_name_parser.add_argument(
        "--emulation-status",
        choices=["good", "imperfect", "preliminary", "unsupported"],
        help="Filter machines by driver 'emulation' status (e.g., 'good', 'preliminary')."
    )
    by_name_parser.add_argument(
        "--show-systems-only",
        action="store_true",
        help="[For Table Output] Only show one row per system, even if it has software. "
             "Software ID and Softlist columns will be 'N/A', Title column will be machine description."
    )
    by_name_parser.add_argument(
        "--show-extra-info",
        action="store_true",
        help="[For Table Output] Show additional columns: System Manufacturer (2nd col) and Software Publisher (before Driver Status)."
    )


    # 1b. 'search by-xml' mode
    by_xml_parser = search_subparsers.add_parser("by-xml", help="Search systems from a generated XML file (e.g., mess-softlist.xml).")
    by_xml_parser.add_argument(
        "xml_filepath",
        help="Path to the XML file containing machine definitions (e.g., mess-softlist.xml, mess-nosoftlist.xml)."
    )
    by_xml_parser.add_argument(
        "search_term",
        nargs='?',
        default="",
        help="Optional: Search term for software ID or description. Applied to ALL systems from the XML file."
    )
    by_xml_parser.add_argument(
        "--limit",
        type=int,
        help="Optional: Limit the number of systems processed to this integer value (for testing)."
    )
    # Common YAML Output Specific Arguments for 'search by-xml' (with default overrides)
    by_xml_parser.add_argument(
        "--output-format",
        choices=["table", "yaml"],
        default="yaml", # Default to YAML for XML output
        help="Output format: 'table' or 'yaml' (default)."
    )
    by_xml_parser.add_argument(
        "--output-file",
        default=SYSTEM_SOFTLIST_YAML_FILE,
        help=f"Path to the output YAML file. Defaults to '{SYSTEM_SOFTLIST_YAML_FILE}'."
    )
    by_xml_parser.add_argument("--platform-key", help="Overrides auto-set platform key (e.g., 'mess-softlist').")
    by_xml_parser.add_argument("--platform-name-full", help="Overrides auto-set platform name (e.g., 'MESS (Softlist Capable)').")
    by_xml_parser.add_argument("--media-type", default="cart", help="Overrides auto-set media type (default: 'cart').")
    by_xml_parser.add_argument("-ect", "--enable-custom-cmd-per-title", action="store_true", help="Overrides auto-set enable_custom_cmd_per_title.")
    by_xml_parser.add_argument("-en", "--emu-name", default="MAME (Cartridge)", help="Overrides auto-set emulator name (default: 'MAME (Cartridge)').")
    by_xml_parser.add_argument("-de", "--default-emu", action="store_true", default=True, help="Overrides auto-set default emulator (default: true).")
    by_xml_parser.add_argument("-dec", "--default-emu-cmd-params", default="-keyboardprovider dinput", help="Overrides auto-set default command parameters (default: '-keyboardprovider dinput').")
    # Arguments for driver status filtering (specific to search command overall)
    by_xml_parser.add_argument(
        "--driver-status",
        choices=["good", "imperfect", "preliminary", "unsupported"],
        help="Filter machines by driver 'status' (e.g., 'good', 'preliminary')."
    )
    by_xml_parser.add_argument(
        "--emulation-status",
        choices=["good", "imperfect", "preliminary", "unsupported"],
        help="Filter machines by driver 'emulation' status (e.g., 'good', 'preliminary')."
    )
    by_xml_parser.add_argument(
        "--show-systems-only",
        action="store_true",
        help="[For Table Output] Only show one row per system, even if it has software. "
             "Software ID and Softlist columns will be 'N/A', Title column will be machine description."
    )
    by_xml_parser.add_argument(
        "--show-extra-info",
        action="store_true",
        help="[For Table Output] Show additional columns: System Manufacturer (2nd col) and Software Publisher (before Driver Status)."
    )


    # 2. 'copy-roms' subcommand
    copy_parser = subparsers.add_parser("copy-roms", help="Copy/create ROM zips based on system_softlist.yml.")
    copy_parser.add_argument(
        "--input-file",
        default=SYSTEM_SOFTLIST_YAML_FILE,
        help=f"Path to the input YAML file to read for copying. Defaults to '{SYSTEM_SOFTLIST_YAML_FILE}'."
    )

    # 3. 'list-good-emulation' subcommand
    list_good_parser = subparsers.add_parser("list-good-emulation", help="List MAME machines with 'good' emulation status.")
    list_good_parser.add_argument(
        "--exclude-arcade",
        action="store_true",
        help="Excludes machines that do not have a software list defined (typically arcade machines)."
    )

    # 4. 'mess' subcommand
    mess_parser = subparsers.add_parser("mess", help="Commands specific to MESS (softlist-capable systems).")
    mess_subparsers = mess_parser.add_subparsers(dest="mess_command", required=True, help="MESS specific actions.")

    # 4a. 'mess list-good-emulation' action
    mess_list_good_parser = mess_subparsers.add_parser("list-good-emulation", help="List MESS machines from mess.ini with 'good' emulation status.")
    mess_list_good_parser.add_argument(
        "--exclude-arcade",
        action="store_true",
        help="Excludes machines that do not have a software list defined (typically arcade machines). (Already filtered by mess.ini)"
    )
    mess_list_good_parser.add_argument(
        "--mess-ini",
        default=MESS_INI_PATH,
        help=f"Path to the MESS.ini file. Defaults to '{MESS_INI_PATH}'."
    )
    
    # 5. 'split' subcommand
    split_parser = subparsers.add_parser("split", help="Generate filtered MAME XMLs based on MESS.ini and softwarelist capability.")
    split_parser.add_argument(
        "--mess-ini",
        default=MESS_INI_PATH,
        help=f"Path to the MESS.ini file to filter machines. Defaults to '{MESS_INI_PATH}'."
    )


    args = parser.parse_args()

    # --- Dispatch commands ---
    if args.command == "search":
        # Determine systems to process based on search_mode
        systems_to_process = []
        
        # Default values for platform info (can be overridden by explicit CLI args)
        platform_key = args.platform_key
        platform_name_full = args.platform_name_full
        media_type = args.media_type
        enable_custom_cmd_per_title = args.enable_custom_cmd_per_title
        emu_name = args.emu_name
        default_emu = args.default_emu
        default_emu_cmd_params = args.default_emu_cmd_params
        
        # Store filters for driver/emulation status (common to both search modes)
        driver_status_filter = args.driver_status
        emulation_status_filter = args.emulation_status
        
        # Store --show-systems-only and --show-extra-info flags (common to both search modes for table output)
        show_systems_only_flag = args.show_systems_only 
        show_extra_info_flag = args.show_extra_info 

        if args.search_mode == "by-name":
            processed_systems_set = set(args.systems)
            if args.fuzzy:
                fuzzy_matches = get_all_mame_systems_by_prefix(args.fuzzy)
                if fuzzy_matches:
                    processed_systems_set.update(fuzzy_matches)
                    print(f"[INFO] Found {len(fuzzy_matches)} systems matching '{args.fuzzy}'.")
                else:
                    print(f"[INFO] No systems found matching '--fuzzy {args.fuzzy}'.")
                    
            if args.exclude_systems:
                initial_count = len(processed_systems_set)
                for excl_sys in args.exclude_systems:
                    if excl_sys in processed_systems_set:
                        processed_systems_set.remove(excl_sys)
                        print(f"[INFO] Excluded system '{excl_sys}' from processing.")
                if len(processed_systems_set) < initial_count:
                    print(f"[INFO] {initial_count - len(processed_systems_set)} systems excluded.")

            systems_to_process = sorted(list(processed_systems_set))

            # Apply --limit here for by-name mode
            if args.limit is not None and args.limit >= 0:
                print(f"[INFO] Limiting processing to {args.limit} systems.")
                systems_to_process = systems_to_process[:args.limit]
            elif args.limit is not None and args.limit < 0:
                 parser.error("Value for --limit cannot be negative.")


            search_term_for_core = args.search_term

            # Validation specific to by-name mode for YAML output
            if args.output_format == "yaml":
                if not all([platform_key, platform_name_full, media_type]):
                    parser.error("For 'search by-name' with YAML output, --platform-key, --platform-name-full, and --media-type are required.")
                if not systems_to_process:
                    parser.error("You must specify at least one system (explicitly or via --fuzzy) for 'search by-name'.")

        elif args.search_mode == "by-xml":
            systems_to_process = sorted(list(get_all_mame_systems_from_xml_file(args.xml_filepath)))
            search_term_for_core = args.search_term

            # Apply --limit here for by-xml mode
            if args.limit is not None and args.limit >= 0:
                print(f"[INFO] Limiting processing to {args.limit} systems.")
                systems_to_process = systems_to_process[:args.limit]
            elif args.limit is not None and args.limit < 0:
                 parser.error("Value for --limit cannot be negative.")


            # Auto-set/override platform details based on XML filename
            xml_filename_base = os.path.basename(args.xml_filepath)
            
            auto_platform_key = os.path.splitext(xml_filename_base)[0]
            auto_platform_name = ""
            auto_enable_custom_cmd_per_title = False
            auto_emu_name = "MAME (Cartridge)"
            auto_default_emu = True
            auto_default_emu_cmd_params = "-keyboardprovider dinput"
            
            if xml_filename_base == TMP_MESS_SOFTLIST_XML_FILE:
                auto_platform_name = "MESS (Softlist Capable)"
                auto_enable_custom_cmd_per_title = True
            elif xml_filename_base == TMP_MESS_NOSOFTLIST_XML_FILE:
                auto_platform_name = "MESS (No Softlist)"
                auto_enable_custom_cmd_per_title = False
            else:
                auto_platform_name = f"Custom XML: {xml_filename_base}" 
            
            # Apply auto-set values if not explicitly overridden by user
            platform_key = args.platform_key if args.platform_key else auto_platform_key
            platform_name_full = args.platform_name_full if args.platform_name_full else auto_platform_name
            media_type = args.media_type # This already has a default in by_xml_parser
            # For enable_custom_cmd_per_title, explicitly check if it was set to True, otherwise use auto-value
            enable_custom_cmd_per_title = args.enable_custom_cmd_per_title if args.enable_custom_cmd_per_title is True else auto_enable_custom_cmd_per_title
            # For emu_name, default_emu, default_emu_cmd_params, prioritize explicit over auto
            emu_name = args.emu_name if args.emu_name is not None else auto_emu_name
            default_emu = args.default_emu if args.default_emu is not False else auto_default_emu
            default_emu_cmd_params = args.default_emu_cmd_params if args.default_emu_cmd_params is not None else auto_default_emu_cmd_params


            if not systems_to_process:
                print(f"[ERROR] No systems found in '{args.xml_filepath}'. Cannot perform search.")
                sys.exit(1)
            
        # Common validation for YAML output (now placed after all info is gathered)
        if args.output_format == "yaml":
            if not all([platform_key, platform_name_full, media_type]):
                parser.error("For YAML output, derived or explicitly provided --platform-key, --platform-name-full, and --media-type are required.")
            if (default_emu or default_emu_cmd_params) and not emu_name:
                parser.error("--default-emu and --default-emu-cmd-params require --emu-name to be specified.")
            if not systems_to_process:
                parser.error("No systems to process after XML parsing and filtering.")
        
        # Call the core function with the now-determined arguments
        perform_mame_search_and_output(
            systems_to_process=systems_to_process,
            search_term=search_term_for_core,
            output_format=args.output_format,
            platform_key=platform_key,
            platform_name_full=platform_name_full,
            media_type=media_type,
            enable_custom_cmd_per_title=enable_custom_cmd_per_title,
            emu_name=emu_name,
            default_emu=default_emu,
            default_emu_cmd_params=default_emu_cmd_params,
            output_file_path=args.output_file,
            driver_status_filter=driver_status_filter, # Pass filters
            emulation_status_filter=emulation_status_filter, # Pass filters
            show_systems_only=show_systems_only_flag, # Pass the flag
            show_extra_info=show_extra_info_flag # Pass the flag
        )

    elif args.command == "copy-roms":
        args.output_file = args.input_file # Aligning arg name for function compatibility
        perform_rom_copy_operation(args)

    elif args.command == "list-good-emulation":
        parse_good_emulation_drivers(exclude_arcade=args.exclude_arcade)
        
    elif args.command == "mess":
        if args.mess_command == "list-good-emulation":
            mess_machines = parse_mess_ini_machines(args.mess_ini)
            if mess_machines:
                parse_good_emulation_drivers(
                    exclude_arcade=args.exclude_arcade,
                    machines_to_filter=mess_machines
                )
            else:
                print(f"[INFO] No machines found in MESS.ini or MESS.ini not found. No machines to list.")

    elif args.command == "split":
        run_split_command(args)

    # Final cleanup of any remaining temp files (excluding the generated mess-*.xml files which are outputs)
    for tmp_file in [TMP_SOFTWARE_XML_FILE, TMP_MACHINE_XML_FILE, TMP_ALL_MACHINES_XML_FILE, TMP_MESS_XML_FILE]:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

if __name__ == "__main__":
    main()