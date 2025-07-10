import sys
import os
import yaml
import csv
import functools
import io
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QCheckBox, QComboBox, QFormLayout, QDialog,
    QDialogButtonBox, QMessageBox, QTextEdit, QFileDialog, QGroupBox, QLabel,
    QSplitter
)
from PySide6.QtCore import Qt, QObject, Signal, QThread, QTimer
from PySide6.QtGui import QFont, QIntValidator

# Import the actual core logic script
try:
    import mess_curator as core_logic
except ImportError:
    class MockCoreLogic:
        def __init__(self):
            self.APP_CONFIG = {}
            self.CONFIG_FILE = "config.yaml (mocked)"

        def __getattr__(self, name):
            if name == "APP_CONFIG":
                return self.APP_CONFIG
            if name == "CONFIG_FILE":
                return self.CONFIG_FILE
            
            def dummy_func(*args, **kwargs):
                print(f"Mocked core_logic.{name} called with: {args}, {kwargs}")
                if name == "load_configuration":
                    return False
                if name == "get_parsed_mame_xml_root":
                    return None
                return [] 
            return dummy_func
    core_logic = MockCoreLogic()


# === Advanced Worker with I/O Redirection ===
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = self._stringio_out = io.StringIO()
        sys.stderr = self._stringio_err = io.StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio_out.getvalue().splitlines())
        self.extend(self._stringio_err.getvalue().splitlines())
        del self._stringio_out
        del self._stringio_err
        sys.stdout = self._stdout
        sys.stderr = self._stderr

class Worker(QObject):
    finished = Signal()
    progress = Signal(str)
    error = Signal(str)
    result = Signal(object)
    
    def __init__(self, func, **kwargs):
        super().__init__()
        self.func = func
        self.kwargs = kwargs

    def run(self):
        try:
            with Capturing() as output:
                res = self.func(**self.kwargs)
            
            for line in output:
                if "[ERROR]" in line or "[WARNING]" in line.upper() or "traceback" in line.lower():
                    self.error.emit(line)
                else:
                    self.progress.emit(line)
            
            self.result.emit(res)
        except Exception as e:
            self.error.emit(f"Unhandled exception in worker: {e}\nCheck console for full traceback.")
            import traceback
            traceback.print_exc()
        finally:
            self.finished.emit()


# === Main Application Window ===
class MameRomManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAME MESS Curator UI")
        self.setGeometry(100, 100, 1200, 900)
        self.progress_timer = QTimer(self)
        self.progress_chars = ['|', '/', '─', '\\']
        self.progress_index = 0
        self.init_ui()
        self.load_initial_config()

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 10))
        
        self.main_tab_widget = QTabWidget()

        self.platforms_tab = PlatformsTab(self.log_output.append, self)
        self.search_tab = SearchTab(self.log_output.append, self)
        self.rom_copy_tab = RomCopyTab(self.log_output.append, self)
        self.settings_tab = SettingsTab(self.log_output.append, self)

        self.main_tab_widget.addTab(self.platforms_tab, "Platforms")
        self.main_tab_widget.addTab(self.search_tab, "Search")
        self.main_tab_widget.addTab(self.rom_copy_tab, "ROM Copy")
        self.main_tab_widget.addTab(self.settings_tab, "Settings")

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.main_tab_widget)
        splitter.addWidget(self.log_output)
        splitter.setSizes([600, 300]) 

        main_layout.addWidget(splitter)
        
        self.status_label = QLabel("Ready")
        self.statusBar().addWidget(self.status_label)
        self.progress_timer.timeout.connect(self.update_progress_indicator)

    def load_initial_config(self):
        if not core_logic.load_configuration():
            QMessageBox.warning(self, "Configuration Not Found",
                                f"Configuration file '{core_logic.CONFIG_FILE}' not found.\n\nPlease go to the 'Settings' tab to configure the required paths and save them.")
        else:
            self.settings_tab.load_settings_from_core_config()
            self.rom_copy_tab.update_paths_from_settings()
            self.platforms_tab.load_platforms()
            self.log_output.append("Application initialized successfully.")
            
    def start_long_operation(self):
        self.status_label.setText("Running...  ")
        self.progress_index = 0
        self.progress_timer.start(100)

    def stop_long_operation(self):
        self.progress_timer.stop()
        self.status_label.setText("Ready")

    def update_progress_indicator(self):
        char = self.progress_chars[self.progress_index]
        self.status_label.setText(f"Running... {char}")
        self.progress_index = (self.progress_index + 1) % len(self.progress_chars)


# === Reusable UI Components ===
class TableOptionsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Table/CSV Options", parent)
        layout = QFormLayout(self)
        self.show_systems_only_cb = QCheckBox("Show Systems Only")
        self.show_extra_info_cb = QCheckBox("Show Extra Info (Manufacturer, Year, etc.)")
        sort_by_choices = ['system_name', 'system_desc', 'manufacturer', 'year', 'software_id', 'title', 'publisher', 'driver_status', 'emulation_status', 'sourcefile']
        self.sort_by_combo = QComboBox()
        self.sort_by_combo.addItems(["(No Sorting)"] + sort_by_choices)
        
        layout.addRow(self.show_systems_only_cb)
        layout.addRow(self.show_extra_info_cb)
        layout.addRow("Sort By:", self.sort_by_combo)

class YamlOptionsWidget(QGroupBox):
    def __init__(self, parent=None, existing_categories=None):
        super().__init__("YAML Platform Options", parent)
        if existing_categories is None:
            existing_categories = set()
            
        layout = QFormLayout(self)
        self.platform_key_le = QLineEdit()
        self.platform_name_full_le = QLineEdit()
        self.platform_category_cb = QComboBox()
        self.platform_category_cb.setEditable(True)
        self.platform_category_cb.addItems(sorted(list(existing_categories)))
        self.media_type_cb = QComboBox()
        self.media_type_cb.addItems(["cart", "disk", "cdrom", "cassette", "rom"])

        layout.addRow("Platform Key:", self.platform_key_le)
        layout.addRow("Platform Name:", self.platform_name_full_le)
        layout.addRow("Platform Category:", self.platform_category_cb)
        layout.addRow("Media Type:", self.media_type_cb)

