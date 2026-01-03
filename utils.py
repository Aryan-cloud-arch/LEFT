#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#
#   ██╗   ██╗████████╗██╗██╗     ███████╗
#   ██║   ██║╚══██╔══╝██║██║     ██╔════╝
#   ██║   ██║   ██║   ██║██║     ███████╗
#   ██║   ██║   ██║   ██║██║     ╚════██║
#   ╚██████╔╝   ██║   ██║███████╗███████║
#    ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝
#
#   Utility Functions for Telegram Auto Leave Tool
#
#   GitHub  : github.com/Aryan-cloud-arch/LEFT
#   Telegram: @MaiHuAryan
#
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import os                      # For file and directory operations
from datetime import datetime  # For timestamps in logs
from pathlib import Path       # For path handling


# ═══════════════════════════════════════════════════════════════════════════════
#                              FILE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def ensure_directory(directory_path):
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory_path: Path to the directory
    
    Returns:
        bool: True if directory exists or was created, False on error
    """
    try:
        # Create directory and all parent directories if they don't exist
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False


def write_log(log_file, entries, mode='w'):
    """
    Write entries to a log file.
    
    Args:
        log_file: Path to the log file
        entries: List of entries to write
        mode: File mode ('w' for write, 'a' for append)
    
    Returns:
        bool: True if successful, False on error
    """
    try:
        # Ensure the directory exists
        ensure_directory(os.path.dirname(log_file))
        
        # Write to file
        with open(log_file, mode, encoding='utf-8') as f:
            # Write header with timestamp
            f.write("=" * 80 + "\n")
            f.write(f"  Telegram Auto Leave Tool - Log\n")
            f.write(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"  GitHub: github.com/Aryan-cloud-arch/LEFT\n")
            f.write(f"  Telegram: @MaiHuAryan\n")
            f.write("=" * 80 + "\n\n")
            
            # Write entries
            for entry in entries:
                f.write(f"{entry}\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        return True
    except Exception as e:
        print(f"Error writing to log file: {e}")
        return False


def append_to_log(log_file, entry):
    """
    Append a single entry to the log file.
    
    Args:
        log_file: Path to the log file
        entry: Entry to append
    
    Returns:
        bool: True if successful, False on error
    """
    try:
        ensure_directory(os.path.dirname(log_file))
        
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {entry}\n")
        
        return True
    except Exception as e:
        print(f"Error appending to log: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#                           CONFIG VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_config():
    """
    Validate the configuration file.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        from config import API_ID, API_HASH, PHONE_NUMBER
        
        # Check API_ID
        if not API_ID or API_ID == 12345678:
            return False, "API_ID is not set. Please update config.py"
        
        # Check API_HASH
        if not API_HASH or API_HASH == "your_api_hash_here":
            return False, "API_HASH is not set. Please update config.py"
        
        # Check PHONE_NUMBER
        if not PHONE_NUMBER or "XXXXXXXXXX" in PHONE_NUMBER:
            return False, "PHONE_NUMBER is not set. Please update config.py"
        
        # Check phone number format
        if not PHONE_NUMBER.startswith("+"):
            return False, "PHONE_NUMBER must start with + (country code)"
        
        return True, None
        
    except ImportError:
        return False, "config.py not found. Please create it from config.py.example"
    except Exception as e:
        return False, f"Error validating config: {e}"


# ═══════════════════════════════════════════════════════════════════════════════
#                           DATA PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

def categorize_dialogs(to_leave_indices, to_keep_indices, all_dialogs):
    """
    Categorize dialogs into 'to leave' and 'to keep' lists.
    
    Args:
        to_leave_indices: Set of indices to leave
        to_keep_indices: Set of indices to keep
        all_dialogs: List of all dialogs
    
    Returns:
        tuple: (to_leave_list, to_keep_list)
    """
    to_leave = []
    to_keep = []
    
    for i, dialog in enumerate(all_dialogs, 1):  # 1-indexed
        # Create a copy with original index
        dialog_copy = dialog.copy()
        dialog_copy['original_index'] = i
        
        if i in to_leave_indices and i not in to_keep_indices:
            to_leave.append(dialog_copy)
        else:
            to_keep.append(dialog_copy)
    
    return to_leave, to_keep


def format_time(seconds):
    """
    Format seconds into a human-readable string.
    
    Args:
        seconds: Number of seconds
    
    Returns:
        str: Formatted time string (e.g., "2h 30m 15s")
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"


def truncate_string(text, max_length, suffix="..."):
    """
    Truncate a string to a maximum length, adding suffix if truncated.
    
    Args:
        text: The string to truncate
        max_length: Maximum allowed length
        suffix: Suffix to add if truncated (default: "...")
    
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# ═══════════════════════════════════════════════════════════════════════════════
#                              SAFETY CHECKS
# ═══════════════════════════════════════════════════════════════════════════════

def estimate_time(num_groups, delay_per_group=2, batch_size=10, batch_delay=10):
    """
    Estimate the time required to leave all groups.
    
    Args:
        num_groups: Number of groups to leave
        delay_per_group: Delay in seconds between each leave
        batch_size: Number of leaves before extra pause
        batch_delay: Extra delay after each batch
    
    Returns:
        tuple: (total_seconds, formatted_string)
    """
    # Calculate base time
    base_time = num_groups * delay_per_group
    
    # Calculate batch pauses
    num_batches = num_groups // batch_size
    batch_time = num_batches * batch_delay
    
    # Total time
    total_seconds = base_time + batch_time
    
    return total_seconds, format_time(total_seconds)


def is_safe_to_continue(num_groups, max_safe=500):
    """
    Check if it's safe to proceed with the operation.
    
    Args:
        num_groups: Number of groups to leave
        max_safe: Maximum number considered safe
    
    Returns:
        tuple: (is_safe, warning_message)
    """
    if num_groups > max_safe:
        return False, f"Leaving {num_groups} groups at once is risky. Consider doing it in smaller batches."
    return True, None


# ═══════════════════════════════════════════════════════════════════════════════
#                              TEST (if run directly)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Test functions
    print("Testing utils.py")
    print("=" * 50)
    
    # Test time formatting
    print(f"30 seconds: {format_time(30)}")
    print(f"90 seconds: {format_time(90)}")
    print(f"3700 seconds: {format_time(3700)}")
    
    # Test time estimation
    total, formatted = estimate_time(100)
    print(f"\nEstimated time for 100 groups: {formatted}")
    
    # Test truncation
    long_text = "This is a very long group name that needs to be truncated"
    print(f"\nTruncated: {truncate_string(long_text, 30)}")
