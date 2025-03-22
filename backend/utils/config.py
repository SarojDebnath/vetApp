import json
import os

class ConfigManager:
    def __init__(self, config_file="vet_app_config.json"):
        """Initialize the config manager"""
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default if it doesn't exist"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # If the file is corrupted, create default config
                return self.create_default_config()
        else:
            # If the file doesn't exist, create default config
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        config = {
            "save_folder": os.path.join(os.getcwd(), "storage")
        }
        
        # Create save folder if it doesn't exist
        if not os.path.exists(config["save_folder"]):
            os.makedirs(config["save_folder"])
        
        # Save default config
        self.config = config
        self.save_config()
        
        return config
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f)
    
    def update_config(self, new_config):
        """Update configuration"""
        self.config.update(new_config)
    
    def get_db_path(self):
        """Get database path from configuration"""
        return os.path.join(self.config.get("save_folder", os.getcwd()), "vet_app.db") 