class EmuOptionsWidget(QGroupBox):
    def __init__(self, parent=None, existing_emu_names=None):
        super().__init__("Emulator Options (for YAML)", parent)
        if existing_emu_names is None:
            existing_emu_names = set()
            
        layout = QFormLayout(self)
        self.enable_custom_cmd_cb = QCheckBox("Enable Custom Cmd Per Title")
        self.emu_name_cb = QComboBox()
        self.emu_name_cb.setEditable(True)
        self.emu_name_cb.addItems(sorted(list(existing_emu_names)))
        self.default_emu_cb = QCheckBox("Set as Default Emulator")
        self.default_emu_cmd_params_le = QLineEdit()

        layout.addRow(self.enable_custom_cmd_cb)
        layout.addRow("Emulator Name:", self.emu_name_cb)
        layout.addRow(self.default_emu_cb)
        layout.addRow("Default Cmd Params:", self.default_emu_cmd_params_le)

class InclusionOptionsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("System Inclusions / Exclusions", parent)
        layout = QFormLayout(self)
        self.include_systems_le = QLineEdit()
        self.exclude_systems_le = QLineEdit()
        self.include_systems_le.setPlaceholderText("Space-separated list (e.g. \"nes snes\")")
        self.exclude_systems_le.setPlaceholderText("Space-separated list (e.g. \"nes snes\")")

        layout.addRow("Include Systems:", self.include_systems_le)
        layout.addRow("Exclude Systems:", self.exclude_systems_le)


