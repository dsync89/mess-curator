# MESS Curator Tool

## Organize, Filter, and Curate Your MAME/MESS ROMsets with Ease

This tool is a powerful command-line utility designed for the meticulous curation of MAME's non-arcade "MESS" platforms and their associated software lists. It is the only tool of its kind that provides the flexibility to parse, filter, and group any MAME systems into custom platforms, which can then be used to build perfectly organized ROM sets.

If you've ever wanted to separate Plug & Play TV Games, Handhelds LCDs, or obscure Consoles from your main MAME set, this is the tool you need.

This tool allows you to:

*   **Intelligently filter** MAME's vast machine list by name, fuzzy prefix, description, driver status, and emulation status.
*   **Auto-generate structured YAML** configuration files (`system_softlist.yml`) for platforms, complete with systems, their associated software lists, and even individual software IDs.
*   **Define per-game launch commands** directly from the command line, essential for computer systems.
*   **Selectively include or exclude** entire software lists to fine-tune your platforms.
*   **Copy and organize** ROMs into a curated folder structure, creating dummy `.zip` files for missing titles or standalone systems.
*   **Pre-process MAME's XML data** by filtering for MESS systems (non-arcade) and splitting them into "softlist-capable" and "non-softlist" categories, significantly speeding up subsequent operations.
*   **List "good" emulation drivers** for easy discovery of well-supported systems.
*   **Provide detailed table outputs** for various data views directly from your YAML or MAME's XML.
*   **Manage program configurations** easily via a `config.yaml` file or command-line arguments.

<p align="center">
  <a href="https://ko-fi.com/B0B8WK7DL" target="_blank">
    <img src="https://storage.ko-fi.com/cdn/brandasset/v2/support_me_on_kofi_blue.png" alt="Buy Me a Coffee at ko-fi.com" width="250">
  </a>
</p>

## Companion Tool to my Launchbox Plugin - MESS Curated Softlist Importer

