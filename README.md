# MESS Curator Tool

## Organize, Filter, and Curate Your MAME/MESS ROMsets with Ease

This tool is a powerful command-line utility designed for the meticulous curation of MAME's non-arcade "MESS" platforms and their associated software lists. It is the only tool of its kind that provides the flexibility to parse, filter, and group any MAME systems into custom platforms, which can then be used to build perfectly organized ROM sets.

If you've ever wanted to separate your TV Games, Handhelds, or obscure Consoles from your main MAME set, this is the tool you need.

This tool allows you to:

*   **Intelligently filter** MAME's vast machine list by name, fuzzy prefix, description, driver status, and emulation status.
*   **Auto-generate structured YAML** configuration files (`system_softlist.yml`) for platforms, complete with systems, their associated software lists, and even individual software IDs.
*   **Copy and organize** ROMs into a curated folder structure, creating dummy `.zip` files for missing titles or standalone systems.
*   **Pre-process MAME's XML data** by filtering for MESS systems (non-arcade) and splitting them into "softlist-capable" and "non-softlist" categories, significantly speeding up subsequent operations.
*   **List "good" emulation drivers** for easy discovery of well-supported systems.
*   **Provide detailed table outputs** for various data views directly from your YAML or MAME's XML.
*   **Manage program configurations** easily via a `config.yaml` file or command-line arguments.

## Companion Tool to my Launchbox Plug in - `MESS Curated Softlist Importer`