# === Platform Configuration Dialog ===
# --- ADD THIS CLASS BACK (in its new, improved form) ---
class PlatformConfigDialog(QDialog):
    def __init__(self, parent=None, platform_data=None, existing_values=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Platform Configuration")
        self.setGeometry(150, 150, 600, 500)

        self.platform_data = platform_data if platform_data is not None else {}
        self.existing_values = existing_values if existing_values is not None else {'categories': set(), 'emu_names': set()}
        self.is_editing = 'platform_key' in self.platform_data and self.platform_data['platform_key']

        self.init_ui()
        if self.is_editing:
            self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.yaml_options = YamlOptionsWidget(self, existing_categories=self.existing_values['categories'])
        if self.is_editing:
            self.yaml_options.platform_key_le.setReadOnly(True)
            self.yaml_options.platform_key_le.setStyleSheet("background-color: #f0f0f0;")
        layout.addWidget(self.yaml_options)

        self.emu_options = EmuOptionsWidget(self, existing_emu_names=self.existing_values['emu_names'])
        layout.addWidget(self.emu_options)

        # --- REVISED Sourcing Group ---
        sourcing_group = QGroupBox("System & Software Sourcing (will be used to generate/update software list)")
        sourcing_layout = QFormLayout(sourcing_group)
        self.systems_te = QTextEdit() # For positional systems
        self.filter_machine_name_fuzzy_le = QLineEdit()
        self.filter_machine_description_le = QLineEdit()
        self.filter_machine_sourcefile_le = QLineEdit()
        self.filter_software_description_le = QLineEdit() # Replaces old search_term
        self.include_systems_le = QLineEdit()
        self.exclude_systems_le = QLineEdit()
        self.exclude_softlist_le = QLineEdit()
        
        self.systems_te.setPlaceholderText("One per line, or space/comma separated")
        self.filter_machine_name_fuzzy_le.setPlaceholderText("e.g. jak_")
        self.include_systems_le.setPlaceholderText("Space separated (e.g. \"nes snes\")")
        self.exclude_systems_le.setPlaceholderText("Space separated (e.g. \"nes snes\")")
        self.exclude_softlist_le.setPlaceholderText("Space separated (e.g. \"nes_ade\")")
        sourcing_layout.addRow("Systems (Positional):", self.systems_te)
        sourcing_layout.addRow("Filter Machine Name (Fuzzy):", self.filter_machine_name_fuzzy_le)
        sourcing_layout.addRow("Filter Machine Description:", self.filter_machine_description_le)
        sourcing_layout.addRow("Filter Machine Source File:", self.filter_machine_sourcefile_le)
        sourcing_layout.addRow("Filter Software Description:", self.filter_software_description_le)
        sourcing_layout.addRow("Include Systems (Manual Add):", self.include_systems_le)
        sourcing_layout.addRow("Exclude Systems (Manual Remove):", self.exclude_systems_le)
        layout.addWidget(sourcing_group)
        # --- END REVISED Sourcing Group ---

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def load_data(self):
        self.yaml_options.platform_key_le.setText(self.platform_data.get('platform_key', ''))
        self.yaml_options.platform_name_full_le.setText(self.platform_data.get('platform_name_full', ''))
        self.yaml_options.platform_category_cb.setCurrentText(' '.join(self.platform_data.get('platform_category', [])))
        
        media_type_index = self.yaml_options.media_type_cb.findText(self.platform_data.get('media_type', 'cart'))
        if media_type_index >= 0:
            self.yaml_options.media_type_cb.setCurrentIndex(media_type_index)

        self.emu_options.enable_custom_cmd_cb.setChecked(self.platform_data.get('enable_custom_cmd_per_title', False))
        self.emu_options.emu_name_cb.setCurrentText(self.platform_data.get('emu_name', ''))
        self.emu_options.default_emu_cb.setChecked(self.platform_data.get('default_emu', False))
        self.emu_options.default_emu_cmd_params_le.setText(self.platform_data.get('default_emu_cmd_params', ''))
        
        self.systems_te.setText('\n'.join(self.platform_data.get('systems', [])))
        self.filter_machine_name_fuzzy_le.setText(self.platform_data.get('filter_machine_name_fuzzy', ''))
        self.include_systems_le.setText(' '.join(self.platform_data.get('include_systems', [])))
        self.exclude_systems_le.setText(' '.join(self.platform_data.get('exclude_systems', [])))
        self.exclude_softlist_le.setText(' '.join(self.platform_data.get('exclude_softlist', [])))

    def get_data(self):
        platform_key = self.yaml_options.platform_key_le.text().strip()
        if not platform_key:
            QMessageBox.warning(self, "Input Required", "Platform Key is a mandatory field.")
            return None

        # Gather all data, including the new filter fields
        return {
            'platform_key': platform_key,
            'platform_name_full': self.yaml_options.platform_name_full_le.text().strip(),
            'platform_categories': [c.strip() for c in self.yaml_options.platform_category_cb.currentText().split() if c.strip()],
            'media_type': self.yaml_options.media_type_cb.currentText(),
            'systems': [s.strip() for s in self.systems_te.toPlainText().strip().replace(',', ' ').split() if s.strip()],
            'filter_machine_name_fuzzy': self.filter_machine_name_fuzzy_le.text().strip(),
            'filter_machine_description': [s.strip() for s in self.filter_machine_description_le.text().strip().split() if s.strip()],
            'filter_machine_sourcefile': self.filter_machine_sourcefile_le.text().strip(),
            'filter_software_description': self.filter_software_description_le.text().strip(),
            'include_systems': [item.strip() for item in self.include_systems_le.text().replace(',', ' ').split() if item.strip()],
            'exclude_systems': [item.strip() for item in self.exclude_systems_le.text().replace(',', ' ').split() if item.strip()],
            'exclude_softlist': [item.strip() for item in self.exclude_softlist_le.text().replace(',', ' ').split() if item.strip()],

            'enable_custom_cmd_per_title': self.emu_options.enable_custom_cmd_cb.isChecked(),
            'emu_name': self.emu_options.emu_name_cb.currentText().strip(),
            'default_emu': self.emu_options.default_emu_cb.isChecked(),
            'default_emu_cmd_params': self.emu_options.default_emu_cmd_params_le.text().strip(),
        }


# === Main UI Tabs ===
class PlatformsTab(QWidget):
    def __init__(self, log_func, main_app_ref):
        super().__init__()
        self.log = log_func
        self.main_app_ref = main_app_ref
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.platforms_table = QTableWidget()
        self.platforms_table.setColumnCount(3)
        self.platforms_table.setHorizontalHeaderLabels(["Platform Key", "Platform Name", "Media Type"])
        self.platforms_table.horizontalHeader().setStretchLastSection(True)
        self.platforms_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.platforms_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.platforms_table.setSortingEnabled(True)
        layout.addWidget(self.platforms_table)

        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add New Platform...")
        self.edit_btn = QPushButton("Edit Selected...")
        self.delete_btn = QPushButton("Delete Selected")
        self.refresh_btn = QPushButton("Refresh List")
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        layout.addLayout(button_layout)

        self.add_btn.clicked.connect(self.add_platform)
        self.edit_btn.clicked.connect(self.edit_platform)
        self.platforms_table.doubleClicked.connect(self.edit_platform)
        self.refresh_btn.clicked.connect(self.load_platforms)
        self.delete_btn.clicked.connect(self.delete_platforms)

    def load_platforms(self):
        if not hasattr(self.main_app_ref, 'settings_tab'): return
        
        yaml_path = self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text()
        if not yaml_path or not os.path.exists(yaml_path):
            self.log(f"[INFO] YAML file not found or specified: {yaml_path}")
            self.platforms_table.setRowCount(0)
            return

        platforms = core_logic._load_yaml_file(yaml_path)
        self.platforms_table.setSortingEnabled(False)
        self.platforms_table.setRowCount(0)
        
        for key, data in platforms.items():
            row = self.platforms_table.rowCount()
            self.platforms_table.insertRow(row)
            self.platforms_table.setItem(row, 0, QTableWidgetItem(key))
            self.platforms_table.setItem(row, 1, QTableWidgetItem(data.get("platform", {}).get("name", "N/A")))
            self.platforms_table.setItem(row, 2, QTableWidgetItem(data.get("media_type", "N/A")))
            
            flat_systems = []
            for item in data.get('system', []):
                if isinstance(item, str): flat_systems.append(item)
                elif isinstance(item, dict): flat_systems.extend(item.keys())
            
            platform_data_for_dialog = {
                'platform_key': key,
                'platform_name_full': data.get("platform", {}).get("name"),
                'platform_category': data.get("platform_category", []),
                'media_type': data.get("media_type"),
                'enable_custom_cmd_per_title': data.get("enable_custom_command_line_param_per_software_id", False),
                'emu_name': data.get("emulator", {}).get("name", ''),
                'default_emu': data.get("emulator", {}).get("default_emulator", False),
                'default_emu_cmd_params': data.get("emulator", {}).get("default_command_line_parameters", ''),
                'systems': flat_systems,
                'fuzzy': '', 'include_systems': [], 'exclude_systems': [], 'search_term': ''
            }
            self.platforms_table.item(row, 0).setData(Qt.UserRole, platform_data_for_dialog)
        
        self.platforms_table.resizeColumnsToContents()
        self.platforms_table.setSortingEnabled(True)
        self.log(f"Loaded {len(platforms)} platforms from '{yaml_path}'.")

    def add_platform(self):
        existing_values = self._get_existing_yaml_values()
        dialog = PlatformConfigDialog(self, existing_values=existing_values)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                # For a new platform, we always run the full search
                self.run_search_and_update(data)

    def edit_platform(self):
        selected_rows = self.platforms_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a platform to edit.")
            return

        row = selected_rows[0].row()
        platform_data_for_dialog = self.platforms_table.item(row, 0).data(Qt.UserRole)
        existing_values = self._get_existing_yaml_values()
        
        dialog = PlatformConfigDialog(self, platform_data=platform_data_for_dialog, existing_values=existing_values)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                # When editing, ask the user if they want to re-scan
                reply = QMessageBox.question(self, "Update Options",
                                             "Do you want to re-scan MAME using the new filter criteria to update the system and software lists?\n\n"
                                             "- 'Yes' will re-run the full search (can be slow).\n"
                                             "- 'No' will only save changes to metadata (like name, category, and emulator settings) and the manually entered system list.",
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                             QMessageBox.No)
                if reply == QMessageBox.Cancel:
                    return
                
                if reply == QMessageBox.Yes:
                    self.run_search_and_update(data)
                else: # 'No' was clicked
                    self.run_manual_update(data)

    def _get_existing_yaml_values(self):
        # This helper function is still useful and can be added back as-is.
        categories = set()
        emu_names = set()
        yaml_path = self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text()
        if not yaml_path or not os.path.exists(yaml_path):
            return {'categories': categories, 'emu_names': emu_names}

        platforms = core_logic._load_yaml_file(yaml_path)
        for data in platforms.values():
            cats = data.get('platform_category', [])
            if isinstance(cats, list):
                categories.update(cats)
            if 'emulator' in data and 'name' in data['emulator']:
                emu_names.add(data['emulator']['name'])
        return {'categories': categories, 'emu_names': emu_names}
        
    def process_platform_dialog_data(self, data, is_new=False):
        if is_new:
            self.run_full_search_for_platform(data)
            return
            
        reply = QMessageBox.question(self, "Update Options",
                                     "Do you want to re-scan MAME to update the system and software lists for this platform?\n\n"
                                     "- 'Yes' will re-run the full search (can be slow).\n"
                                     "- 'No' will only save changes to metadata (like name and categories).",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                     QMessageBox.No)

        if reply == QMessageBox.Cancel:
            return
        elif reply == QMessageBox.Yes:
            self.run_full_search_for_platform(data)
        elif reply == QMessageBox.No:
            self.run_metadata_only_update(data)

    def run_manual_update(self, data):
        self.log(f"[INFO] Manually saving platform metadata for '{data['platform_key']}'...")
        yaml_path = self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text()
        
        # --- CORRECTED LOGIC FOR MANUAL UPDATE ---
        # 1. Load the entire existing YAML data
        existing_data = core_logic._load_yaml_file(yaml_path)
        
        # 2. Get the specific platform entry we are editing, or a new empty one
        platform_entry = existing_data.get(data['platform_key'], {})
        
        # 3. Update only the metadata fields from the dialog
        platform_entry['platform'] = {"name": data['platform_name_full']}
        platform_entry['media_type'] = data['media_type']
        
        if data['platform_categories']:
            platform_entry['platform_category'] = data['platform_categories']
        elif 'platform_category' in platform_entry:
            del platform_entry['platform_category']

        if data['emu_name']:
            platform_entry['emulator'] = {
                'name': data['emu_name'],
                'default_emulator': data['default_emu'],
                'default_command_line_parameters': data['default_emu_cmd_params']
            }
        elif 'emulator' in platform_entry:
            del platform_entry['emulator']
        
        # 4. CRITICAL: Update the system list from the text box, but DO NOT touch the software_lists/configs
        # This preserves the existing software data.
        new_system_list_from_dialog = sorted(data['systems'])
        
        # We need to rebuild the 'system' block carefully
        preserved_system_block = []
        existing_system_details = {}
        # First, map existing system details for easy lookup
        for item in platform_entry.get('system', []):
            if isinstance(item, dict):
                sys_name = next(iter(item))
                existing_system_details[sys_name] = item[sys_name]
        
        # Now, build the new list based on the user's manual entry
        for sys_name in new_system_list_from_dialog:
            if sys_name in existing_system_details:
                # If it existed before, carry over its details (software_lists, etc.)
                preserved_system_block.append({sys_name: existing_system_details[sys_name]})
            else:
                # If it's a new system added manually, just add its name
                preserved_system_block.append(sys_name)
        
        platform_entry['system'] = preserved_system_block
        
        # 5. Put the modified platform entry back into the main data structure
        existing_data[data['platform_key']] = platform_entry

        # 6. Save the entire file
        try:
            with open(yaml_path, "w", encoding="utf-8") as f:
                yaml.dump(existing_data, f, default_flow_style=False, sort_keys=False)
            self.log(f"[SUCCESS] Manually updated '{data['platform_key']}' in '{yaml_path}'.")
            self.load_platforms()
        except Exception as e:
            self.log(f"<font color='red'>[ERROR] Failed to save manual update: {e}</font>")

    def run_search_and_update(self, data):
        # This method gathers all data and calls the core search function
        self.log(f"[INFO] Performing full MAME scan to generate/update platform '{data['platform_key']}'...")
        
        xml_source_path = core_logic.APP_CONFIG.get('mess_xml_file')
        if not xml_source_path or not os.path.exists(xml_source_path):
             if not core_logic.ensure_mess_xml_exists():
                 self.log("<font color='red'>MESS XML file is not available. Cannot perform search.</font>")
                 return
             xml_source_path = core_logic.APP_CONFIG.get('mess_xml_file')
        
        source_xml_root = core_logic.get_parsed_mame_xml_root(xml_source_path)
        if source_xml_root is None:
            self.log(f"<font color='red'>Could not parse source XML: {xml_source_path}</font>")
            return
            
        systems_pool = set()
        # Logic to build the initial pool based on user input
        if data['systems'] or data['filter_machine_name_fuzzy'] or data['include_systems']:
            systems_pool.update(data['systems'])
            if data['filter_machine_name_fuzzy']:
                systems_pool.update(core_logic.get_all_mame_systems_by_prefix_from_root(data['filter_machine_name_fuzzy'], source_xml_root))
            if data['include_systems']:
                systems_pool.update(data['include_systems'])
        else:
            systems_pool.update(core_logic.get_all_mame_systems_from_xml_file(xml_source_path))

        # Apply machine filters from the dialog
        if data['filter_machine_description']:
            initial_count = len(systems_pool)
            filtered_set = {
                name for name in systems_pool 
                if all(term.lower() in source_xml_root.find(f"machine[@name='{name}']/description").text.lower()
                       for term in data['filter_machine_description'])
            }
            systems_pool = filtered_set
            self.log(f"[INFO] After machine description filter: {initial_count} -> {len(systems_pool)} systems.")

        if data['filter_machine_sourcefile']:
            initial_count = len(systems_pool)
            filtered_set = {
                name for name in systems_pool
                if data['filter_machine_sourcefile'].lower() in source_xml_root.find(f"machine[@name='{name}']").get("sourcefile", "").lower()
            }
            systems_pool = filtered_set
            self.log(f"[INFO] After machine sourcefile filter: {initial_count} -> {len(systems_pool)} systems.")

        systems_pool.difference_update(data['exclude_systems'])
        systems_to_process = sorted(list(systems_pool))
        
        kwargs = {
            'systems_to_process': systems_to_process,
            'search_term': data['filter_software_description'],
            'output_format': 'yaml',
            'output_file_path': self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text(),
            'source_xml_root': source_xml_root,
            'platform_key': data['platform_key'],
            'platform_name_full': data['platform_name_full'],
            'platform_categories': data['platform_categories'],
            'media_type': data['media_type'],
            'enable_custom_cmd_per_title': data['enable_custom_cmd_per_title'],
            'emu_name': data['emu_name'],
            'default_emu': data['default_emu'],
            'default_emu_cmd_params': data['default_emu_cmd_params'],
            'show_systems_only': False, 'show_extra_info': False, 'sort_by': None,
            'exclude_softlist': [], 'include_softlist': [],
            'software_configs_to_add': {}, 'softlist_configs_to_add': {},
        }
        self._launch_worker(core_logic.perform_mame_search_and_output, **kwargs)

    def run_full_search_for_platform(self, data):
        source_xml_path = core_logic.APP_CONFIG.get('mess_xml_file', 'mess.xml')
        source_xml_root = core_logic.get_parsed_mame_xml_root(source_xml_path)
        if source_xml_root is None:
            self.log(f"<font color='red'>Could not parse source XML: {source_xml_path}</font>")
            return
        
        processed_systems_set = set(data.get('systems', []))
        if data.get('fuzzy'):
            processed_systems_set.update(core_logic.get_all_mame_systems_by_prefix_from_root(data['fuzzy'], source_xml_root))
        if data.get('include_systems'):
            processed_systems_set.update(data['include_systems'])
        if data.get('exclude_systems'):
            processed_systems_set.difference_update(data['exclude_systems'])
            
        systems_to_process = sorted(list(processed_systems_set))
        
        kwargs = {
            'systems_to_process': systems_to_process,
            'search_term': data['search_term'],
            'output_format': 'yaml',
            'output_file_path': self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text(),
            'source_xml_root': source_xml_root,
            'platform_key': data['platform_key'],
            'platform_name_full': data['platform_name_full'],
            'platform_categories': data['platform_categories'],
            'media_type': data['media_type'],
            'enable_custom_cmd_per_title': data['enable_custom_cmd_per_title'],
            'emu_name': data['emu_name'],
            'default_emu': data['default_emu'],
            'default_emu_cmd_params': data['default_emu_cmd_params'],
        }
        self.log(f"[INFO] Performing full search and update for platform '{data['platform_key']}'...")
        self._launch_worker(core_logic.perform_mame_search_and_output, **kwargs)

    def run_metadata_only_update(self, data):
        kwargs = {
            'output_file_path': self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text(),
            'platform_key': data['platform_key'],
            'platform_name_full': data['platform_name_full'],
            'platform_categories': data['platform_categories'],
            'media_type': data['media_type'],
            'enable_custom_cmd_per_title': data['enable_custom_cmd_per_title'],
            'emu_name': data['emu_name'],
            'default_emu': data['default_emu'],
            'default_emu_cmd_params': data['default_emu_cmd_params'],
        }
        self.log(f"[INFO] Performing metadata-only update for platform '{data['platform_key']}'...")
        self._launch_worker(core_logic.update_platform_metadata_only, **kwargs)
        
    def _launch_worker(self, target_func, **kwargs):
        self.main_app_ref.start_long_operation()
        self.thread = QThread()
        self.worker = Worker(target_func, **kwargs)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.main_app_ref.stop_long_operation)
        self.worker.progress.connect(self.log)
        self.worker.error.connect(lambda msg: self.log(f"<font color='red'>{msg}</font>"))
        self.worker.finished.connect(self.load_platforms)

        self.thread.start()

    def delete_platforms(self):
        selected_rows = self.platforms_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select one or more platforms to delete.")
            return

        reply = QMessageBox.question(self, 'Confirm Delete', 
                                     f"Are you sure you want to delete {len(selected_rows)} selected platform(s)?\nThis will permanently modify the YAML file.", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            yaml_path = self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text()
            platforms_data = core_logic._load_yaml_file(yaml_path)

            keys_to_delete = {self.platforms_table.item(r.row(), 0).text() for r in selected_rows}
            
            for key in keys_to_delete:
                if key in platforms_data:
                    del platforms_data[key]
                    self.log(f"[INFO] Deleting platform '{key}' from YAML.")
            
            try:
                with open(yaml_path, "w", encoding="utf-8") as f:
                    yaml.dump(platforms_data, f, default_flow_style=False, sort_keys=False)
                self.log(f"[SUCCESS] '{yaml_path}' updated.")
            except Exception as e:
                self.log(f"<font color='red'>[ERROR] Failed to save YAML after deletion: {e}</font>")
            
            self.load_platforms()


# === Main Search Tab Container ===
# ----------------- REPLACE THE ENTIRE SearchTab CLASS WITH THIS -----------------
class SearchTab(QWidget):
    def __init__(self, log_func, main_app_ref):
        super().__init__()
        self.log = log_func
        self.main_app_ref = main_app_ref
        self.init_ui()

    def init_ui(self):
        # Main layout for the entire tab
        main_layout = QVBoxLayout(self)
        
        # --- Top Section for Search Criteria and Options ---
        top_hbox = QHBoxLayout()
        
        # Group for Search Criteria
        criteria_group = QGroupBox("Search Criteria")
        criteria_layout = QFormLayout(criteria_group)
        
        # Group for All Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)

        top_hbox.addWidget(criteria_group, 2) # Give more space to criteria
        top_hbox.addWidget(options_group, 1)
        main_layout.addLayout(top_hbox)

        # --- Populate Search Criteria ---
        self.systems_te = QTextEdit()
        self.systems_te.setPlaceholderText("Optional: System shortnames. one per line (e.g., nes)")
        self.filter_machine_name_fuzzy_le = QLineEdit()
        self.filter_machine_name_fuzzy_le.setPlaceholderText("System shortnames to search for (e.g., gnw_, jak_)")
        self.filter_machine_description_le = QLineEdit()
        self.filter_machine_description_le.setPlaceholderText("Full machine description (e.g., Nintendo, JAKK)")
        self.filter_machine_sourcefile_le = QLineEdit()
        self.filter_machine_sourcefile_le.setPlaceholderText("Sourcefile that emulates the system (e.g., tvgames, handhelds, tvgames/xavix_adc.cpp)")
        self.filter_software_description_le = QLineEdit()
        self.filter_software_description_le.setPlaceholderText("Full software description/title (e.g., Mario, Donkey Kong)")
        self.limit_le = QLineEdit()
        self.limit_le.setValidator(QIntValidator(0, 99999))
        self.limit_le.setFixedWidth(50)

        criteria_layout.addRow("Systems (Positional):", self.systems_te)
        criteria_layout.addRow("Filter Machine Name (Fuzzy):", self.filter_machine_name_fuzzy_le)
        criteria_layout.addRow("Filter Machine Description:", self.filter_machine_description_le)
        criteria_layout.addRow("Filter Machine Source File:", self.filter_machine_sourcefile_le)
        criteria_layout.addRow("Filter Software Description:", self.filter_software_description_le)
        criteria_layout.addRow("Limit Systems Processed:", self.limit_le)

        # --- Populate Options ---
        self.table_options = TableOptionsWidget()
        self.inclusion_options = InclusionOptionsWidget() # This widget is still useful
        self.yaml_options = YamlOptionsWidget()
        self.emu_options = EmuOptionsWidget()

        options_layout.addWidget(self.table_options)
        options_layout.addWidget(self.inclusion_options)
        options_layout.addWidget(self.yaml_options)
        options_layout.addWidget(self.emu_options)
        options_layout.addStretch()
        
        self.yaml_options.hide()
        self.emu_options.hide()

        # --- Output and Action Section ---
        output_group = QGroupBox("Output")
        output_layout = QHBoxLayout(output_group)
        self.output_format_cb = QComboBox()
        self.output_format_cb.addItems(["table", "yaml", "csv"])
        self.output_file_le = QLineEdit()
        browse_output_btn = QPushButton("...")
        self.run_search_btn = QPushButton("Run Search")
        
        output_layout.addWidget(QLabel("Format:"))
        output_layout.addWidget(self.output_format_cb)
        output_layout.addWidget(QLabel("Output File (optional):"))
        output_layout.addWidget(self.output_file_le, 1)
        output_layout.addWidget(browse_output_btn)
        output_layout.addStretch()
        output_layout.addWidget(self.run_search_btn)
        main_layout.addWidget(output_group)

        # --- Results Table ---
        self.results_table = QTableWidget()
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setSortingEnabled(True)
        main_layout.addWidget(self.results_table)
        
        # --- Connections ---
        self.output_format_cb.currentTextChanged.connect(self.toggle_output_options)
        self.run_search_btn.clicked.connect(self.run_search)
        browse_output_btn.clicked.connect(lambda: self.main_app_ref.settings_tab.browse_file(self.output_file_le, "Select Output File", "All Files (*)"))
    
    def toggle_output_options(self, text):
        is_yaml = (text == 'yaml')
        self.yaml_options.setVisible(is_yaml)
        self.emu_options.setVisible(is_yaml)
        self.table_options.setVisible(not is_yaml)

    def run_search(self):
        try:
            # --- 1. GATHER ARGS FROM UI ---
            args_dict = {
                'systems': [s.strip() for s in self.systems_te.toPlainText().split() if s.strip()],
                'filter_machine_name_fuzzy': self.filter_machine_name_fuzzy_le.text().strip(),
                'filter_machine_description': [s.strip() for s in self.filter_machine_description_le.text().split() if s.strip()],
                'filter_machine_sourcefile': self.filter_machine_sourcefile_le.text().strip(),
                'filter_software_description': self.filter_software_description_le.text().strip(),
                'limit': int(self.limit_le.text()) if self.limit_le.text().isdigit() else None,
                'include_systems': [s.strip() for s in self.inclusion_options.include_systems_le.text().split() if s.strip()],
                'exclude_systems': [s.strip() for s in self.inclusion_options.exclude_systems_le.text().split() if s.strip()],
                'output_format': self.output_format_cb.currentText(),
                'output_file': self.output_file_le.text().strip(),
                # ... and all the other UI elements ...
            }
            from argparse import Namespace
            args = Namespace(**args_dict)

            self.log("[INFO] Starting search...")
            
            # --- 2. ENSURE XML IS AVAILABLE (like in main()) ---
            xml_source_path = core_logic.APP_CONFIG.get('mess_xml_file')
            if not xml_source_path or not os.path.exists(xml_source_path):
                 if not core_logic.ensure_mess_xml_exists():
                     self.log("<font color='red'>MESS XML file is not available. Cannot perform search.</font>")
                     return
                 xml_source_path = core_logic.APP_CONFIG.get('mess_xml_file')

            source_xml_root = core_logic.get_parsed_mame_xml_root(xml_source_path)
            if source_xml_root is None:
                self.log(f"<font color='red'>Could not parse source XML: {xml_source_path}</font>")
                return
            
            # --- 3. BUILD AND FILTER THE SYSTEM POOL (copied from main()) ---
            systems_pool = set()
            user_provided_systems = bool(args.systems or args.filter_machine_name_fuzzy or args.include_systems)
            if user_provided_systems:
                if args.systems: systems_pool.update(args.systems)
                if args.filter_machine_name_fuzzy: systems_pool.update(core_logic.get_all_mame_systems_by_prefix_from_root(args.filter_machine_name_fuzzy, source_xml_root))
                if args.include_systems: systems_pool.update(args.include_systems)
            else:
                systems_pool.update(core_logic.get_all_mame_systems_from_xml_file(xml_source_path))

            self.log(f"[INFO] Initial system pool size: {len(systems_pool)}")

            # --- THIS IS THE CORRECTED FILTER LOGIC ---
            if args.filter_machine_description:
                initial_count = len(systems_pool)
                filtered_set = set()
                for machine_element in source_xml_root.findall("machine"):
                    machine_name = machine_element.get("name")
                    if machine_name in systems_pool:
                        description = machine_element.findtext("description", "")
                        if all(term.lower() in description.lower() for term in args.filter_machine_description):
                            filtered_set.add(machine_name)
                systems_pool = filtered_set
                self.log(f"[INFO] After machine description filter: {initial_count} -> {len(systems_pool)} systems.")

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
                self.log(f"[INFO] After machine sourcefile filter: {initial_count} -> {len(systems_pool)} systems.")
            
            if args.exclude_systems:
                systems_pool.difference_update(args.exclude_systems)
            
            systems_to_process = sorted(list(systems_pool))
            if args.limit is not None:
                systems_to_process = systems_to_process[:args.limit]
            
            # --- 4. PREPARE KWARGS FOR THE WORKER ---
            # (Gathering from UI elements again to ensure they are current)
            table_opts = self.table_options
            yaml_opts = self.yaml_options
            emu_opts = self.emu_options
            
            kwargs = {
                'systems_to_process': systems_to_process,
                'search_term': self.filter_software_description_le.text().strip(),
                'output_format': self.output_format_cb.currentText(),
                'output_file_path': self.output_file_le.text().strip(),
                'platform_key': yaml_opts.platform_key_le.text().strip(), 
                'platform_name_full': yaml_opts.platform_name_full_le.text().strip(),
                'platform_categories': [c.strip() for c in yaml_opts.platform_category_cb.currentText().split() if c.strip()],
                'media_type': yaml_opts.media_type_cb.currentText(),
                'enable_custom_cmd_per_title': emu_opts.enable_custom_cmd_cb.isChecked(),
                'emu_name': emu_opts.emu_name_cb.currentText().strip(), 
                'default_emu': emu_opts.default_emu_cb.isChecked(), 
                'default_emu_cmd_params': emu_opts.default_emu_cmd_params_le.text().strip(),
                'show_systems_only': table_opts.show_systems_only_cb.isChecked(), 
                'show_extra_info': table_opts.show_extra_info_cb.isChecked(),
                'sort_by': table_opts.sort_by_combo.currentText() if table_opts.sort_by_combo.currentIndex() > 0 else None, 
                'source_xml_root': source_xml_root
                # Note: include/exclude softlist and other complex args can be added here if you add UI for them
            }

            # --- 5. LAUNCH WORKER ---
            self.main_app_ref.start_long_operation()
            self.thread = QThread()
            self.worker = Worker(core_logic.perform_mame_search_and_output, **kwargs)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self.main_app_ref.stop_long_operation)
            self.worker.progress.connect(self.log)
            self.worker.error.connect(lambda msg: self.log(f"<font color='red'>{msg}</font>"))
            self.worker.result.connect(self.display_search_results)
            self.worker.finished.connect(self.main_app_ref.platforms_tab.load_platforms)
            self.thread.start()

        except Exception as e:
            self.log(f"<font color='red'>UI Error before starting worker: {e}</font>")
            self.main_app_ref.stop_long_operation()
            
    def display_search_results(self, result_package):
        # The core logic needs to be adapted to return table data instead of printing it
        # For now, we assume it's a tuple of (headers, data)
        if not isinstance(result_package, tuple) or len(result_package) != 2:
            self.log("[INFO] Search finished. Check log for details.")
            return

        headers, data = result_package
        # ... rest of table display logic ...
        self.results_table.setRowCount(len(data))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        self.results_table.resizeColumnsToContents()
        self.log(f"[SUCCESS] Search complete. Displaying {len(data)} results.")
