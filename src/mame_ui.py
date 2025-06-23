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

        # Create tabs
        self.platforms_tab = PlatformsTab(self.log_output.append, self)
        self.search_tab = SearchTab(self.log_output.append, self)
        self.rom_copy_tab = RomCopyTab(self.log_output.append, self)
        self.settings_tab = SettingsTab(self.log_output.append, self)

        # Add tabs
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


# === Platform Configuration Dialog ===
class PlatformConfigDialog(QDialog):
    def __init__(self, parent=None, platform_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Platform Configuration")
        self.setGeometry(150, 150, 600, 500)

        self.platform_data = platform_data if platform_data is not None else {}
        self.is_editing = 'platform_key' in self.platform_data and self.platform_data['platform_key']

        self.init_ui()
        if self.is_editing:
            self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Basic Info
        self.platform_key_le = QLineEdit()
        self.platform_name_full_le = QLineEdit()
        self.platform_category_le = QLineEdit()
        self.media_type_cb = QComboBox()
        self.media_type_cb.addItems(["cart", "disk", "cdrom", "cassette", "rom"])
        
        if self.is_editing:
            self.platform_key_le.setReadOnly(True)
            self.platform_key_le.setStyleSheet("background-color: #f0f0f0;")

        form_layout.addRow("Platform Key:", self.platform_key_le)
        form_layout.addRow("Platform Name:", self.platform_name_full_le)
        form_layout.addRow("Platform Category(s):", self.platform_category_le)
        self.platform_category_le.setPlaceholderText("Space-separated list")
        form_layout.addRow("Media Type:", self.media_type_cb)
        layout.addLayout(form_layout)

        # Emulator Options
        self.emu_options = EmuOptionsWidget(self)
        layout.addWidget(self.emu_options)

        # System Sourcing
        sourcing_group = QGroupBox("System Sourcing")
        sourcing_layout = QFormLayout(sourcing_group)
        self.systems_te = QTextEdit()
        self.fuzzy_le = QLineEdit()
        self.search_term_le = QLineEdit()
        self.include_systems_le = QLineEdit()
        self.exclude_systems_le = QLineEdit()
        
        self.systems_te.setPlaceholderText("One per line, or space/comma separated")
        self.include_systems_le.setPlaceholderText("Space separated")
        self.exclude_systems_le.setPlaceholderText("Space separated")

        sourcing_layout.addRow("Systems:", self.systems_te)
        sourcing_layout.addRow("Fuzzy Prefix:", self.fuzzy_le)
        sourcing_layout.addRow("Include Systems:", self.include_systems_le)
        sourcing_layout.addRow("Exclude Systems:", self.exclude_systems_le)
        sourcing_layout.addRow("Software Search Term:", self.search_term_le)
        layout.addWidget(sourcing_group)

        # Dialog Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def load_data(self):
        self.platform_key_le.setText(self.platform_data.get('platform_key', ''))
        self.platform_name_full_le.setText(self.platform_data.get('platform_name_full', ''))
        self.platform_category_le.setText(' '.join(self.platform_data.get('platform_category', [])))
        
        media_type_index = self.media_type_cb.findText(self.platform_data.get('media_type', 'cart'))
        if media_type_index >= 0:
            self.media_type_cb.setCurrentIndex(media_type_index)

        self.emu_options.enable_custom_cmd_cb.setChecked(self.platform_data.get('enable_custom_cmd_per_title', False))
        self.emu_options.emu_name_le.setText(self.platform_data.get('emu_name', ''))
        self.emu_options.default_emu_cb.setChecked(self.platform_data.get('default_emu', False))
        self.emu_options.default_emu_cmd_params_le.setText(self.platform_data.get('default_emu_cmd_params', ''))
        
        self.systems_te.setText('\n'.join(self.platform_data.get('systems', [])))
        self.fuzzy_le.setText(self.platform_data.get('fuzzy', ''))
        self.include_systems_le.setText(' '.join(self.platform_data.get('include_systems', [])))
        self.exclude_systems_le.setText(' '.join(self.platform_data.get('exclude_systems', [])))
        self.search_term_le.setText(self.platform_data.get('search_term', ''))

    def get_data(self):
        platform_key = self.platform_key_le.text().strip()
        if not platform_key:
            QMessageBox.warning(self, "Input Required", "Platform Key is a mandatory field.")
            return None

        systems_raw = self.systems_te.toPlainText().strip()
        systems = [s.strip() for s in systems_raw.replace(',', ' ').split() if s.strip()]
        fuzzy = self.fuzzy_le.text().strip()
        include_systems = [s.strip() for s in self.include_systems_le.text().split() if s.strip()]
        
        if not systems and not fuzzy and not include_systems:
            QMessageBox.warning(self, "Input Required", "You must provide at least one system name, a fuzzy prefix, or an included system.")
            return None
            
        return {
            'platform_key': platform_key,
            'platform_name_full': self.platform_name_full_le.text().strip(),
            'platform_categories': [c.strip() for c in self.platform_category_le.text().split() if c.strip()],
            'media_type': self.media_type_cb.currentText(),
            'systems': systems,
            'fuzzy': fuzzy,
            'include_systems': include_systems,
            'exclude_systems': [s.strip() for s in self.exclude_systems_le.text().split() if s.strip()],
            'search_term': self.search_term_le.text().strip(),
            'enable_custom_cmd_per_title': self.emu_options.enable_custom_cmd_cb.isChecked(),
            'emu_name': self.emu_options.emu_name_le.text().strip(),
            'default_emu': self.emu_options.default_emu_cb.isChecked(),
            'default_emu_cmd_params': self.emu_options.default_emu_cmd_params_le.text().strip(),
        }


# === Platforms Tab ===
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
        dialog = PlatformConfigDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                self.process_platform_dialog_data(data, is_new=True)

    def edit_platform(self):
        selected_rows = self.platforms_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a platform to edit.")
            return

        row = selected_rows[0].row()
        platform_data_for_dialog = self.platforms_table.item(row, 0).data(Qt.UserRole)
        
        dialog = PlatformConfigDialog(self, platform_data=platform_data_for_dialog)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                self.process_platform_dialog_data(data, is_new=False)

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
        self.worker.finished.connect(self.main_app_ref.stop_long_operation)
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


# === Reusable UI Components for Search Tabs ===
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
    def __init__(self, parent=None):
        super().__init__("YAML Platform Options", parent)
        layout = QFormLayout(self)
        self.platform_key_le = QLineEdit()
        self.platform_name_full_le = QLineEdit()
        self.platform_category_le = QLineEdit()
        self.media_type_cb = QComboBox()
        self.media_type_cb.addItems(["cart", "disk", "cdrom", "cassette", "rom"])

        layout.addRow("Platform Key:", self.platform_key_le)
        layout.addRow("Platform Name:", self.platform_name_full_le)
        layout.addRow("Platform Category(s):", self.platform_category_le)
        self.platform_category_le.setPlaceholderText("Space-separated list")
        layout.addRow("Media Type:", self.media_type_cb)

class EmuOptionsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Emulator Options (for YAML)", parent)
        layout = QFormLayout(self)
        self.enable_custom_cmd_cb = QCheckBox("Enable Custom Cmd Per Title")
        self.emu_name_le = QLineEdit()
        self.default_emu_cb = QCheckBox("Set as Default Emulator")
        self.default_emu_cmd_params_le = QLineEdit()

        layout.addRow(self.enable_custom_cmd_cb)
        layout.addRow("Emulator Name:", self.emu_name_le)
        layout.addRow(self.default_emu_cb)
        layout.addRow("Default Cmd Params:", self.default_emu_cmd_params_le)

class InclusionOptionsWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("System Inclusions / Exclusions", parent)
        layout = QFormLayout(self)
        self.include_systems_le = QLineEdit()
        self.exclude_systems_le = QLineEdit()
        self.include_systems_le.setPlaceholderText("Space-separated list")
        self.exclude_systems_le.setPlaceholderText("Space-separated list")

        layout.addRow("Include Systems:", self.include_systems_le)
        layout.addRow("Exclude Systems:", self.exclude_systems_le)


# === Main Search Tab Container ===
class SearchTab(QWidget):
    def __init__(self, log_func, main_app_ref):
        super().__init__()
        self.log = log_func
        self.main_app_ref = main_app_ref
        
        main_layout = QVBoxLayout(self)
        self.search_tabs = QTabWidget()
        main_layout.addWidget(self.search_tabs)

        # Create individual search tabs, storing their components
        self.by_name_tab_components = self._create_search_tab("by-name")
        self.by_xml_tab_components = self._create_by_xml_tab()
        self.by_filter_tab_components = self._create_by_filter_tab()
        self.by_sourcefile_tab_components = self._create_by_sourcefile_tab()

        self.search_tabs.addTab(self.by_name_tab_components['page'], "By Name")
        self.search_tabs.addTab(self.by_xml_tab_components['page'], "By XML File")
        self.search_tabs.addTab(self.by_filter_tab_components['page'], "By Description Filter")
        self.search_tabs.addTab(self.by_sourcefile_tab_components['page'], "By Source File")

        self.results_table = QTableWidget()
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.results_table)

    def _create_base_search_layout(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # --- Options Group (now on the left) ---
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        
        table_options = TableOptionsWidget()
        yaml_options = YamlOptionsWidget()
        emu_options = EmuOptionsWidget()
        inclusion_options = InclusionOptionsWidget()
        
        # Add widgets to layout
        options_layout.addWidget(table_options)
        options_layout.addWidget(inclusion_options)
        options_layout.addWidget(yaml_options)
        options_layout.addWidget(emu_options)
        options_layout.addStretch()

        # --- Main content area (with search criteria on right) ---
        main_hbox = QHBoxLayout()
        search_criteria_group = QGroupBox("Search Criteria")
        search_layout = QFormLayout(search_criteria_group)
        
        main_hbox.addWidget(options_group, 1)
        main_hbox.addWidget(search_criteria_group, 2)
        
        layout.addLayout(main_hbox)

        # Hide YAML/Emu options by default
        yaml_options.hide()
        emu_options.hide()

        # --- Output and Run Section ---
        output_group = QGroupBox("Output")
        output_layout = QHBoxLayout(output_group)
        output_format_cb = QComboBox()
        output_format_cb.addItems(["table", "yaml", "csv"])
        output_file_le = QLineEdit()
        browse_output_btn = QPushButton("...")
        run_search_btn = QPushButton("Run Search")
        
        output_layout.addWidget(QLabel("Format:"))
        output_layout.addWidget(output_format_cb)
        output_layout.addWidget(QLabel("Output File:"))
        output_layout.addWidget(output_file_le, 1)
        output_layout.addWidget(browse_output_btn)
        output_layout.addStretch()
        output_layout.addWidget(run_search_btn)
        
        layout.addWidget(output_group)
        
        # Connect signal to show/hide options
        output_format_cb.currentTextChanged.connect(lambda text: self.toggle_yaml_options(text, yaml_options, emu_options))

        return {
            'page': page, 'search_layout': search_layout,
            'table_options': table_options, 'yaml_options': yaml_options,
            'emu_options': emu_options, 'inclusion_options': inclusion_options,
            'output_format_cb': output_format_cb, 'output_file_le': output_file_le,
            'browse_output_btn': browse_output_btn, 'run_search_btn': run_search_btn
        }

    def toggle_yaml_options(self, text, yaml_widget, emu_widget):
        is_yaml = (text == 'yaml')
        yaml_widget.setVisible(is_yaml)
        emu_widget.setVisible(is_yaml)

    def _create_search_tab(self, mode):
        c = self._create_base_search_layout()
        
        c['limit_le'] = QLineEdit()
        c['limit_le'].setValidator(QIntValidator(0, 99999))
        c['limit_le'].setFixedWidth(50)

        if mode == "by-name":
            c['systems_te'] = QTextEdit()
            c['systems_te'].setPlaceholderText("Enter system names, one per line or separated by space/comma.")
            c['fuzzy_le'] = QLineEdit()
            c['search_term_le'] = QLineEdit()
            c['search_layout'].addRow("Systems:", c['systems_te'])
            c['search_layout'].addRow("Fuzzy Prefix:", c['fuzzy_le'])
            c['search_layout'].addRow("Software Search Term:", c['search_term_le'])
            c['run_search_btn'].clicked.connect(lambda: self.run_generic_search(c, self._get_by_name_args))
        elif mode == "by-xml":
            c['xml_filepath_le'] = QLineEdit()
            c['xml_browse_btn'] = QPushButton("...")
            xml_hbox = QHBoxLayout()
            xml_hbox.addWidget(c['xml_filepath_le'])
            xml_hbox.addWidget(c['xml_browse_btn'])
            c['search_layout'].addRow("XML File Path:", xml_hbox)
            c['search_term_le'] = QLineEdit()
            c['search_layout'].addRow("Software Search Term:", c['search_term_le'])
            c['xml_browse_btn'].clicked.connect(lambda: self.main_app_ref.settings_tab.browse_file(c['xml_filepath_le'], "Select MAME XML", "XML Files (*.xml)"))
            c['run_search_btn'].clicked.connect(lambda: self.run_generic_search(c, self._get_by_xml_args))
        elif mode == "by-filter":
            c['description_terms_le'] = QLineEdit()
            c['description_terms_le'].setPlaceholderText("Space-separated list of terms (e.g., \"in 1\" handheld)")
            c['search_layout'].addRow("Description Contains:", c['description_terms_le'])
            c['run_search_btn'].clicked.connect(lambda: self.run_generic_search(c, self._get_by_filter_args))
        elif mode == "by-sourcefile":
            c['sourcefile_term_le'] = QLineEdit()
            c['sourcefile_term_le'].setPlaceholderText("e.g., xavix.cpp or just xavix")
            c['search_layout'].addRow("Source File Contains:", c['sourcefile_term_le'])
            c['run_search_btn'].clicked.connect(lambda: self.run_generic_search(c, self._get_by_sourcefile_args))
        
        c['search_layout'].addRow("Limit Results:", c['limit_le'])
        return c
    
    def _create_by_name_tab(self):
        c = self._create_base_search_layout()
        
        c['systems_te'] = QTextEdit()
        c['systems_te'].setPlaceholderText("Enter system names, one per line or separated by space/comma.")
        c['fuzzy_le'] = QLineEdit()
        c['search_term_le'] = QLineEdit()
        c['limit_le'] = QLineEdit()
        c['limit_le'].setValidator(QIntValidator(0, 99999))
        c['limit_le'].setFixedWidth(50)
        
        c['search_layout'].addRow("Systems:", c['systems_te'])
        c['search_layout'].addRow("Fuzzy Prefix:", c['fuzzy_le'])
        c['search_layout'].addRow("Software Search Term:", c['search_term_le'])
        c['search_layout'].addRow("Limit Results:", c['limit_le'])
        
        c['run_search_btn'].clicked.connect(lambda: self.run_generic_search(c, self._get_by_name_args))
        return c

    def _create_by_xml_tab(self):
        c = self._create_base_search_layout()

        c['xml_filepath_le'] = QLineEdit()
        c['xml_browse_btn'] = QPushButton("...")
        xml_hbox = QHBoxLayout()
        xml_hbox.addWidget(c['xml_filepath_le'])
        xml_hbox.addWidget(c['xml_browse_btn'])
        c['search_layout'].addRow("XML File Path:", xml_hbox)
        
        c['search_term_le'] = QLineEdit()
        c['search_layout'].addRow("Software Search Term:", c['search_term_le'])

        c['limit_le'] = QLineEdit()
        c['limit_le'].setValidator(QIntValidator(0, 99999))
        c['limit_le'].setFixedWidth(50)
        c['search_layout'].addRow("Limit Results:", c['limit_le'])

        c['xml_browse_btn'].clicked.connect(lambda: self.main_app_ref.settings_tab.browse_file(c['xml_filepath_le'], "Select MAME XML", "XML Files (*.xml)"))
        c['run_search_btn'].clicked.connect(lambda: self.run_generic_search(c, self._get_by_xml_args))
        return c

    def _create_by_filter_tab(self):
        c = self._create_base_search_layout()
        c['description_terms_le'] = QLineEdit()
        c['description_terms_le'].setPlaceholderText("Space-separated list of terms (e.g., \"in 1\" handheld)")
        c['search_layout'].addRow("Description Contains:", c['description_terms_le'])
        
        c['limit_le'] = QLineEdit()
        c['limit_le'].setValidator(QIntValidator(0, 99999))
        c['limit_le'].setFixedWidth(50)
        c['search_layout'].addRow("Limit Results:", c['limit_le'])
        
        c['run_search_btn'].clicked.connect(lambda: self.run_generic_search(c, self._get_by_filter_args))
        return c

    def _create_by_sourcefile_tab(self):
        c = self._create_base_search_layout()
        c['sourcefile_term_le'] = QLineEdit()
        c['sourcefile_term_le'].setPlaceholderText("e.g., xavix.cpp or just xavix")
        c['search_layout'].addRow("Source File Contains:", c['sourcefile_term_le'])
        
        c['limit_le'] = QLineEdit()
        c['limit_le'].setValidator(QIntValidator(0, 99999))
        c['limit_le'].setFixedWidth(50)
        c['search_layout'].addRow("Limit Results:", c['limit_le'])
        
        c['run_search_btn'].clicked.connect(lambda: self.run_generic_search(c, self._get_by_sourcefile_args))
        return c

    def run_generic_search(self, components, get_specific_args_func):
        try:
            initial_args_dict = get_specific_args_func(components)
            if initial_args_dict is None: return

            from argparse import Namespace
            initial_args = Namespace(**initial_args_dict)
            
            xml_source_path = core_logic.APP_CONFIG.get('mess_xml_file', 'mess.xml')
            self.log(f"[INFO] Using source XML for search: {xml_source_path}")
            source_xml_root = core_logic.get_parsed_mame_xml_root(xml_source_path)
            if source_xml_root is None:
                self.log(f"<font color='red'>Could not parse source XML: {xml_source_path}</font>")
                return

            processed_systems_set = set()
            if initial_args.search_mode == 'by-name':
                processed_systems_set.update(initial_args.systems)
                if hasattr(initial_args, 'fuzzy') and initial_args.fuzzy:
                    processed_systems_set.update(core_logic.get_all_mame_systems_by_prefix_from_root(initial_args.fuzzy, source_xml_root))
            elif initial_args.search_mode == 'by-xml':
                processed_systems_set.update(core_logic.get_all_mame_systems_from_xml_file(initial_args.xml_filepath))
            elif initial_args.search_mode == 'by-filter':
                for machine in source_xml_root.findall("machine"):
                    desc = machine.findtext("description", "").lower()
                    if any(term.lower() in desc for term in initial_args.description_terms):
                        processed_systems_set.add(machine.get("name"))
            elif initial_args.search_mode == 'by-sourcefile':
                 for machine in source_xml_root.findall("machine"):
                    if initial_args.sourcefile_term.lower() in machine.get("sourcefile", "").lower():
                        processed_systems_set.add(machine.get("name"))
            
            inclusion_opts = components['inclusion_options']
            include_systems = [s.strip() for s in inclusion_opts.include_systems_le.text().split() if s.strip()]
            exclude_systems = [s.strip() for s in inclusion_opts.exclude_systems_le.text().split() if s.strip()]
            if include_systems: processed_systems_set.update(include_systems)
            if exclude_systems: processed_systems_set.difference_update(exclude_systems)
            
            systems_to_process = sorted(list(processed_systems_set))
            
            limit_text = components['limit_le'].text()
            limit = int(limit_text) if limit_text.isdigit() else None
            if limit is not None:
                systems_to_process = systems_to_process[:limit]

            table_opts = components['table_options']
            yaml_opts = components['yaml_options']
            emu_opts = components['emu_options']
            output_format = components['output_format_cb'].currentText()
            output_file = components['output_file_le'].text()

            if output_format == "csv" and not output_file:
                QMessageBox.warning(self, "Output File Required", "An output file must be specified for CSV format.")
                return

            if output_format == "yaml":
                if not output_file:
                    output_file = self.main_app_ref.settings_tab.system_softlist_yaml_file_le.text()
                if not all([yaml_opts.platform_key_le.text(), yaml_opts.platform_name_full_le.text(), yaml_opts.media_type_cb.currentText()]):
                    QMessageBox.warning(self, "YAML Info Required", "Platform Key, Name, and Media Type are required for YAML output.")
                    return

            kwargs = {
                'systems_to_process': systems_to_process,
                'search_term': getattr(initial_args, 'search_term', ''),
                'search_mode': initial_args.search_mode,
                'output_format': output_format,
                'output_file_path': output_file,
                'show_systems_only': table_opts.show_systems_only_cb.isChecked(),
                'show_extra_info': table_opts.show_extra_info_cb.isChecked(),
                'sort_by': table_opts.sort_by_combo.currentText() if table_opts.sort_by_combo.currentIndex() > 0 else None,
                'platform_key': yaml_opts.platform_key_le.text(),
                'platform_name_full': yaml_opts.platform_name_full_le.text(),
                'platform_categories': [c.strip() for c in yaml_opts.platform_category_le.text().split() if c.strip()],
                'media_type': yaml_opts.media_type_cb.currentText(),
                'enable_custom_cmd_per_title': emu_opts.enable_custom_cmd_cb.isChecked(),
                'emu_name': emu_opts.emu_name_le.text(),
                'default_emu': emu_opts.default_emu_cb.isChecked(),
                'default_emu_cmd_params': emu_opts.default_emu_cmd_params_le.text(),
                'source_xml_root': source_xml_root
            }

            self.log(f"[INFO] Starting search with mode '{kwargs['search_mode']}'...")
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

    def _get_by_name_args(self, c):
        systems_raw = c['systems_te'].toPlainText().strip()
        systems = [s.strip() for s in systems_raw.replace(',', ' ').split() if s.strip()]
        fuzzy = c['fuzzy_le'].text().strip()
        if not systems and not fuzzy:
            QMessageBox.warning(self, "Input Required", "Please enter at least one system name or a fuzzy prefix.")
            return None
        return {
            'search_mode': 'by-name',
            'systems': systems,
            'fuzzy': fuzzy,
            'search_term': c['search_term_le'].text().strip()
        }

    def _get_by_xml_args(self, c):
        xml_path = c['xml_filepath_le'].text().strip()
        if not xml_path:
            QMessageBox.warning(self, "Input Required", "Please specify an XML file path.")
            return None
        return {
            'search_mode': 'by-xml',
            'xml_filepath': xml_path,
            'search_term': c['search_term_le'].text().strip()
        }

    def _get_by_filter_args(self, c):
        terms_raw = c['description_terms_le'].text().strip()
        terms = [t.strip() for t in terms_raw.split() if t.strip()]
        if not terms:
            QMessageBox.warning(self, "Input Required", "Please enter at least one description term.")
            return None
        return {
            'search_mode': 'by-filter',
            'description_terms': terms,
            'search_term': ''
        }

    def _get_by_sourcefile_args(self, c):
        term = c['sourcefile_term_le'].text().strip()
        if not term:
            QMessageBox.warning(self, "Input Required", "Please enter a source file term.")
            return None
        return {
            'search_mode': 'by-sourcefile',
            'sourcefile_term': term,
            'search_term': ''
        }
        
    def display_search_results(self, result_package):
        if not isinstance(result_package, tuple) or len(result_package) != 2:
            return 
        
        headers, data = result_package
        if not data:
            self.log("[i] No matching items found.")
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            return

        self.results_table.setRowCount(len(data))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        
        self.results_table.resizeColumnsToContents()
        self.log(f"[SUCCESS] Search complete. Displaying {len(data)} results.")


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

        self.mame_executable_le = QLineEdit()
        self.browse_mame_btn = QPushButton("...")
        create_path_widget(self.mame_executable_le, self.browse_mame_btn, "MAME Executable Path:", True, "MAME Executable (mame.exe)")

        self.softlist_rom_sources_dir_le = QLineEdit()
        self.browse_softlist_btn = QPushButton("...")
        create_path_widget(self.softlist_rom_sources_dir_le, self.browse_softlist_btn, "Softlist ROMs Source Dir:", False)

        self.out_romset_dir_le = QLineEdit()
        self.browse_out_romset_btn = QPushButton("...")
        create_path_widget(self.out_romset_dir_le, self.browse_out_romset_btn, "Output ROMset Dir:", False)

        self.system_softlist_yaml_file_le = QLineEdit()
        self.browse_yaml_btn = QPushButton("...")
        create_path_widget(self.system_softlist_yaml_file_le, self.browse_yaml_btn, "System Softlist YAML:", True, "YAML Files (*.yaml *.yml)")

        self.mess_ini_path_le = QLineEdit()
        self.browse_mess_ini_btn = QPushButton("...")
        create_path_widget(self.mess_ini_path_le, self.browse_mess_ini_btn, "MESS.ini Path:", True, "INI Files (*.ini)")

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
        self.softlist_rom_sources_dir_le.setText(core_logic.APP_CONFIG.get("softlist_rom_sources_dir", ""))
        self.out_romset_dir_le.setText(core_logic.APP_CONFIG.get("out_romset_dir", ""))
        self.system_softlist_yaml_file_le.setText(core_logic.APP_CONFIG.get("system_softlist_yaml_file", "system_softlist.yml"))
        self.mess_ini_path_le.setText(core_logic.APP_CONFIG.get("mess_ini_path", ""))
        self.log("[INFO] Settings tab populated from config.")

    def save_settings(self):
        """Saves settings from the UI to the global APP_CONFIG and then to file."""
        core_logic.APP_CONFIG["mame_executable"] = self.mame_executable_le.text()
        core_logic.APP_CONFIG["softlist_rom_sources_dir"] = self.softlist_rom_sources_dir_le.text()
        core_logic.APP_CONFIG["out_romset_dir"] = self.out_romset_dir_le.text()
        core_logic.APP_CONFIG["system_softlist_yaml_file"] = self.system_softlist_yaml_file_le.text()
        core_logic.APP_CONFIG["mess_ini_path"] = self.mess_ini_path_le.text()
        
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