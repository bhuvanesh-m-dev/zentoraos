#!/usr/bin/env python3
"""
Logging System for Zentora
Handles application logging to file and console
"""

import os
import sys
from datetime import datetime


class Logger:
    """Simple logging system"""
    
    LOG_DIR = os.path.expanduser("~/.config/zentora/logs")
    LOG_FILE = os.path.join(LOG_DIR, "zentora.log")
    
    LEVEL_DEBUG = 0
    LEVEL_INFO = 1
    LEVEL_WARNING = 2
    LEVEL_ERROR = 3
    LEVEL_CRITICAL = 4
    
    LEVEL_NAMES = {
        LEVEL_DEBUG: "DEBUG",
        LEVEL_INFO: "INFO",
        LEVEL_WARNING: "WARNING",
        LEVEL_ERROR: "ERROR",
        LEVEL_CRITICAL: "CRITICAL"
    }
    
    def __init__(self, name="Zentora", level=LEVEL_INFO):
        """
        Initialize logger
        
        Args:
            name: Logger name
            level: Minimum log level
        """
        self.name = name
        self.level = level
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """Create log directory if it doesn't exist"""
        os.makedirs(self.LOG_DIR, exist_ok=True)
    
    def _format_message(self, level, message):
        """Format log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level_name = self.LEVEL_NAMES.get(level, "UNKNOWN")
        return f"[{timestamp}] [{level_name}] [{self.name}] {message}"
    
    def _write_log(self, level, message):
        """Write log to file and console"""
        if level < self.level:
            return
        
        formatted = self._format_message(level, message)
        
        # Write to file
        try:
            with open(self.LOG_FILE, 'a') as f:
                f.write(formatted + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}", file=sys.stderr)
        
        # Write to console
        if level >= self.LEVEL_ERROR:
            print(formatted, file=sys.stderr)
        else:
            print(formatted)
    
    def debug(self, message):
        """Log debug message"""
        self._write_log(self.LEVEL_DEBUG, message)
    
    def info(self, message):
        """Log info message"""
        self._write_log(self.LEVEL_INFO, message)
    
    def warning(self, message):
        """Log warning message"""
        self._write_log(self.LEVEL_WARNING, message)
    
    def error(self, message):
        """Log error message"""
        self._write_log(self.LEVEL_ERROR, message)
    
    def critical(self, message):
        """Log critical message"""
        self._write_log(self.LEVEL_CRITICAL, message)
    
    def exception(self, message):
        """Log exception with traceback"""
        import traceback
        tb = traceback.format_exc()
        self.error(f"{message}\n{tb}")
    
    @classmethod
    def get_log_contents(cls, lines=100):
        """
        Get recent log contents
        
        Args:
            lines: Number of lines to retrieve
            
        Returns:
            str: Log contents
        """
        try:
            with open(cls.LOG_FILE, 'r') as f:
                all_lines = f.readlines()
                return ''.join(all_lines[-lines:])
        except:
            return ""
    
    @classmethod
    def clear_logs(cls):
        """Clear log file"""
        try:
            with open(cls.LOG_FILE, 'w') as f:
                f.write("")
            return True
        except:
            return False


# Global logger instance
_global_logger = None

def get_logger(name="Zentora"):
    """Get global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger(name)
    return _global_logger


if __name__ == "__main__":
    # Test logger
    logger = get_logger("Test")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