# ----------------- END OF REPLACEMENT -----------------

# === ROM Copy Tab ===
class RomCopyTab(QWidget):
    def __init__(self, log_func, main_app_ref):
        super().__init__()
        self.log = log_func
        self.main_app_ref = main_app_ref
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.softlist_rom_sources_dir_le_display = QLineEdit()
        self.softlist_rom_sources_dir_le_display.setReadOnly(True)
        form_layout.addRow("Source ROMs Dir:", self.softlist_rom_sources_dir_le_display)

        self.out_romset_dir_le_display = QLineEdit()
        self.out_romset_dir_le_display.setReadOnly(True)
        form_layout.addRow("Destination ROMs Dir:", self.out_romset_dir_le_display)

        main_layout.addLayout(form_layout)

        self.copy_btn = QPushButton("Start ROM Copy Operation")
        main_layout.addWidget(self.copy_btn)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.copy_btn.clicked.connect(self.start_rom_copy)
        self.main_app_ref.main_tab_widget.currentChanged.connect(self.update_paths_on_tab_change)

    def update_paths_on_tab_change(self, index):
        if self.main_app_ref.main_tab_widget.widget(index) == self:
            self.update_paths_from_settings()

    def update_paths_from_settings(self):
        if not hasattr(self.main_app_ref, 'settings_tab'):
            return
        self.softlist_rom_sources_dir_le_display.setText(self.main_app_ref.settings_tab.softlist_rom_sources_dir_le.text())
        self.out_romset_dir_le_display.setText(self.main_app_ref.settings_tab.out_romset_dir_le.text())

    def start_rom_copy(self):
        from argparse import Namespace
        args = Namespace(input_file=self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text())

        self.log("[INFO] Starting ROM copy operation...")
        self.main_app_ref.start_long_operation()
        self.thread = QThread()
        self.worker = Worker(core_logic.perform_rom_copy_operation, args=args)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.main_app_ref.stop_long_operation)
        self.worker.progress.connect(self.log)
        self.worker.error.connect(lambda msg: self.log(f"<font color='red'>{msg}</font>"))
        self.thread.start()