The primary purpose of this tool is to generate a `system_softlist.yml` file, which acts as a direct input for my first Launchbox Plugin - [MESS Curated Softlist ROM Importer plugin for LaunchBox](https://github.com/dsync89/lb-mess-curated-platform-softlist-importer).

The workflow is simple:

1. Use this tool to filter a list of platforms that you want into `system_softlist.yml` file.
2. Use the `copy-roms` command to create a curated ROM set based on the YAML file.
3. Use my LaunchBox plugin to import your games, which reads the generated `system_softlist.yml` 
to automatically add platforms, emulators, metadata, clones, mark broken games, and per title custom MAME command-line parameters in LaunchBox.

## Key Features

MESS Curator provides a comprehensive suite of tools to discover, filter, and organize MAME's non-arcade systems and software into custom-tailored collections.

- **Intuitive System Discovery & Filtering**:
  - **Machine Filters**: Precisely target systems using clear and explicit flags. Filter by name (`--filter-machine-name-fuzzy`), description (`--filter-machine-description`), or even the driver source file (`--filter-machine-sourcefile`). You can even chain them together!
  - **Status Filtering**: Narrow your search to include only machines with a specific driver or emulation status (e.g., `--emulation-status good`).

- **Custom Platform Generation**:
  - **YAML Blueprints**: Automatically generate structured YAML files (`system_softlist.yml`) that act as a blueprint for your curated platforms.
  - **Flexible Grouping**: Group any combination of MAME systems into a single, logical platform—perfect for creating collections like "All JAKKS Pacific TV Games" or "All Handhelds with Good Emulation."

- **Advanced Customization & Automation**:
  - **Per-Title Commands**: Define custom command-line parameters for individual software titles (`--add-software-config`), essential for computer systems or games needing special setup.
  - **Per-Softlist Commands**: Apply default command-line parameters to all titles within a specific software list (`--add-softlist-config`) for broad configuration.
  - **Selective Inclusion/Exclusion**: Fine-tune your platforms by explicitly including or excluding specific systems or entire software lists.

- **Curated ROM Set Construction**:
  - **Automated Copying**: Use the `copy-roms` command to read your YAML blueprint and automatically build a clean, organized ROM set in your output directory.
  - **Placeholder Creation**: The tool can create dummy `.zip` files for any missing software, ensuring your frontend sees a complete set, even if you don't have all the ROMs.

- **Streamlined Workflow & Utilities**:
  - **Automated XML Handling**: The tool automatically downloads the correct `mess.xml` for your MAME version on first run, eliminating manual steps.
  - **Setup Wizard**: An interactive, first-run wizard guides you through setting up all necessary paths.
  - **Data Views**: Inspect your YAML files or MAME's XML data in clean, readable tables using the `table` and `platform-info` commands.
  - **GUI**: A graphical user interface is available for users who prefer a visual approach.

## Why This Tool is Unique

Many existing tools focus on full ROMset validation or arcade-only management. MESS Curator specifically targets the unique challenges of curating non-arcade "MESS" systems with a focus on flexibility and automation.

*   **Unmatched Filtering Granularity**: MESS Curator stands alone in its ability to distinguish between filtering **machines** and filtering the **software** within them. Using explicit flags like `--filter-machine-description` and `--filter-software-description` removes ambiguity and gives you precise control over your collection at both the system and title level.

*   **MESS-Centric by Design**: The tool is built from the ground up to understand and handle the nuances of MAME's non-arcade systems. It correctly interprets software lists, compatibility flags, and the complex relationships between systems.

*   **Intelligent Platform Curation**: Go beyond MAME's rigid structure. You can group any arbitrary set of systems—even from different driver files or manufacturers—into a single, cohesive platform in your YAML file. This allows you to organize your collection based on themes, genres, or any other criteria you choose.

*   **Automation-Ready Output**: The generated `system_softlist.yml` is a well-structured, machine-readable blueprint. It's designed to be consumed by external scripts and frontend plugins, most notably the [MESS Curated Softlist ROM Importer for LaunchBox](https://github.com/dsync89/lb-mess-curated-platform-softlist-importer), for fully automated setup.

*   **Performance and Simplicity**: By automatically downloading and caching the necessary `mess.xml`, the tool avoids forcing users to perform slow, manual `mame -listxml` generations and simplifies the entire setup process.


## Dependencies

MESS Curator requires the `mess.xml` that matches the MAME romset version you download. This XML is actively maintained by the good Italian community at https://www.progettosnaps.net/mess/repository. This `mess.xml` file is critical as it contains a list of machine/system names that is non-Arcade that would otherwise impossible to determined using the `mame.xml` that you generated using `mame -listxml` itself, as it does not contain any fields that indicate whether a system is Arcade or Non-Arcade.

### Backstory

Previously mess-curator requires several intermediate steps to generate a `mess.xml`. These are now obsolete and the program will simply download the xml from https://www.progettosnaps.net/mess/repository based on the mame version you specified.
1. Download `mess.ini` maintained by the good Italian community at https://github.com/AntoPISA/MAME_SupportFiles that you put into `MAME\folders`. 
2. Compare each entries in `mess.ini` against the full `mame.xml` generated using `mame -listxml`
3. Output into `mess.xml`.

## The System-Softlist YAML

While you may use this tool as a lister to quickly filter out those systems/softlist that you like, or generate CSV then filter yourself, the most powerful power or the main motivation for this tool is to generate a YAML file, which I aptly called **System-Softlist YAML** that contains a list of systems, softlists, metadata, etc. This file also acts as the blueprint for my [Launchbox MESS Curator Plugin] tool that can be used to readily import these system or titles as Platforms in Launchbox front end.

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

See [Advanced Usage](#advanced-usage) for the command line examples that can be used to generate these advanced overridable configs.

## Preset System-Softlist YAML

In case you don't want to generate the system-softlist YAML yourself, I had meticulously curated a list of notable MESS systems on the recent MAME sets (0.277, 0.278) that I personally like to have in my collections and you can use it as-is. You can find them in the `data\<mame_version>\system_softlist.yml` folder. 

These preset system-softlist YAML is created using a Windows PowerShell script in `gen_platforms_all.ps1`. In case you updated a MAME set and I still haven't update the template, you can simply run that script to update the YAML file based on the newer MAME mess.xml file.

The systems are chosen based on one of the following critieria:

- **Obscurity**: Less known system or manufacturer are prioritize as I am interested to know more about it. 
- **Playable titles**: The system must have at least one or few playable titles.
- **Well known manufacturer**: This might contradict with the first criteria, but if it's from a well known Manufacturer you bet to see it in the list, especially those LCD Handhelds from well known manufacturers like Konami, Nintendo, and Tiger.com

I do welcome contribution to these listings as time goes if you think more systems should be added. Since I used Launchbox as my front-end, I include all games (both broken and working) and then use my [Launchbox MESS Curator Plugin] tool to mark those games as Broken and add clones as additional apps. 

You can extend or generate your own YAML Files.

### How to Use

Be sure to configure `config.yaml` and point `system_softlist_yaml_file` to `data\<mame_version>\system_softlist.yml` for the program to read those. 

Or simply copy the said yml file into the root of this project repo, and then set `system_softlist_yaml_file` to `system_softlist.yml` which is relative to the project folder instead.

## Installation

1.  **Python 3.7+:** Ensure you have Python 3.7+ installed. You can download it from [python.org](https://www.python.org/downloads/).
2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/dsync89/mess-curator.git
    cd mess-curator 
    ```
3.  **Install Dependencies:**
    ```bash
    pip install PyYAML tabulate
    ```
4.  **MAME:** Ensure you have a MAME installation (0.277+ recommended) and know its executable path.
5.  **mess.ini:** This tool requires a `mess.ini` file (typically placed in MAME's `folders` directory) to distinguish non-arcade systems. You can obtain this from communities like [AntoPISA's MAME Support Files](https://github.com/AntoPISA/MAME_SupportFiles).

## Getting Started

Before running most commands, the tool needs to know where your MAME executable, ROMs, and output files are located.

### Initial Configuration

The very first time you run `mess_curator.py` (and `config.yaml` doesn't exist), it will automatically launch a guided setup process:

```bash
python src\mess_curator.py
```

or on Windows

```
mess_curator.bat
```

Follow the prompts to set your paths. It will attempt to auto-detect sensible defaults.

```
python .\src\mess_curator.py search --filter-machine-description Nintendo --filter-software-description Mario
[ERROR] Config file not found: C:\Users\dsync89\Documents\Github-dsync89\mess-curator\config.yaml
============================================================
 MAME MESS Curator Tool - Initial Setup Wizard
============================================================

Configuration file 'C:\Users\dsync89\Documents\Github-dsync89\mess-curator\config.yaml' not found.
Let's set up the necessary paths to get started.

[1/5] Please enter the full path to your MAME executable (e.g., C:\MAME\mame.exe):
> c:\Programs\LaunchBox\Emulators\MAME 0.278\mame.exe

[INFO] Attempting to auto-detect MAME version by running the executable...

[2/5] Auto-detected MAME version: 0.278

[3/5] Please enter the path to your MAME 'softlist' ROMs directory:
      (This is where subfolders like 'nes', 'ekara_cart', etc., are located)
> c:\Programs\LaunchBox\Emulators\MAME 0.278\roms\softlist

[4/5] Please enter the path for the curated output ROMsets:
      (This directory will be created if it doesn't exist)
> r:\roms\other\mame-mess

[5/5] The generated platform metadata will be saved as 'system_softlist.yml' in the current directory.

==================== Configuration Summary ====================
mame_executable:               c:\Programs\LaunchBox\Emulators\MAME 0.278\mame.exe
mess_version:                  0.278
softlist_rom_sources_dir:      c:\Programs\LaunchBox\Emulators\MAME 0.278\roms\softlist
out_romset_dir:                r:\roms\other\mame-mess
system_softlist_yaml_file:     system_softlist.yml
mess_xml_file:                 mess.xml
============================================================

Save this configuration? [Y/n]: y

[SUCCESS] Configuration saved to 'C:\Users\dsync89\Documents\Github-dsync89\mess-curator\config.yaml'. You can now run the tool.
```

Once that is setup, it will then check if there's any `mess.xml` for the MAME version. If none, then it will automatically download from https://www.progettosnaps.net/mess/repository/. The next time you run it and if the `mess.xml` file exist in `data\<mame_version>\mess.xml`, then it will simply use it instead.

```
[WARNING] MESS XML for version 0.278 not found.
          Would you like to download it from progetto-snaps.net? [Y/n]: y
[INFO] Attempting to download from: https://www.progettosnaps.net/download/?tipo=mess_xml&file=/mess/packs/xml/mess278.zip
[INFO] Downloading... 100%
[INFO] Download complete.
[INFO] Extracting 'C:\Users\dsync89\Documents\Github-dsync89\mess-curator\data\mess0.278_temp.zip' to 'C:\Users\dsync89\Documents\Github-dsync89\mess-curator\data\0.278'...
[SUCCESS] MESS XML for version 0.278 is now available at 'C:\Users\dsync89\Documents\Github-dsync89\mess-curator\data\0.278\mess.xml'.
```

You can then proceed to use the rest of the subcommands. 

See [Usage](#usage) for a list of subcommands that you can use with mess-curator.

**Viewing Current Configuration:**

```
python src\mess_curator.py config    
```

**Setting Specific Paths (Command Line):**

You can also modify the `config.yaml` to set each individual config, or using the `--set-<field_name>` arg.

```
python src\mess_curator.py config --set-mame-exe-path "C:\Programs\LaunchBox\Emulators\MAME 0.277\mame.exe"
python src\mess_curator.py config --set-softlist-rom-dir "C:\Programs\LaunchBox\Emulators\MAME 0.277\roms"
python src\mess_curator.py config --set-output-rom-dir "C:\Users\dsync89\Documents\Github-dsync89\mess-curator\out\mame_curated_romset"
python src\mess_curator.py config --set-mess-ini-path "C:\Programs\LaunchBox\Emulators\MAME 0.277\folders\mess.ini"
python src\mess_curator.py config --set-system-softlist-yaml-file "C:\Users\dsync89\Documents\Github-dsync89\mess-curator\data\my_platforms.yml"
```

*(Paths shown are examples, adjust to your system. Note: `MAME_EXECUTABLE's` parent directory is used to guess mess.ini default path)*

## Usage

All commands follow a subcommand structure. Use `python src\mess_curator.py <command> -h` for specific help.

**Important Notes for Windows (PowerShell/CMD):**

If your paths or arguments contain spaces, enclose them in double quotes "like this".

When breaking a long command across multiple lines, use the backtick (`) at the end of each line (except the last one):

```powershell
python src\mess_curator.py search `
    --output-format yaml `
    --platform-key my-platform `
    --filter-machine-name-fuzzy "jak_"
```

---

### `search` Command: Find Systems and Generate YAML/Table/CSV

The `search` command is the core of the tool, allowing you to find systems based on various criteria and generate structured output.

```bash
usage: mess_curator.py search [-h] [--show-systems-only] [--show-extra-info] [--sort-by {system_name,system_desc,manufacturer,year,software_id,title,publisher,driver_status,emulation_status,sourcefile}]
                              [--platform-key PLATFORM_KEY] [--platform-name-full PLATFORM_NAME_FULL] [--platform-category PLATFORM_CATEGORY [PLATFORM_CATEGORY ...]] [--media-type MEDIA_TYPE] [-ect] [-en EMU_NAME] [-de]
                              [-dec DEFAULT_EMU_CMD_PARAMS] [--add-software-config SOFTLIST:SWID:"PARAMETERS"] [--add-softlist-config SOFTLIST:"PARAMETERS"] [--include-systems INCLUDE_SYSTEMS]
                              [--exclude-systems EXCLUDE_SYSTEMS] [--include-softlist INCLUDE_SOFTLIST]
                              [--exclude-softlist EXCLUDE_SOFTLIST] [--filter-machine-name-fuzzy FILTER_MACHINE_NAME_FUZZY]
                              [--filter-machine-description FILTER_MACHINE_DESCRIPTION [FILTER_MACHINE_DESCRIPTION ...]] [--filter-machine-sourcefile FILTER_MACHINE_SOURCEFILE]
                              [--filter-software-description FILTER_SOFTWARE_DESCRIPTION] [--input-xml INPUT_XML] [--limit LIMIT]
                              [--output-format {table,yaml,csv}] [--output-file OUTPUT_FILE] [--driver-status {good,imperfect,preliminary,unsupported}]
                              [--emulation-status {good,imperfect,preliminary,unsupported}]
                              [systems ...]
```

**Key Search and Filtering Arguments:**

- `systems`: (Positional) One or more MAME system short names (e.g., `nes`, `snes`).
- `--filter-machine-name-fuzzy <prefix>`: Find all systems starting with a specific prefix (e.g., `jak_`).
- `--filter-machine-description <text>`: Filter systems where the description contains the given text.
- `--filter-machine-sourcefile <file.cpp>`: Filter systems by their driver source file (e.g., `xavix.cpp`).
- `--filter-software-description <text>`: Filter by a term in the software's ID or description.
- `--driver-status`: Filter by driver status (e.g., `good`).
- `--emulation-status`: Filter by emulation status (e.g., `good`).
- `--include-systems` / `--exclude-systems`: Explicitly include or exclude systems.
- `--include-softlist` / `--exclude-softlist`: Explicitly include or exclude software lists.
- `--input-xml <path>`: Specify the source XML file (e.g., `mess-softlist.xml`). Defaults to the one for your configured MAME version.

**Common Output Arguments:**

- `--output-format {table,yaml,csv}`: Choose the output format. Defaults to `table`.
- `--output-file <path>`: Specify the output file path (required for `csv`, optional for `yaml`).
- `--show-extra-info`: (For table) Show additional columns like Manufacturer, Year, etc.
- `--show-systems-only`: (For table) Show only one row per system.

**YAML Output Specific Arguments:**

- `--platform-key <key>`: (Required) A unique key for the platform (e.g., `jakks-pacific-tv-games`).
- `--platform-name-full <name>`: (Required) The full, human-readable name of the platform.
- `--media-type <type>`: (Required) The media type (e.g., `cart`, `floppy`).
- `--add-software-config 'softlist:swid:"params"'`: Add a custom command for a specific game.
- `--add-softlist-config 'softlist:"params"'`: Add a default command for all games in a softlist.

**Examples:**

- **Table output for a single system and its software:**

```bash
python src\mess_curator.py search nes --output-format table
```

- **YAML output for multiple JAKKS systems (fuzzy search + exclude) with emulator details:**

```powershell
python src\mess_curator.py search `
    --platform-key "jakks-pacific-tv-game" `
    --platform-name-full "JAKKS Pacific TV Game" `
    --media-type "cart" `
    --enable-custom-cmd-per-title `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput" `
    --output-format yaml `
    --filter-machine-name-fuzzy "jak_" `
    --exclude-systems "jak_pf jak_prft jak_s500 jak_smwm jak_ths jak_tink jak_totm jak_umdf"
```

- **Find "in-1" multigame systems from `mess.xml`, output to YAML:**

```powershell
python src\mess_curator.py search `
    --filter-machine-description "in-1" `
    --platform-key "mess-filtered-all-in-one-systems" `
    --platform-name-full "MESS (All-In-One Systems)" `
    --media-type "cart" `
    --output-format yaml
```

- **Table output for good emulation systems from `mess-softlist.xml`, with full infos:**

```powershell
python src\mess_curator.py search `
    --emulation-status good `
    --show-extra-info
```

- **Search for Mario softlist titles in Nintendo Machines**

```
python .\src\mess_curator.py search `
    --filter-machine-description Nintendo`
    --filter-software-description Mario
```

### `copy-roms` Command: Construct Your ROMset

Reads your `system_softlist.yml` and copies/creates dummy `.zip` files in a structured output directory.

```bash
python src\mess_curator.py copy-roms --input-file system_softlist.yml
```

**Output Structure Example:**
`C:\temp\mame_curated_romsetv2\my_platform_key\system_name\softlist_name\software_id.zip`

**Options:**
- `--input-file <path>`: Specify the input `system_softlist.yml` file. (Defaults to configured path)
- `--platform-key <key>`: (Optional) Copy ROMs only for a specific platform by its key.
- `--create-placeholder-zip`: Always create empty placeholder (dummy) zips instead of copying from the source directory.
- `--dry-run`: Show what would be copied or created without modifying any files.

Note:
- I highly recommend using `--create-placeholder-zip` to create a dummy zip. Unlike most emulators that require taking the full ROM path as the input argument, MAME maintains its internal database of ROM lists and paths, and the command-line parameter only requires the system or softlist name.

### `table` Command: Display `system_softlist.yml` as Table

Parses and displays the contents of your `system_softlist.yml` in a detailed table.

```bash
python src\mess_curator.py table --platform-key nintendo-game-and-watch --show-extra-info
```

**Options:**

- `--platform-key <key>`: Display only a specific platform.
- `--input-file <path>`: Specify the input `system_softlist.yml`. (Defaults to configured path)
- `--mame-xml-source <path>`: MAME XML file to fetch system descriptions/statuses. (Defaults to the one for your configured MAME version)
- `--show-systems-only`: Show only one row per system.
- `--show-extra-info`: Show Manufacturer and Publisher columns.

### `platform-info` Command: Display High-Level Platform Summary

Provides a high-level overview of platforms defined in your `system_softlist.yml`, including counts of systems, softlists, and software IDs.

```bash
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

### `split` Command: Generate Filtered MAME XMLs
This command is crucial for optimizing later search operations. It filters a given `mame.xml` based on the systems in `mess.ini` and then splits the result.

> Note: This is no longer necessary and only kept if you still wish to do so. Now the tool simply refers to the `mess.xml` downloadable from https://www.progettosnaps.net/mess/repository/

```bash
# Generate a fresh mame.xml from your configured mame.exe
python src\mess_curator.py split --from-mame-exe

# Or use an existing mame.xml file
python src\mess_curator.py split --input-xml "C:\path\to\your\mame.xml"
```

Output Files (generated in the `data/<version>` directory):
- `mess.xml`: (Machines listed in your mess.ini from mame.xml)
- `mess-softlist.xml`: (Machines from mess.xml that support software lists)
- `mess-nosoftlist.xml`: (Machines from mess.xml that do NOT support software lists)

Options:
- `--mess-ini <path>`: Specify a custom mess.ini file. (Defaults to configured path)
- `--input-xml <path>`: Path to an existing full `mame.xml` to use as the source.
- `--from-mame-exe`: Generate a fresh `mame.xml` from the `mame.exe` defined in your config.

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

### All Commands

For detailed help on any command, use the `-h` flag (e.g., `python src/mess_curator.py search -h`).

*   **`config`**: View or update tool configuration.
*   **`split`**: Generate filtered `mess.xml`, `mess-softlist.xml`, and `mess-nosoftlist.xml`.
*   **`search`**: The main command for finding systems and generating `table`, `yaml`, or `csv` output.
*   **`copy-roms`**: Copy ROMs based on your YAML file.
*   **`table`**: Display the contents of a YAML file in a detailed table.
*   **`platform-info`**: Show a high-level summary of the platforms in your YAML file.

## Advanced Usage

### **Example 1: Create a Platform for Acorn Electron that with a Common Custom Game Command per Softlist Media Format**

This example generates a YAML entry for the `electron` system, and uses a common custom `autoboot` command for all the titles in `bbc_cass`, `electron_cass`, `electron_cart` and `electron_flop` softlist respectively. 

```
# ----------------------
# Acorn Electron
# ----------------------
python .\src\mess_curator.py search `
    --platform-key acorn-electron `
    --platform-name-full "Acorn Electron" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cass `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput electron -skip_gameinfo -autoboot_delay \"2\" -autoboot_command \"*tape\nchain\"\"\"\"\"\"\n\" -cass' `
    --output-format yaml `
    --output-file system_softlist.yml `
    --exclude-softlist "electron_rom" `
    --add-softlist-config 'bbc_cass:electron -skip_gameinfo -autoboot_delay "2" -autoboot_command "*TAPE\nCHAIN\"\"\"\"\"\"\n" -cass' `
    --add-softlist-config 'electron_cass:electron -skip_gameinfo -autoboot_delay "2" -autoboot_command "*TAPE\nCHAIN\"\"\"\"\"\"\n" -cass' `
    --add-softlist-config 'electron_cart:electron -cart' `
    --add-softlist-config 'electron_flop:electron -skip_gameinfo -autoboot_delay "2" -autoboot_command \"cat\n\n\n\n\n\nrun !boot\n\" -flop' `
    electron
```

Output example

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
    name: MAME (MESS)
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
          _default_config:
            command_line_parameters: electron -skip_gameinfo -autoboot_delay 2 -autoboot_command
              *TAPE\nCHAIN""""""\n -cass
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

### **Example 2: Create a Platform for Bandai Gundam RX-78 with both Common Softlist and Custom Game Command**

This example generates a YAML entry for the `rx78` system, and uses the common custom `autoboot` command for `rx78_cart` and `rx78_cass` softlist. But adds a specific per-title `autoboot` command for the game `graphmaths` and `yellowcab`, since those two titles require specific `autoboot` command.

```powershell
# ----------------------
# Bandai Gundam RX-78
# ----------------------
python .\src\mess_curator.py search `
    --platform-key bandai-gundam-rx-78 `
    --platform-name-full "Bandai Gundam RX-78" `
    --platform-category "Computers" "MESS (Computers)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput rx78 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --add-softlist-config 'rx78_cart:rx78 -cart' `
    --add-softlist-config 'rx78_cass:rx78 -cass1' `
    --add-software-config 'rx78_cass:graphmaths:rx78 -autoboot_delay 2 -autoboot_command MON\nL\nGRM\n -cart basic -cass1' `
    --add-software-config 'rx78_cass:yellowcab:rx78 -autoboot_delay 2 -autoboot_command MON\nL\nCAB\n -cart basic -cass1' `
    rx78
```

Output example

```
bandai-gundam-rx-78:
  platform:
    name: Bandai Gundam RX-78
  platform_category:
  - Computers
  - MESS (Computers)
  - MESS (System w/ Softlist)
  media_type: cart
  enable_custom_command_line_param_per_software_id: false
  emulator:
    name: MAME (MESS)
    default_emulator: true
    default_command_line_parameters: -keyboardprovider dinput rx78 -cart
  system:
  - rx78:
      software_lists:
      - softlist_name: rx78_cart
        software_id:
        - abcword
        - aerial
...
      - softlist_name: rx78_cass
        software_id:
        - graphmaths
        - yellowcab
      software_configs:
        rx78_cart:
          _default_config:
            command_line_parameters: rx78 -cart
        rx78_cass:
          _default_config:
            command_line_parameters: rx78 -cass1
          graphmaths:
            command_line_parameters: rx78 -autoboot_delay 2 -autoboot_command MON\nL\nGRM\n
              -cart basic -cass1
          yellowcab:
            command_line_parameters: rx78 -autoboot_delay 2 -autoboot_command MON\nL\nCAB\n
              -cart basic -cass1
```

### **Example 3: Exclude a compatible softlist that is not unique for a system**

The TimeTop GameKing handhelds support both `gameking` and `gameking3` softlist`, but since I created a separate Platform name for TimeTop GameKing 3, I excluded it from the GameKing platform.

```
# ----------------------
# TimeTop GameKing
# ----------------------
python .\src\mess_curator.py search `
    --platform-key timetop-game-king `
    --platform-name-full "TimeTop GameKing" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gameking -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --exclude-softlist "gameking3" `
    gameking
```

Likewise, the TimeTop GameKing 3 will exlude every softlist titles meant for Game King 1.

```
# ----------------------
# TimeTop GameKing 3
# ----------------------
python .\src\mess_curator.py search `
    --platform-key timetop-game-king-3 `
    --platform-name-full "TimeTop GameKing 3" `
    --platform-category "Handhelds" "MESS (Handhelds)" "MESS (System w/ Softlist)" `
    --media-type cart `
    --emu-name "MAME (MESS)" `
    --default-emu `
    --default-emu-cmd-params "-keyboardprovider dinput gamekin3 -cart" `
    --output-format yaml `
    --output-file system_softlist.yml `
    --exclude-softlist "gameking" `
    gamekin3
```

### **Example 4: Create a Platform for Handhelds, Including Only Specific Softlists**

This example finds all systems with "Entex" in their description, but **only includes** software from the `advision` and `svis_cart` softlists.

```powershell
python .\src\mess_curator.py search `
    --filter-description "Entex" `
    --platform-key "entex-handhelds" `
    --platform-name-full "Entex Handhelds" `
    --media-type "cart" `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --output-format yaml `
    --include-softlist "advision svis_cart"
```

### **Example 5: Find All "Good" TV Games and Output to a Table**

This is useful for discovery. It searches all MESS systems for "TV Game" in the description, filters for "good" emulation, and displays the results in a clean table.

```powershell
python .\src\mess_curator.py search `
    --filter-description "TV Game" `
    --emulation-status good `
    --show-extra-info
```

### **Example 6: Build Your Curated ROM Set**

Once your `system_softlist.yml` is configured, this command will create a clean, organized folder structure with all the required ROMs.

```bash
python src/mess_curator.py copy-roms
```

### **More Examples**

For more examples, see the `gen_platforms_all.ps1` powershell script that is used to generate the `system_softlist.yml` template file for a mame version.

This will read your system softlist YAML and copy the files into the configured output directory, ready for ingesting by my [MESS Curated Softlist ROM Importer plugin for LaunchBox](https://github.com/dsync89/lb-mess-curated-platform-softlist-importer).

## GUI

MESS Curator CLI also comes with CLI. However the GUI is not frequently updated as compared to the CLI version. 

### How It Works

To keep the GUI easier to sync with CLI, it calls the CLI functions and render the result on UI.

### Run
```
python src\mess_ui.py
```

## FAQ

**Q: How does the tool determine if a system suport softlist?**

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

**Q: How are softlist titles assigned to a system, especially when it's part of a system family with variants?**

A Softlist XML which contains a list of titles in a softlist might include a <compatibility> element that indicates which systems a title is compatible with. When this element is present, MESS Curator will respect it and assign only the titles that match the compatibility value of the target machine. This ensures that each title runs only on systems it's designed for.

For example, consider the Tandy TRS-80 computer family, which includes five models:

- 0 = trs80
- 1 = trs80l2 and its clones
- 3 = trs80m3
- 4 = trs80m4
- H = HT series

If you're running the `trs80` machine, only titles marked with compatibility value `0` will be available, since that's the value associated with that specific model.

**Q: Is all the softlist supported by a system get added?**

No, only the softlist that is unique or specific to the system will get added.

Take `Sega SC-3000` Computer system for example, it supports 3 softlists: `sc3000_cart`, `sc3000_cass`, and `sg1000`. But since SG1000 is already supported by another `Sega SC-1000` computer, it is not added to the `SC-3000` system.

## Contribution

Feel free to open issues or pull requests on the GitHub repository if you have suggestions to the MESS systems that should be added as default, bug reports, or want to contribute to the project and pay for a cup of my soy bean~

<p align="center">
  <a href="https://ko-fi.com/B0B8WK7DL" target="_blank">
    <img src="https://storage.ko-fi.com/cdn/brandasset/v2/support_me_on_kofi_blue.png" alt="Buy Me a Coffee at ko-fi.com" width="250">
  </a>
</p>
