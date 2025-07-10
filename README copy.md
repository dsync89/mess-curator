# MESS Curator Tool

## Organize, Filter, and Curate Your MAME/MESS ROMsets with Ease

This tool is a powerful command-line utility designed for the meticulous curation of MAME's non-arcade "MESS" platforms and their associated software lists. It is the only tool of its kind that provides the flexibility to parse, filter, and group any MAME systems into custom platforms, which can then be used to build perfectly organized ROM sets.

If you've ever wanted to separate your TV Games, Handhelds, or obscure Consoles from your main MAME set, this is the tool you need.

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

## Companion Tool to my Launchbox Plug in - `MESS Curated Softlist Importer`

The primary purpose of this tool is to generate a `system_softlist.yml` file, which acts as a direct input for my first Launchbox Plugin - [MESS Curated Softlist ROM Importer plugin for LaunchBox](https://github.com/dsync89/lb-mess-curated-platform-softlist-importer).

The workflow is simple:

1. Use this tool to filter a list of platforms that you want into `system_softlist.yml` file.
2. Use the `copy-roms` command to create a curated ROM set based on the YAML file.
3. Use my LaunchBox plugin to import your games, which reads the generated `system_softlist.yml` 
to automatically add platforms, emulators, metadata, clones, mark broken games, and per title custom MAME command-line parameters in LaunchBox.

## The System-Softlist YAML

The core of MESS Curator is the `system_softlist.yml` file. This file acts as the blueprint for your curated platforms.

### Structure Example

The YAML is structured logically, with a unique key for each platform. Here is an example for the Acorn Archimedes, demonstrating a custom command for the game `elite`.

```yaml
acorn-archimedes:
  platform:
    name: Acorn Archimedes
  platform_category:
  - Computers
  - MESS (Computers)
  - MESS (System w/ Softlist)
  media_type: floppy
  enable_custom_command_line_param_per_software_id: true
  emulator:
    name: MAME (Floppy)
    default_emulator: true
    default_command_line_parameters: -keyboardprovider dinput aa4401 -flop
  system:
  - aa4401:
      software_lists:
      - softlist_name: arch_flop
        software_id:
        - elite
        - zarch
        # ... other software ...
      software_configs:
        arch_flop:
          elite:
            command_line_parameters: -autoboot_delay 2 -autoboot_command "*BASIC\nCHAIN \"ELITE\""
```

## Installation

1.  **Python 3.7+:** Ensure you have a modern version of Python installed.
2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/dsync89/mess-curator.git
    cd mess-curator
    ```
3.  **Install Dependencies:**
    ```bash
    pip install PyYAML tabulate
    ```
4.  **MAME:** Have a recent MAME installation ready and know the path to `mame.exe`.
5.  **mess.ini:** This tool requires a `mess.ini` file (typically placed in MAME's `folders` directory) to distinguish non-arcade systems. You can obtain this from communities like [AntoPISA's MAME Support Files](https://github.com/AntoPISA/MAME_SupportFiles).

## Getting Started

### 1. Initial Configuration

The first time you run the script, a guided setup wizard will launch to configure essential paths.

```bash
python src/mess_curator.py
```

You can view or update your configuration at any time:
`python src/mess_curator.py config`
`python src/mess_curator.py config --set-mame-exe-path "C:\MAME\mame.exe"`

### 2. Pre-processing MAME Data (Recommended)

For the best performance, generate filtered XML files. This is a one-time operation that dramatically speeds up future searches.

```bash
python src/mess_curator.py split
```

This command creates `mess.xml`, `mess-softlist.xml`, and `mess-nosoftlist.xml` in your project directory, which the tool will use automatically.

## Usage and Examples

The most powerful command is `search`, which allows you to find systems and generate your YAML file.

---

### **Example 1: Create a Platform for Acorn Archimedes with a Custom Game Command**

This example generates a YAML entry for the `aa4401` system, but adds a specific `autoboot` command just for the game `elite`.

```powershell
python .\src\mess_curator.py search by-name `
    --platform-key acorn-archimedes `
    --platform-name-full "Acorn Archimedes" `
    --platform-category "Computers" `
    --media-type floppy `
    --emu-name "MAME (Floppy)" `
    --default-emu `
    --default-emu-cmd-params '-keyboardprovider dinput aa4401 -flop' `
    --output-format yaml `
    --add-software-config 'arch_flop:elite:"-autoboot_delay 2 -autoboot_command \"*BASIC\nCHAIN \"ELITE\"\""' `
    aa4401
```

### **Example 2: Create a Platform for Handhelds, Including Only Specific Softlists**

This example finds all systems with "Entex" in their description, but **only includes** software from the `advision` and `svis_cart` softlists.

```powershell
python .\src\mess_curator.py search by-filter "Entex" `
    --input-xml mess.xml `
    --platform-key entex-handhelds `
    --platform-name-full "Entex Handhelds" `
    --media-type cart `
    --emu-name "MAME (Cartridge)" `
    --default-emu `
    --output-format yaml `
    --include-softlist "advision svis_cart"
```

### **Example 3: Find All "Good" TV Games and Output to a Table**

This is useful for discovery. It searches all MESS systems for "TV Game" in the description, filters for "good" emulation, and displays the results in a clean table.

```powershell
python .\src\mess_curator.py search by-filter "TV Game" `
    --input-xml mess.xml `
    --emulation-status good `
    --show-extra-info `
    --output-format table
```

### **Example 4: Build Your Curated ROM Set**

Once your `system_softlist.yml` is configured, this command will create a clean, organized folder structure with all the required ROMs.

```bash
python src/mess_curator.py copy-roms
```

This will read your YAML and copy the files into the configured output directory, ready for your frontend.

## All Commands

For detailed help on any command, use the `-h` flag (e.g., `python src/mess_curator.py search by-name -h`).

*   **`config`**: View or update tool configuration.
*   **`split`**: Generate filtered `mess.xml`, `mess-softlist.xml`, and `mess-nosoftlist.xml`.
*   **`search`**: The main command for finding systems and generating output.
    *   `by-name`: Search for systems by explicit name or fuzzy prefix.
    *   `by-xml`: Use a pre-existing XML file as the source for systems.
    *   `by-filter`: Find systems by searching their description text.
    *   `by-sourcefile`: Find systems by their driver source file (e.g., `nes.cpp`).
*   **`copy-roms`**: Copy ROMs based on your YAML file.
*   **`table`**: Display the contents of a YAML file in a detailed table.
*   **`platform-info`**: Show a high-level summary of the platforms in your YAML file.

## Contribution

Contributions are welcome! Feel free to open an issue or pull request for bug fixes, feature suggestions, or additions to the default platform lists.

If you find this tool useful, please consider supporting its development.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B8WK7DL)