# === Settings Tab ===
# --- REPLACE THE ENTIRE SettingsTab CLASS WITH THIS ---
class SettingsTab(QWidget):
    def __init__(self, log_func, main_app_ref):
        super().__init__()
        self.log = log_func
        self.main_app_ref = main_app_ref
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        def create_path_widget(line_edit_obj, browse_button_obj, label_text, is_file=True, file_filter=None):
            line_edit_obj.setPlaceholderText(label_text)
            hbox = QHBoxLayout()
            hbox.addWidget(line_edit_obj)
            hbox.addWidget(browse_button_obj)
            form_layout.addRow(label_text, hbox)
            if is_file:
                browse_button_obj.clicked.connect(lambda: self.browse_file(line_edit_obj, f"Select {label_text}", file_filter))
            else:
                browse_button_obj.clicked.connect(lambda: self.browse_directory(line_edit_obj, f"Select {label_text}"))

        # --- REVISED UI ELEMENTS ---
        self.mame_executable_le = QLineEdit()
        self.browse_mame_btn = QPushButton("...")
        create_path_widget(self.mame_executable_le, self.browse_mame_btn, "MAME Executable Path:", True, "MAME Executable (mame.exe)")

        # Add the MAME Version field
        self.mess_version_le = QLineEdit()
        self.mess_version_le.setPlaceholderText("e.g., 0.278 (auto-detected if blank)")
        form_layout.addRow("MAME Version:", self.mess_version_le)
        
        self.softlist_rom_sources_dir_le = QLineEdit()
        self.browse_softlist_btn = QPushButton("...")
        create_path_widget(self.softlist_rom_sources_dir_le, self.browse_softlist_btn, "Softlist ROMs Source Dir:", False)

        self.out_romset_dir_le = QLineEdit()
        self.browse_out_romset_btn = QPushButton("...")
        create_path_widget(self.out_romset_dir_le, self.browse_out_romset_btn, "Output ROMset Dir:", False)

        self.system_softlist_yaml_file_le = QLineEdit()
        self.browse_yaml_btn = QPushButton("...")
        create_path_widget(self.system_softlist_yaml_file_le, self.browse_yaml_btn, "System Softlist YAML:", True, "YAML Files (*.yaml *.yml)")

        # Make mess.ini optional and less prominent
        self.mess_ini_path_le = QLineEdit()
        self.browse_mess_ini_btn = QPushButton("...")
        create_path_widget(self.mess_ini_path_le, self.browse_mess_ini_btn, "MESS.ini Path (for split):", True, "INI Files (*.ini)")
        # --- END REVISED UI ---

        main_layout.addLayout(form_layout)
        
        self.save_settings_btn = QPushButton("Save Settings to config.yaml")
        main_layout.addWidget(self.save_settings_btn)
        main_layout.addStretch()

        self.save_settings_btn.clicked.connect(self.save_settings)

    def browse_file(self, line_edit, title, file_filter):
        start_dir = os.path.dirname(line_edit.text()) if os.path.dirname(line_edit.text()) else os.getcwd()
        file_path, _ = QFileDialog.getOpenFileName(self, title, start_dir, file_filter)
        if file_path:
            line_edit.setText(file_path)

    def browse_directory(self, line_edit, title):
        start_dir = line_edit.text() if os.path.isdir(line_edit.text()) else os.getcwd()
        dir_path = QFileDialog.getExistingDirectory(self, title, start_dir)
        if dir_path:
            line_edit.setText(dir_path)

    def load_settings_from_core_config(self):
        """Loads settings from the global APP_CONFIG dictionary."""
        self.mame_executable_le.setText(core_logic.APP_CONFIG.get("mame_executable", ""))
        self.mess_version_le.setText(core_logic.APP_CONFIG.get("mess_version", ""))
        self.softlist_rom_sources_dir_le.setText(core_logic.APP_CONFIG.get("softlist_rom_sources_dir", ""))
        self.out_romset_dir_le.setText(core_logic.APP_CONFIG.get("out_romset_dir", ""))
        self.system_softlist_yaml_file_le.setText(core_logic.APP_CONFIG.get("system_softlist_yaml_file", "system_softlist.yml"))
        self.mess_ini_path_le.setText(core_logic.APP_CONFIG.get("mess_ini_path", ""))
        self.log("[INFO] Settings tab populated from config.")

    def save_settings(self):
        """Saves settings from the UI to the global APP_CONFIG and then to file."""
        # --- REVISED SAVE LOGIC ---
        core_logic.APP_CONFIG["mame_executable"] = self.mame_executable_le.text()
        
        # Auto-detect version if the field is empty
        mess_version = self.mess_version_le.text().strip()
        if not mess_version and self.mame_executable_le.text():
            self.log("[INFO] MAME Version field is empty, attempting to auto-detect from executable...")
            detected_version = core_logic.get_mame_version_from_exe(self.mame_executable_le.text())
            if detected_version:
                mess_version = detected_version
                self.mess_version_le.setText(mess_version) # Update UI
                self.log(f"[INFO] Auto-detected version: {mess_version}")
            else:
                self.log("[WARNING] Could not auto-detect version. Please enter it manually.")
        core_logic.APP_CONFIG["mess_version"] = mess_version

        core_logic.APP_CONFIG["softlist_rom_sources_dir"] = self.softlist_rom_sources_dir_le.text()
        core_logic.APP_CONFIG["out_romset_dir"] = self.out_romset_dir_le.text()
        core_logic.APP_CONFIG["system_softlist_yaml_file"] = self.system_softlist_yaml_file_le.text()
        core_logic.APP_CONFIG["mess_ini_path"] = self.mess_ini_path_le.text()
        # No need to save mess_xml_file, as it's dynamic
        
        if core_logic.save_configuration():
            self.log("[SUCCESS] Settings saved to config.yaml.")
            QMessageBox.information(self, "Settings Saved", "Configuration saved successfully.")
        else:
            self.log("<font color='red'>[ERROR] Failed to save settings to config.yaml.</font>")
            QMessageBox.critical(self, "Save Error", "Failed to save settings.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MameRomManagerApp()
    window.show()
    sys.exit(app.exec())