#!/usr/bin/env python3
"""
Internet Connectivity Checker
Adapted from Setbian's approach
"""

import urllib.request
import urllib.error


def check_internet(timeout=5):
    """
    Check if internet is available
    
    Args:
        timeout: Connection timeout in seconds
        
    Returns:
        bool: True if internet is available, False otherwise
    """
    test_urls = [
        'http://www.google.com',
        'http://www.cloudflare.com',
        'http://1.1.1.1'
    ]
    
    for url in test_urls:
        try:
            urllib.request.urlopen(url, timeout=timeout)
            return True
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
            continue
    
    return False


def check_internet_with_ui(parent_window=None):
    """
    Check internet with UI feedback
    
    Args:
        parent_window: tkinter parent window for dialog
        
    Returns:
        bool: True if internet available
    """
    if check_internet():
        return True
    
    if parent_window:
        import tkinter as tk
        from tkinter import messagebox
        messagebox.showwarning(
            "No Internet Connection",
            "Internet connection is required for some Zentora features.\n"
            "Please check your connection.\n\n"
            "You can still use installed modules offline.",
            parent=parent_window
        )
    
    return False


if __name__ == "__main__":
    # Test internet connectivity
    if check_internet():
        print("✓ Internet connection is available")
    else:
        print("✗ No internet connection")