The primary purpose of this tool is to generate a `system_softlist.yml` file, which acts as a direct input for my first Launchbox Plugin - [MESS Curated Softlist ROM Importer plugin for LaunchBox](https://github.com/dsync89/lb-mess-curated-platform-softlist-importer).

The workflow is simple:

1. Use this tool to filter a list of platforms that you want into `system_softlist.yml` file.
2. Use the `copy-roms` command to create a curated ROM set based on the YAML file.
3. Use my LaunchBox plugin to import your games, which reads the generated `system_softlist.yml` 
to automatically add platforms, emulators, metadata, clones, mark broken games, and per title custom MAME command-line parameters in LaunchBox.

## Key Features

- **Flexible System Searching**:
  - By Name: Specify systems directly or use fuzzy prefixes (e.g., `jak_` to find all JAKKS Pacific systems).
  - By XML File: Use pre-filtered XMLs (like `mess-softlist.xml`) as a starting point.
  - By Filter: Discover systems by searching their descriptions (e.g., find all systems with "handheld" in their description).

- **Detailed Filtering**: Narrow down results by driver status (good, imperfect) and emulation status.

- **Custom Platform Generation**: Group any combination of systems into a single, cohesive platform entry in your YAML file.

- **Curated ROM Set Creation**: Automatically copy the required ROMs (or create dummy files for missing ones) into an organized folder structure that mirrors your YAML.

- **GUI**: A GUI for those that prefer graphics.

- **Initial Setup Wizard***: A guided, interactive setup to configure all necessary paths, making first-time use easy.


## Why This Tool is Unique

Many existing tools focus on full ROMset validation or arcade-only management. MESS Curator specifically targets:

*   **MESS Systems Integration:** Explicitly handles and filters non-arcade MAME systems.
*   **Softlist Granularity:** Generates YAML that correctly distinguishes between multiple softlists per system, and individual software IDs/titles within each.
*   **Frontend-Friendly Output:** The YAML output (`system_softlist.yml`) is designed to be easily parseable by external tools (like my LaunchBox plugin) for automated import of platform and game metadata into Launchbox front-end.
*   **Smart Caching:** Avoids repeatedly running slow `mame -listxml` commands by caching generated XMLs (`mame.xml`, `mess.xml`), making subsequent operations much faster.
*   **Flexible Filtering:** Allows highly specific filtering by description, driver status, emulation status, and softlist capability, enabling users to build niche collections (e.g., "all good emulation handhelds," "all x-in-1 systems").


## Dependencies

MESS Curator requires the `mess.ini` maintained by the good Italian community at https://github.com/AntoPISA/MAME_SupportFiles that you put into `MAME\folders`. This `mess.ini` file is critical as it contains a list of machine/system names that is non-Arcade that would otherwise impossible to determined using the `mame.xml` that you generated using `mame -listxml` itself, as it does not contain any fields that indicate whether a system is Arcade or Non-Arcade.

Note that the repo might not be updated as quickly as the MAME release. 

Take MAME 0.278 for example, it was released a week before 2025-07-07, but as of 2025-07-07 that repo still is yet to be updated with the `mess.ini` for 0.278 set. Fortunately you can simply use the `mess.ini` from the 0.277 release as the changes might be minor and you will probably not missing anything.

## System-Softlist YAML

While you may use this tool as a lister to quickly filter out those systems/softlist that you like, or generate CSV then filter yourself, the most powerful power or the main motivation for this tool is to generate a YAML file, which I aptly called **System-Softlist YAML** that contains a list of systems, softlists, metadata, etc. that is later on used to readily import these as Platforms in Launcbhox using my [Launchbox MESS Curator Plugin] tool.

### Structure

An example of a System-Softlist YAML contains general common fields like:

```
jakks-pacific-tv-game:  # <-- a unique human readable key that identify a platform. Named as <MANUFACTURER>-<SYSTEM_NAME>
  platform:
    name: JAKKS Pacific TV Game # <-- Human readable Platform Name. This is used to create Platform Name in Launchbox when importing using my [Launchbox MESS Curator Plugin] tool
  platform_category:
  - Consoles
  - MESS (TV Games)
  media_type: cart
  enable_custom_command_line_param_per_software_id: true
  emulator:
    name: MAME (Cartridge)
    default_emulator: true
    default_command_line_parameters: -keyboardprovider dinput
  system: # <-- a list of system only or system with softlist
  - jak_batm # <-- a system without a `software_lists` simply means that it does not support software list.
  - jak_bbh
  - jak_bbsf
    ...
  - jak_disf: # <-- A system that support software list
      software_lists:
      - softlist_name: jakks_gamekey_dy
        software_id:
        - sbwlgoof
        - stenfcha
        - stenfchs
```

Some systems such as Computers might contain several softlists in which you want to apply the same command line params for all titles in that softlists. E.g. Acorn Electron.

These are defined in `software_configs` key which is optional, such as
```
      software_configs:  
        <SOFTLIST_NAME>: # this must match with the softlist name that the system support
          _default_config: # the default fixed key that is used to hint the cmd line that is applied to all titles within this softlist
            command_line_parameters: <value here will be globally applied to all softlist titles within <SOFTLIST_NAME>>
          <SOFTLIST_TITLE> # softlist title specific options that will take precedence/overwrite those that are defined in `_default_config`.
            command_line_parameters: <value here will overwrite the cmd line param in `_default_config`
```

There are times when you might need to use `software_configs.<SOFTLIST_TITLE>` for specific games for a softlist instead of a global cmd line that get applied to all games for that softlist. A notable one is Acorn Atom systems where each game require different cmd line param where the game name cannot be simply determined from the rom filename itself.

```
acorn-atom:
  platform:
    name: Acorn Atom
  platform_category:
  - Computers
  - MESS (Computers)
  - MESS (System w/ Softlist)
  media_type: floppy
  enable_custom_command_line_param_per_software_id: false
  emulator:
    name: MAME (Floppy)
    default_emulator: true
    default_command_line_parameters: -keyboardprovider dinput atom -autoboot_delay
      "2" -autoboot_command "DOS\nCAT\n*RUN"" -flop1
  system:
  - atom:
      software_lists:
      - softlist_name: atom_flop
        software_id:
        - chuckie
        - dosutils
        - egghead
        - f14
        - gala
        - galxians
        - hardhath
        - hypervpr
        - jetsetmn
        - joeblade
        - jsw
        - jsw2
        - jungle
        - manicmin
        - repton
      software_configs:
        atom_flop:
          joeblade: # <-- define a per game cmd line param
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"JOE"\n -autoboot_delay
              1 -flop1
          egghead:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"EHRUN"\n -autoboot_delay
              1 -flop1
          jsw:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"JSWRUN"\n -autoboot_delay
              1 -flop1
          gala:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"CGALA"\n -autoboot_delay
              1 -flop1
          hardhath:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"LOADER"\n -autoboot_delay
              1 -flop1
          jungle:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"JUNGLE"\n -autoboot_delay
              1 -flop1
          hypervpr:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"LOADER"\n -autoboot_delay
              1 -flop1
          f14:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"F14RUN"\n -autoboot_delay
              1 -flop1
          galxians:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"GALAXI"\n -autoboot_delay
              1 -flop1
          chuckie:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"CCHUCK"\n -autoboot_delay
              1 -flop1
          jsw2:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"JSW2RUN"\n -autoboot_delay
              1 -flop1
          repton:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"REPLOAD"\n -autoboot_delay
              1 -flop1
          manicmin:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"MMRUN"\n -autoboot_delay
              1 -flop1
          jetsetmn:
            command_line_parameters: atom -ab *DOS\n*CAT\n*RUN"LOADER"\n -autoboot_delay
              1 -flop1
```

Here's another example of a system, Acorn Electron that use the same global cmd line param for each titles per softlist, and there is no need for specific cmd line per titles as that would be a LOT to cover and unnecessary.

```
acorn-electron:
  platform:
    name: Acorn Electron
  platform_category:
  - Computers
  - MESS (Computers)
  - MESS (System w/ Softlist)
  media_type: cass
  enable_custom_command_line_param_per_software_id: false
  emulator:
    name: MAME (Cassette)
    default_emulator: true
    default_command_line_parameters: -keyboardprovider dinput electron -skip_gameinfo
      -autoboot_delay "2" -autoboot_command "*tape\nchain""""""\n" -cass
  system:
  - electron:
      software_lists:
      - softlist_name: bbc_cass
        software_id:
        - 9cardbd1
        - 9cardbd2
          ...
      - softlist_name: electron_cart
        software_id:
        - abr
        - abr104
          ...
      - softlist_name: electron_cass
        software_id:
        - 3dbombal
        - 3ddotty
          ...
      - softlist_name: electron_flop
        software_id:
        - 9cardbd1
        - 9cardbd2
          ...
      software_configs:
        bbc_cass:
          _default_config: # <-- use the same cmd line param for all titles in this softlist
            command_line_parameters: electron -skip_gameinfo -autoboot_delay 2 -autoboot_command
              *TAPE\nCHAIN""""""\n -cass
          test:
            command_line_parameters: electron -skip_gameinfo -autoboot_delay 2 -autoboot_command
              *TAPE\nCHAIN""""""\n TEST -cass
        electron_cart:
          _default_config:
            command_line_parameters: electron -cart
        electron_cass:
          _default_config:
            command_line_parameters: electron -skip_gameinfo -autoboot_delay 2 -autoboot_command
              *TAPE\nCHAIN""""""\n -cass
        electron_flop:
          _default_config:
            command_line_parameters: electron -skip_gameinfo -autoboot_delay 2 -autoboot_command
              "cat\n\n\n\n\n\nrun !boot\n" -flop
```

## Preset System-Softlist YAML

In case you don't want to generate the system-softlist YAML yourself, I had meticulously curated a list of notable MESS systems that I personally like to have in my collections and you can use it as-is. The systems are chosen based on one of the following critieria:

- Obscurity: Less known system or manufacturer are prioritize as I am interested to know more about it. 
- Playable titles: The system must have at least one or few playable titles.
- Well known manufacturer: This might contradict with the first criteria, but if it's from a well known Manufacturer you bet to see it in the list, especially those LCD Handhelds from well known manufacturers like Konami, Nintendo, and Tiger.com

I do welcome contribution to these listings as time goes if you think more systems should be added. Since I used Launchbox as my front-end, I include all games (both broken and working) and then use my [Launchbox MESS Curator Plugin] tool to mark those games as Broken and add clones as additional apps. 

You can extend or generate your own YAML Files.

## Installation

1.  **Python 3.x:** Ensure you have Python 3.7+ installed. You can download it from [python.org](https://www.python.org/downloads/).
2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/dsync89/mess-curator.git
    cd mess-curator/src 
    ```
3.  **Install Dependencies:**
    ```bash
    pip install PyYAML tabulate
    ```
4.  **MAME:** Ensure you have a MAME installation (0.277+ recommended) and know its executable path.

### Configuration

Before running most commands, the tool needs to know where your MAME executable, ROMs, and output files are located.

**First Run (Guided Setup):**
The very first time you run `mess_curator.py` (and `config.yaml` doesn't exist), it will automatically launch a guided setup process:

```bash
python src\mess_curator.py
```

Follow the prompts to set your paths. It will attempt to auto-detect sensible defaults.

**Viewing Current Configuration:**

```
python src\mess_curator.py config    
```

**Setting Specific Paths (Command Line):**

```
python src\mess_curator.py config --set-mame-exe-path "C:\Programs\LaunchBox\Emulators\MAME 0.277\mame.exe"
python src\mess_curator.py config --set-softlist-rom-dir "C:\Programs\LaunchBox\Emulators\MAME 0.277\roms"
python src\mess_curator.py config --set-output-rom-dir "C:\Users\Gary\Documents\Github-dsync89\mess-curator\out\mame_curated_romset"
python src\mess_curator.py config --set-mess-ini-path "C:\Programs\LaunchBox\Emulators\MAME 0.277\folders\mess.ini"
python src\mess_curator.py config --set-system-softlist-yaml-file "C:\Users\Gary\Documents\Github-dsync89\mess-curator\data\my_platforms.yml"
```

*(Paths shown are examples, adjust to your system. Note: `MAME_EXECUTABLE's` parent directory is used to guess mess.ini default path)*

### Notes 

For the best performance, the tool relies on filtered XML files for MESS (non-Arcade) instead of the full systems `mame.xml`. After the initial setup, you will be prompted to generate them. You can also do this manually at any time:

```
python src\mess_curator.py split
```

This command will:

1. Generate `mame.xml` (a full machine list, which can take a few minutes).
2. Read your `mess.ini` to create a filtered `mess.xml` containing all non-Arcade systems.
3. Split `mess.xml` into `mess-softlist.xml` (systems with software lists) and `mess-nosoftlist.xml`.

## Usage

All commands follow a subcommand structure. Use `python src\mess_curator.py <command> -h` for specific help.

**Important Notes for Windows (PowerShell/CMD):**

If your paths or arguments contain spaces, enclose them in double quotes "like this".

When breaking a long command across multiple lines, use the backtick (`) at the end of each line (except the last one):

```
python src\mess_curator.py search by-xml `
    --output-format yaml `
    --platform-key my-platform `
    "../data/mess-softlist.xml"
```

---

### `split` Command: Generate Filtered MAME XMLs
This command is crucial for optimizing later search operations. It filters your entire `mame.xml` based on the systems in `mess.ini` and then splits the result.

```
python src\mess_curator.py split
```

Output Files (generated in the script's directory):
- `mame.xml`: (Full MAME machines list, cached for later use)
- `mess.xml`: (Machines listed in your mess.ini from mame.xml)
- `mess-softlist.xml`: (Machines from mess.xml that support software lists)
- `mess-nosoftlist.xml`: (Machines from mess.xml that do NOT support software lists)

Options:
- `--mess-ini <path>`: Specify a custom mess.ini file. (Defaults to configured path)

### `search` Command: Find Systems and Generate YAML/Table

The search command has nested subcommands (`by-name`, `by-xml`, `by-filter`) to specify how systems are chosen.

```
usage: mess_curator.py search [-h] {by-name,by-xml,by-filter,by-sourcefile} ...

positional arguments:
  {by-name,by-xml,by-filter,by-sourcefile}
                        How to specify systems for search.
    by-name             Search systems by explicit names or fuzzy prefix.
    by-xml              Search systems from a generated XML file (e.g., mess-softlist.xml).
    by-filter           Search MAME machines by their XML attributes (e.g., description).
    by-sourcefile       Search MAME machines by their driver source file (e.g., 'xavix.cpp').

options:
  -h, --help            show this help message and exit
```

**Common Options for `search` sub-subcommands:**

- `--output-format {table,yaml}`: Choose between a human-readable table (default for by-name/by-filter) or YAML (default for by-xml).

- `--output-file <path>`: Specify the output system_softlist.yml file path. (Defaults to configured path).

- `--limit <number>`: Limit the number of systems processed (useful for testing).

- `--driver-status {good,imperfect,preliminary,unsupported}`: Filter machines by their driver status.

- `--emulation-status {good,imperfect,preliminary,unsupported}`: Filter machines by their emulation status.

- `--show-systems-only`: (For table output) Show only one row per system (N/A for softlist/software ID, machine description for Title).

- `--show-extra-info`: (For table output) Add "Manufacturer" and "Publisher" columns.

**YAML Output Specific Options for `search` sub-subcommands:**

- `--platform-key <key>`: (Required) Top-level key for the platform in YAML.

- `--platform-name-full <name>`: (Required) Full descriptive name of the platform.

- `--media-type {cart,disk,cdrom,...}`: (Required) Media type for the platform.

- `-ect, --enable-custom-cmd-per-title`: Set enable_custom_command_line_param_per_software_id: true.

- `-en <name>, --emu-name <name>`: Set emulator.name.

- `-de, --default-emu`: Set emulator.default_emulator: true. (Requires -en)

- `-dec <params>, --default-emu-cmd-params <params>`: Set emulator.default_command_line_parameters. (Requires -en)

The most common way to search for systems.

Options Specific to search `by-name`:

- `systems`: Positional argument for explicit system names (e.g., `ekara`, `jak_batm`).

- `search_term`: Positional optional argument for software ID or description.

- `--fuzzy <prefix>`: Find all systems starting with this prefix (e.g., `jak_`).

- `--exclude-systems <names>`: Exclude specific systems from the list.

- `--input-xml <path>`: Source XML file to read machine definitions from. (Defaults to `mame.xml`) 

**Examples:**

- **Table output for a single system and its software:**

```
python src\mess_curator.py search by-name ekara --output-format table
```

- **YAML output for a specific platform:**

```
python src\mess_curator.py search by-name jpopira --output-format yaml `
    --platform-key jpopira-platform `
    --platform-name-full "Takara J-Popira Karaoke Systems" `
    --media-type cart
```

- **YAML output for multiple JAKKS systems (fuzzy search + exclude) with emulator details:**

```
python src\mess_curator.py search by-name `
    --platform-key jakks-pacific-tv-game `
    --platform-name-full "JAKKS Pacific TV Game" `
    --media-type cart `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (Cartridge)"  `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --fuzzy jak_ `
    --exclude-systems jak_pf jak_prft jak_s500 jak_smwm jak_ths jak_tink jak_totm jak_umdf `
    --input-xml ..\data\mame.xml # Use full mame.xml for fuzzy search
```

---

**Options Specific to `search by-xml`:**

- `xml_filepath`: Required positional argument for the XML file path.

- `search_term`: Positional optional argument for software ID or description.

- `--limit <number>`: Limit the number of systems processed.

**Examples:**

**Generate YAML for MESS systems with no softlist, limited to 5, with auto-defaults:**

```
python src\mess_curator.py search by-xml `
    --output-format yaml `
    --limit 5 `
    ..\data\mess-nosoftlist.xml # Assumes this file exists from 'split' command
```

*(This will automatically set platform-key, platform-name-full, enable-custom-cmd-per-title: false, etc.)*

- **Generate YAML for XaviXPort systems from mess.xml, with custom platform/emulator names:**

```
python src\mess_curator.py search by-xml `
    --output-format yaml `
    --platform-key xavixport `
    --platform-name-full "XaviXPORT Systems" `
    --media-type cart `
    --emu-name "MAME (Integrated)" `
    --default-emu `
    --default-emu-cmd-params "-joystickprovider dinput" `
    ..\data\mess.xml # Search within all MESS systems
    xavixport # This acts as a search_term to filter for XaviXPort systems
```

- **Table output for good emulation systems from mess-softlist.xml:**

```
python src\mess_curator.py search by-xml `
    --output-format table `
    --show-extra-info `
    --emulation-status good `
    ..\data\mess-softlist.xml
```

*(This will display softlist-capable systems from mess-softlist.xml that have "good" emulation status.)*

---

A powerful way to find specific types of machines based on their description or properties.

Options Specific to `search by-filter`:

- `description_term`: Required positional argument for text to search in machine descriptions.

- `--softlist-capable`: Only include machines that have a `<softwarelist>` tag.

- `--input-xml <path>`: Source XML file to read machine definitions from. (Defaults to `mame.xml`)

**Examples:**

- **Find "in-1" multigame systems from `mess.xml`, output to YAML:**

```
python src\mess_curator.py search by-filter "in-1" `
    --input-xml ..\data\mess.xml `
    --platform-key mess-filtered-all-in-one-systems `
    --platform-name-full "MESS (All-In-One Systems)" `
    --media-type cart `
    --enable-custom-cmd-per-title ` # Typically true for multi-games
    --emu-name "MAME (Cartridge)"  `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --output-file system_softlist.yml
```

*(Note: if searching for "X-in-1", use "in-1" or "in 1" as search terms. You can run by-filter multiple times and append to the same YAML file for different filters.)*

- **Find "XavixPort" systems (by description) from `mess.xml`:**

```
python src\mess_curator.py search by-filter "xavixport" `
    --input-xml ..\data\mess.xml `
    --platform-key xavixport `
    --platform-name-full "XaviXPORT" `
    --media-type cart `
    --emu-name "MAME (Cartridge)"  `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml
```

### `copy-roms` Command: Construct Your ROMset

Reads your `system_softlist.yml` and copies/creates dummy `.zip` if that is a system files in a structured output directory.

```
python src\mess_curator.py copy-roms --input-file system_softlist.yml
```

**Output Structure Example:**
`C:\temp\mame_curated_romsetv2\my_platform_key\system_name\softlist_name\software_id.zip`

**Options:**
- `--input-file <path>`: Specify the input `system_softlist.yml` file. (Defaults to configured path)
- `--platform-key PLATFORM_KEY`: (Optional) Copy ROMs only for a specific platform by its key.
- `--create-placeholder-zip`: Always create empty placeholder (dummy) zips which is about 22KB instead of copying from the source directory.
- `--dry-run`: Show what would be copied or created without modifying any files.

Note:
- I highly recommend using `--create-placeholder-zip` to create a dummy zip. Unlike most emulator that require taking the full ROM path as the input argument, MAME maintain its internal database of rom list and rom path, and the command line parameter only require the system or softlist name. 

### `table` Command: Display `system_softlist.yml` as Table

Parses and displays the contents of your `system_softlist.yml` in a detailed table.

```
python src\mess_curator.py table --platform-key nintendo-game-and-watch --mame-xml-source ..\data\mess.xml --show-extra-info
```

**Options:**

- `--platform-key <key>`: Display only a specific platform.

- `--input-file <path>`: Specify the input `system_softlist.yml`. (Defaults to configured path)

- `--mame-xml-source <path>`: MAME XML file to fetch system descriptions/statuses. (Defaults to `mame.xml`)

- `--show-systems-only`: Show only one row per system.

- `--show-extra-info`: Show Manufacturer and Publisher columns.

### `platform-info` Command: Display High-Level Platform Summary

Provides a high-level overview of platforms defined in your `system_softlist.yml`, including counts of systems, softlists, and software IDs.

```
python src\mess_curator.py platform-info
```

**Options:**

- `--platform-key <key>`: Display info for a specific platform only.

- `--input-file <path>`: Specify the input `system_softlist.yml`. (Defaults to configured path)

**Output Example:**

```
python.exe .\mess_curator.py platform-info --sort-by-col-num 2
[INFO] Configuration loaded from 'config.yaml'.

===== Displaying Platform Information from 'system_softlist.yml' =====

[INFO] Table sorted by column 2: 'Platform Name'.
| Platform Key                     | Platform Name                      | Platform Category                                      | Media Type   | Custom CMD per Title   | Emulator Name    | Default Emu   | Default Emu Cmd Params                                                                                                       |   # Systems |   # Softlists |   # Software IDs |
|----------------------------------|------------------------------------|--------------------------------------------------------|--------------|------------------------|------------------|---------------|------------------------------------------------------------------------------------------------------------------------------|-------------|---------------|------------------|
| acorn-archimedes                 | Acorn Archimedes                   | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput aa4401 -flop                                                                                        |           1 |             2 |              462 |
| acorn-atom                       | Acorn Atom                         | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput atom -autoboot_delay "2" -autoboot_command "DOS\nCAT\n*RUN"" -flop1                                 |           1 |             3 |               98 |
| acorn-electron                   | Acorn Electron                     | Computers, MESS (Computers), MESS (System w/ Softlist) | cartridge    | False                  | MAME (Cassette)  | True          | -keyboardprovider dinput electron -skip_gameinfo -autoboot_delay 2 -autoboot_command *tape\nchain""\n -cass                  |           1 |             5 |             1247 |
| amstrad-cpc                      | Amstrad CPC                        | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput cpc6128 -flop1                                                                                      |           1 |             2 |            26145 |
| amstrad-gx4000                   | Amstrad GX4000                     | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput gx4000 -cart                                                                                        |           1 |             1 |               32 |
| atari-xegs                       | Atari XEGS                         | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput xegs -cart                                                                                          |           1 |             4 |              587 |
| bbc-microcomputer-system         | BBC Microcomputer System           | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput bbcb -skip_gameinfo -flop1                                                                          |           1 |             4 |              799 |
| bally-astrocade                  | Bally Astrocade                    | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput astrocde -cart                                                                                      |           1 |             1 |              127 |
| bambino-handhelds-lcd            | Bambino Handhelds (LCD)            | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           8 |             0 |                0 |
| bandai-gundam-rx-78              | Bandai Gundam RX-78                | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput rx78 -cart                                                                                          |           1 |             2 |               28 |
| bandai-handhelds-lcd             | Bandai Handheld (LCD)              | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          21 |             0 |                0 |
| bandai-lets-tv-play              | Bandai Let's! TV Play              | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          23 |             0 |                0 |
| bandai-super-note-club           | Bandai Super Note Club             | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput snotec -cart                                                                                        |           1 |             2 |               16 |
| bandai-super-vision-8000         | Bandai Super Vision 8000           | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput sv8000 -cart                                                                                        |           1 |             1 |                7 |
| bandai-tamagotchi                | Bandai Tamagotchi                  | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           8 |             0 |                0 |
| bit-corp-gamate                  | Bit Corp Gamate                    | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput gamate -cart                                                                                        |           1 |             1 |               62 |
| camputers-lynx                   | Camputers Lynx                     | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput lynx128k -autoboot_delay "2" -autoboot_command "XROM\n\n\nEXT DIR\n\n\n\n\n\n\n\nEXT LOAD "" -flop1 |           1 |             2 |               87 |
| casio-loopy                      | Casio Loopy                        | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput casloopy -cart                                                                                      |           1 |             1 |               11 |
| casio-pv-1000                    | Casio PV-1000                      | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput pv1000 -cart                                                                                        |           1 |             1 |               29 |
| casio-pv-2000                    | Casio PV-2000                      | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput pv2000 -cart                                                                                        |           1 |             1 |               29 |
| coleco-adam                      | Coleco ADAM                        | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput adam -skip_gameinfo -flop1                                                                          |           1 |             5 |             1933 |
| coleco-handhelds-lcd             | Coleco Handheld (LCD)              | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           9 |             0 |                0 |
| commodore-vic-10                 | Commodore VIC-10                   | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput vic10 -cart                                                                                         |           1 |             1 |               28 |
| commodore-vic-20                 | Commodore VIC-20                   | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput vic1001 -cart                                                                                       |           1 |             2 |              255 |
| conny-tv-games                   | Conny TV Games                     | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          11 |             0 |                0 |
| creatronic-mega-duck             | Creatronic Mega Duck               | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput megaduck -cart                                                                                      |           1 |             1 |               26 |
| dragon                           | Dragon                             | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput dragon64 -cart                                                                                      |           1 |             6 |             1316 |
| eaca-eg2000-colour-genie         | EACA EG2000 Colour Genie           | Computers, MESS (Computers), MESS (System w/ Softlist) | cartridge    | False                  | MAME (Cassette)  | True          | -keyboardprovider dinput cgenie -autoboot_command \n\nCLOAD\n -autoboot_delay 1 -cass                                        |           1 |             1 |              257 |
| emerson-arcadia-2001             | Emerson Arcadia 2001               | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput arcadia -cart                                                                                       |           1 |             1 |               62 |
| entex-adventure-vision           | Entex Adventure Vision             | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput advision -skip_gameinfo -cart                                                                       |           1 |             1 |                5 |
| entex-handhelds-lcd              | Entex Handhelds (LCD)              | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          19 |             0 |                0 |
| epoch-game-pocket-computer       | Epoch Game Pocket Computer         | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput gamepock -cart                                                                                      |           1 |             1 |                6 |
| epoch-handhelds-lcd              | Epoch Handhelds (LCD)              | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           7 |             0 |                0 |
| epoch-super-cassette-vision      | Epoch Super Cassette Vision        | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput scv -cart                                                                                           |           1 |             1 |               32 |
| epoch-tv-games                   | Epoch TV Games                     | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          39 |             0 |                0 |
| epoch-tv-pc                      | Epoch TV PC                        | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           4 |             0 |                0 |
| exelvision-exl-100               | Exelvision EXL 100                 | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput exl100 -cart                                                                                        |           1 |             1 |               16 |
| exidy-sorcerer                   | Exidy Sorcerer                     | Computers, MESS (Computers), MESS (System w/ Softlist) | cartridge    | False                  | MAME (Cassette)  | True          | -keyboardprovider dinput sorcerer2 -autoboot_command LOG\n -autoboot_delay 3 -cass1                                          |           1 |             2 |              129 |
| funtech-super-acan               | Funtech Super Acan                 | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput supracan -cart                                                                                      |           1 |             1 |               12 |
| gakken-handhelds-lcd             | Gakken Handhelds (LCD)             | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          12 |             0 |                0 |
| gamepark-gp32                    | GamePark GP32                      | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput gp32                                                                                                |           1 |             1 |               38 |
| hartung-game-master              | Hartung Game Master                | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput gmaster -cart                                                                                       |           1 |             1 |               18 |
| hasbro-tv-games                  | Hasbro TV Games                    | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           9 |             0 |                0 |
| interton-vc-4000                 | Interton VC 4000                   | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput vc4000 -cart                                                                                        |           1 |             1 |               37 |
| jakks-pacific-tv-game            | JAKKS Pacific TV Game              | Consoles, MESS (TV Games)                              | cart         | True                   | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          62 |            13 |               36 |
| jakks-pacific-tv-motion-game     | JAKKS Pacific TV Motion Game       | Consoles, MESS (TV Games)                              | cart         | True                   | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           1 |             0 |                0 |
| jakks-pacific-telestory          | JAKKS Pacific Telestory            | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cartridge    | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput telestry -cart                                                                                      |           1 |             1 |               11 |
| joypalette-tv-games              | JoyPalette TV Games                | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           5 |             0 |                0 |
| jungletac-vii                    | JungleTac Vii                      | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput vii -cart                                                                                           |           1 |             1 |                2 |
| koei-pasogo                      | Koei PasoGo                        | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput pasogo -cart                                                                                        |           1 |             1 |                6 |
| konami-handhelds-lcd             | Konami Handhelds (LCD)             | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          20 |             0 |                0 |
| lexibook-tv-games                | Lexibook TV Games                  | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          13 |             0 |                0 |
| mattel-electronics-handhelds-lcd | Mattel Electronics Handhelds (LCD) | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          25 |             0 |                0 |
| mattel-hyperscan                 | Mattel Hyperscan                   | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cartridge    | False                  | MAME (CD)        | True          | -keyboardprovider dinput hyprscan -cdrom                                                                                     |           1 |             2 |              452 |
| mattel-intellivision-ecs         | Mattel Intellivision ECS           | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput intvecs -cart                                                                                       |           1 |             2 |              201 |
| memotech-mtx                     | Memotech MTX                       | Computers, MESS (Computers), MESS (System w/ Softlist) | cartridge    | False                  | MAME (Cassette)  | True          | -keyboardprovider dinput mtx512 -skip_gameinfo -autoboot_command load""\n -autoboot_delay 3 -cass                            |           1 |             5 |               78 |
| milton-bradley-handhelds-lcd     | Milton Bradley Handhelds (LCD)     | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          12 |             0 |                0 |
| nichibutsu-my-vision             | Nichibutsu My Vision               | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput myvision -cart                                                                                      |           1 |             1 |                4 |
| nintendo-famicombox              | Nintendo FamicomBox                | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput famibox                                                                                             |           1 |             0 |                0 |
| nintendo-game-and-watch          | Nintendo Game & Watch              | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          59 |             0 |                0 |
| nintendo-super-game-boy          | Nintendo Super Game Boy            | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           2 |             4 |             6894 |
| parker-brothers-handhelds-lcd    | Parker Brothers Handhelds (LCD)    | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          13 |             0 |                0 |
| philips-vg-5000                  | Philips VG 5000                    | Computers, MESS (Computers), MESS (System w/ Softlist) | cartridge    | False                  | MAME (Cassette)  | True          | -keyboardprovider dinput vg5k -skip_gameinfo -autoboot_command cload\n -autoboot_delay 3 -cass                               |           1 |             1 |               68 |
| philips-videopac-plus            | Philips Videopac+                  | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput videopac -cart                                                                                      |           1 |             0 |                0 |
| play-vision-tv-games             | Play Vision TV Games               | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           4 |             0 |                0 |
| radica-play-tv                   | RADICA Play TV                     | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          59 |             0 |                0 |
| rca-studio-ii                    | RCA Studio II                      | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput studio2 -cart                                                                                       |           1 |             1 |               36 |
| sam-coupe                        | SAM Coupe                          | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput samcoupe -autoboot_delay 2 -skip_gameinfo -autoboot_command \nBOOT\n -flop1                         |           1 |             2 |               31 |
| sega-beena                       | Sega Beena                         | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput beena -cart1                                                                                        |           1 |             1 |               60 |
| sega-sc-3000                     | Sega SC-3000                       | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput sc3000 -cart                                                                                        |           1 |             3 |              270 |
| senario-tv-games                 | Senario TV Games                   | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          23 |             0 |                0 |
| sharp-mz-2500                    | Sharp MZ-2500                      | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput mz2500 -flop1                                                                                       |           1 |             1 |               65 |
| sord-m5                          | Sord M5                            | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput m5 -cart1                                                                                           |           1 |             2 |               73 |
| spectravision-svi-318            | Spectravision SVI-318              | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput svi318 -cart                                                                                        |           1 |             2 |              210 |
| super-impulse-tv-games           | Super Impulse TV Games             | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           5 |             0 |                0 |
| takara-jumping-popira            | Takara Jumping Popira              | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cartridge    | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput jpopira -cart                                                                                       |           1 |             1 |                9 |
| takara-popira                    | Takara Popira                      | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | True                   | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           1 |             1 |               41 |
| takara-tomy-tv-game              | Takara Tomy TV Game                | Consoles, MESS (TV Games)                              | cart         | True                   | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          32 |             1 |                2 |
| takara-e-kara                    | Takara e-kara                      | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cartridge    | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput ekaraa -cart                                                                                        |           1 |             1 |              220 |
| tandy-memorex-vis                | Tandy Memorex VIS                  | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cartridge    | False                  | MAME (CD)        | True          | -keyboardprovider dinput vis -cdrom                                                                                          |           1 |             1 |               70 |
| tandy-trs-80                     | Tandy TRS-80                       | Computers, MESS (Computers), MESS (System w/ Softlist) | cartridge    | False                  | MAME (Cassette)  | True          | -keyboardprovider dinput trs80 -cass                                                                                         |           1 |             1 |                6 |
| tandy-trs-80-color-computer      | Tandy TRS-80 Color Computer        | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput coco3h -cart1                                                                                       |           1 |             2 |              109 |
| tangerine-oric-1                 | Tangerine Oric-1                   | Computers, MESS (Computers), MESS (System w/ Softlist) | cartridge    | False                  | MAME (Cassette)  | True          | -keyboardprovider dinput oric1 -autoboot_delay 4 -autoboot_command cload""\n -cass                                           |           1 |             1 |              449 |
| technosys-aamber-pegasus         | Technosys Aamber Pegasus           | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput pegasus                                                                                             |           1 |             1 |               16 |
| tiger-electronics-handhelds-lcd  | Tiger Electronics Handhelds (LCD)  | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          72 |             0 |                0 |
| tiger-game-com                   | Tiger Game.com                     | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput gamecom -cart1                                                                                      |           1 |             1 |               23 |
| timetop-game-king                | TimeTop Game King                  | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput gameking -cart                                                                                      |           1 |             1 |               45 |
| timetop-game-king-3              | TimeTop Game King 3                | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput gamekin3 -cart                                                                                      |           1 |             2 |               55 |
| tomy-handhelds-lcd               | Tomy Handhelds (LCD)               | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          13 |             0 |                0 |
| tomy-tutor                       | Tomy Tutor                         | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput tutor -cart                                                                                         |           1 |             1 |               32 |
| tomy-evio                        | Tomy evio                          | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput evio -cart                                                                                          |           1 |             1 |               18 |
| tronica-handhelds-lcd            | Tronica Handhelds (LCD)            | Handhelds, MESS (Handhelds LCD)                        | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          10 |             0 |                0 |
| ultimate-products-tv-games       | Ultimate Products TV Games         | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |           7 |             0 |                0 |
| uzebox                           | Uzebox                             | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput uzebox -cart                                                                                        |           1 |             1 |              128 |
| vtech-creativision               | VTech Creativision                 | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput crvision -cart                                                                                      |           1 |             1 |               39 |
| vtech-genius-leader-color        | VTech Genius Leader Color          | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput glcolor -cart1                                                                                      |           1 |             2 |               16 |
| vtech-socrates                   | VTech Socrates                     | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput socrates -cart                                                                                      |           1 |             1 |                8 |
| vtech-tv-games                   | VTech TV Games                     | Consoles, MESS (TV Games)                              | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput                                                                                                     |          10 |             0 |                0 |
| vtech-vsmile                     | VTech VSmile                       | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput vsmile -cart                                                                                        |           1 |             2 |              411 |
| vtech-vsmile-baby                | VTech VSmile Baby                  | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput vsmileb -cart                                                                                       |           1 |             1 |               23 |
| vtech-vsmile-motion              | VTech VSmile Motion                | Consoles, MESS (Consoles), MESS (System w/ Softlist)   | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput vsmilem -cart                                                                                       |           1 |             2 |              411 |
| vector-06c                       | Vector-06C                         | Computers, MESS (Computers), MESS (System w/ Softlist) | floppy       | False                  | MAME (Computers) | True          | -keyboardprovider dinput vector06 -flop1                                                                                     |           1 |             2 |               18 |
| videobrain-family-computer       | VideoBrain Family Computer         | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput vidbrain -cart                                                                                      |           1 |             1 |               18 |
| videoton-tvc-64                  | Videoton TVC 64                    | Computers, MESS (Computers), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput tvc64p -cart1                                                                                       |           1 |             3 |             1103 |
| watara-supervision               | Watara Supervision                 | Handhelds, MESS (Handhelds), MESS (System w/ Softlist) | cart         | False                  | MAME (Cartridge) | True          | -keyboardprovider dinput svision -cart                                                                                       |           1 |             1 |               72 |

Total platforms displayed: 105
```

### `config` Command: Manage Program Settings

Allows you to view or change the program's configuration paths.

```
python src\mess_curator.py config
```

Options (Mutually Exclusive - choose one per command):

- `--set-mame-exe-path <path>`: Set MAME executable path.

- `--set-softlist-rom-dir <path>`: Set Softlist ROMs source directory.

- `--set-output-rom-dir <path>`: Set output ROMset directory.

- `--set-mess-ini-path <path>`: Set MESS.ini file path.

- `--set-system-softlist-yaml-file <path>`: Set System Softlist YAML output file path.

## GUI

MESS Curator CLI also comes with CLI. However the GUI is not frequently updated as compared to the CLI version. 

### How It Works

To keep the GUI easier to sync with CLI, it calls the CLI functions and render the result on UI.

### Run
```
python src\mess_ui.py
```

## FAQ

Q: How does the tool determine if a system suport softlist?

If the `<softwarelist>` entry is present under a `<machine>` entry in the `mame.xml` file, then it is determined to have such.

```
	<machine name="pegasus" sourcefile="ausnz/pegasus.cpp" isbios="no" isdevice="no" ismechanical="no" runnable="yes">
		<description>Aamber Pegasus</description>
		<year>1981</year>
		<manufacturer>Technosys</manufacturer>
		<biosset name="11r2674" description="Monitor 1.1 r2674" default="no" />
		<biosset name="10r2569" description="Monitor 1.0 r2569" default="no" />
		...
		<slot name="exp0d">
		</slot>
		<softwarelist tag="cart_list" name="pegasus_cart" status="original" />
```

## Contribution

Feel free to open issues or pull requests on the GitHub repository if you have suggestions to the MESS systems that should be added as default, bug reports, or want to contribute to the project and pay for a cup of my soy bean~

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B8WK7DL)