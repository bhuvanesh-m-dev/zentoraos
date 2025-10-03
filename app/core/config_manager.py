#!/usr/bin/env python3
"""
Configuration Manager for Zentora
Handles ~/.config/zentora/config.json
"""

import os
import json


class ConfigManager:
    """Manage Zentora configuration"""
    
    CONFIG_DIR = os.path.expanduser("~/.config/zentora")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
    MODULES_DIR = os.path.join(CONFIG_DIR, "modules")
    
    DEFAULT_CONFIG = {
        "version": "1.0.0",
        "first_run": True,
        "modules": {
            "zentora_system": {"enabled": False, "installed": False, "version": "0.0.0"},
            "zentora_ai": {"enabled": False, "installed": False, "version": "0.0.0"},
            "zentora_dev": {"enabled": False, "installed": False, "version": "0.0.0"},
            "zentora_media": {"enabled": False, "installed": False, "version": "0.0.0"}
        },
        "settings": {
            "theme": "light",
            "auto_update": True,
            "telemetry": False,
            "show_notifications": True,
            "minimize_to_tray": False
        },
        "ai": {
            "default_model": "llama3",
            "max_tokens": 2048,
            "temperature": 0.7
        }
    }
    
    def __init__(self):
        """Initialize config manager"""
        self._ensure_config_dir()
        self.config = self._load_config()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        os.makedirs(self.MODULES_DIR, exist_ok=True)
    
    def _load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to handle new config keys
                    return self._merge_configs(self.DEFAULT_CONFIG.copy(), loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # First run
            config = self.DEFAULT_CONFIG.copy()
            self.save_config(config)
            return config
    
    def _merge_configs(self, default, loaded):
        """Merge loaded config with defaults"""
        for key, value in default.items():
            if key not in loaded:
                loaded[key] = value
            elif isinstance(value, dict) and isinstance(loaded[key], dict):
                loaded[key] = self._merge_configs(value, loaded[key])
        return loaded
    
    def save_config(self, config=None):
        """
        Save configuration to file
        
        Args:
            config: Config dict to save (uses self.config if None)
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """
        Get config value using dot notation
        
        Args:
            key: Dot-separated key path (e.g., 'modules.zentora_ai.installed')
            default: Default value if key not found
            
        Returns:
            Config value or default
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key, value):
        """
        Set config value using dot notation
        
        Args:
            key: Dot-separated key path
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
    
    def mark_module_installed(self, module_name, version="1.0.0"):
        """
        Mark a module as installed
        
        Args:
            module_name: Name of the module
            version: Version number
        """
        self.set(f"modules.{module_name}.installed", True)
        self.set(f"modules.{module_name}.enabled", True)
        self.set(f"modules.{module_name}.version", version)
        
        # Create marker file
        marker_dir = os.path.join(self.MODULES_DIR, module_name)
        os.makedirs(marker_dir, exist_ok=True)
        marker_file = os.path.join(marker_dir, ".installed")
        with open(marker_file, 'w') as f:
            f.write(version)
    
    def mark_module_uninstalled(self, module_name):
        """
        Mark a module as uninstalled
        
        Args:
            module_name: Name of the module
        """
        self.set(f"modules.{module_name}.installed", False)
        self.set(f"modules.{module_name}.enabled", False)
        
        # Remove marker file
        marker_file = os.path.join(self.MODULES_DIR, module_name, ".installed")
        if os.path.exists(marker_file):
            os.remove(marker_file)
    
    def is_module_installed(self, module_name):
        """
        Check if module is installed
        
        Args:
            module_name: Name of the module
            
        Returns:
            bool: True if installed
        """
        return self.get(f"modules.{module_name}.installed", False)
    
    def get_module_version(self, module_name):
        """Get installed module version"""
        return self.get(f"modules.{module_name}.version", "0.0.0")
    
    def mark_first_run_complete(self):
        """Mark first run as complete"""
        self.set("first_run", False)
    
    def is_first_run(self):
        """Check if this is first run"""
        return self.get("first_run", True)
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()


if __name__ == "__main__":
    # Test config manager
    config = ConfigManager()
    print("Config file:", config.CONFIG_FILE)
    print("Is first run:", config.is_first_run())
    print("Modules:", config.get("modules"))
