#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#
#   ██████╗  █████╗ ███╗   ██╗ ██████╗ ███████╗    ██████╗  █████╗ ██████╗ ███████╗███████╗██████╗ 
#   ██╔══██╗██╔══██╗████╗  ██║██╔════╝ ██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
#   ██████╔╝███████║██╔██╗ ██║██║  ███╗█████╗      ██████╔╝███████║██████╔╝███████╗█████╗  ██████╔╝
#   ██╔══██╗██╔══██║██║╚██╗██║██║   ██║██╔══╝      ██╔═══╝ ██╔══██║██╔══██╗╚════██║██╔══╝  ██╔══██╗
#   ██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗    ██║     ██║  ██║██║  ██║███████║███████╗██║  ██║
#   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
#
#   Range Parser Module - Parses various range input formats
#
#   GitHub  : github.com/Aryan-cloud-arch/LEFT
#   Telegram: @MaiHuAryan
#
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import re  # Regular expressions for pattern matching


# ═══════════════════════════════════════════════════════════════════════════════
#                             RANGE PARSER CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class RangeParser:
    """
    Parses various range input formats into a set of indices.
    
    Supported formats:
    - "1-40"         : Range from 1 to 40 (inclusive)
    - "1-40,50-60"   : Multiple ranges
    - "5,10,15,20"   : Individual numbers
    - "1-40,55,60-70": Mixed ranges and individual numbers
    - "all"          : All items
    - "name:keyword" : Search by name (for exclude)
    - "none"         : Empty set (for exclude)
    """
    
    @staticmethod
    def parse(input_string, max_value, dialogs=None):
        """
        Parse the input string and return a set of indices.
        
        Args:
            input_string: The user input string
            max_value: Maximum allowed value (total number of items)
            dialogs: List of dialogs (needed for name-based search)
        
        Returns:
            tuple: (set of indices, error message or None)
        """
        
        # ─────────────────────────────────────────────────────────────────────
        # Clean the input
        # ─────────────────────────────────────────────────────────────────────
        
        # Remove whitespace and convert to lowercase
        input_string = input_string.strip().lower()
        
        # ─────────────────────────────────────────────────────────────────────
        # Handle special cases
        # ─────────────────────────────────────────────────────────────────────
        
        # Case: Empty input
        if not input_string:
            return set(), "Input cannot be empty"
        
        # Case: "none" - return empty set (used for exclude)
        if input_string == "none":
            return set(), None
        
        # Case: "all" - return all indices
        if input_string == "all":
            return set(range(1, max_value + 1)), None
        
        # Case: Name-based search (format: "name:keyword")
        if input_string.startswith("name:"):
            return RangeParser._parse_by_name(input_string, dialogs)
        
        # ─────────────────────────────────────────────────────────────────────
        # Parse numeric ranges
        # ─────────────────────────────────────────────────────────────────────
        
        return RangeParser._parse_numeric(input_string, max_value)
    
    @staticmethod
    def _parse_numeric(input_string, max_value):
        """
        Parse numeric ranges and individual numbers.
        
        Args:
            input_string: String containing numbers and ranges
            max_value: Maximum allowed value
        
        Returns:
            tuple: (set of indices, error message or None)
        """
        
        # Initialize empty set to store indices
        indices = set()
        
        # Split by comma to get individual parts
        # Example: "1-40,55,60-70" becomes ["1-40", "55", "60-70"]
        parts = input_string.split(",")
        
        for part in parts:
            # Remove whitespace from each part
            part = part.strip()
            
            # Skip empty parts
            if not part:
                continue
            
            # Check if it's a range (contains hyphen)
            if "-" in part:
                # ─────────────────────────────────────────────────────────────
                # Parse range (e.g., "1-40")
                # ─────────────────────────────────────────────────────────────
                
                # Split by hyphen
                range_parts = part.split("-")
                
                # Validate: should have exactly 2 parts
                if len(range_parts) != 2:
                    return set(), f"Invalid range format: '{part}'"
                
                try:
                    # Convert to integers
                    start = int(range_parts[0].strip())
                    end = int(range_parts[1].strip())
                    
                    # Validate range values
                    if start < 1:
                        return set(), f"Range start must be at least 1: '{part}'"
                    
                    if end > max_value:
                        return set(), f"Range end ({end}) exceeds maximum ({max_value})"
                    
                    if start > end:
                        return set(), f"Range start ({start}) cannot be greater than end ({end})"
                    
                    # Add all numbers in range to the set
                    for i in range(start, end + 1):
                        indices.add(i)
                        
                except ValueError:
                    return set(), f"Invalid numbers in range: '{part}'"
            
            else:
                # ─────────────────────────────────────────────────────────────
                # Parse individual number
                # ─────────────────────────────────────────────────────────────
                
                try:
                    num = int(part)
                    
                    # Validate number
                    if num < 1:
                        return set(), f"Number must be at least 1: {num}"
                    
                    if num > max_value:
                        return set(), f"Number ({num}) exceeds maximum ({max_value})"
                    
                    # Add to set
                    indices.add(num)
                    
                except ValueError:
                    return set(), f"Invalid number: '{part}'"
        
        # ─────────────────────────────────────────────────────────────────────
        # Final validation
        # ─────────────────────────────────────────────────────────────────────
        
        if not indices:
            return set(), "No valid numbers found in input"
        
        return indices, None
    
    @staticmethod
    def _parse_by_name(input_string, dialogs):
        """
        Parse name-based search (e.g., "name:family").
        Returns indices of dialogs containing the keyword in their name.
        
        Args:
            input_string: String in format "name:keyword"
            dialogs: List of dialog objects
        
        Returns:
            tuple: (set of indices, error message or None)
        """
        
        # Check if dialogs list is provided
        if dialogs is None:
            return set(), "Dialogs list required for name-based search"
        
        # Extract keyword (everything after "name:")
        keyword = input_string[5:].strip().lower()  # Remove "name:" prefix
        
        # Check if keyword is empty
        if not keyword:
            return set(), "Keyword cannot be empty for name search"
        
        # Find all dialogs containing the keyword
        indices = set()
        
        for i, dialog in enumerate(dialogs, 1):  # 1-indexed
            # Get dialog title and convert to lowercase for comparison
            title = dialog.get('title', '').lower()
            
            # Check if keyword is in the title
            if keyword in title:
                indices.add(i)
        
        # Return results
        if not indices:
            return set(), f"No groups/channels found containing '{keyword}'"
        
        return indices, None
    
    @staticmethod
    def validate_input(input_string):
        """
        Quick validation of input format (without parsing).
        
        Args:
            input_string: The input to validate
        
        Returns:
            bool: True if format looks valid, False otherwise
        """
        
        # Clean input
        input_string = input_string.strip().lower()
        
        # Special keywords are always valid
        if input_string in ["all", "none"]:
            return True
        
        # Name search format
        if input_string.startswith("name:"):
            return len(input_string) > 5  # Must have keyword after "name:"
        
        # Check for valid characters (numbers, hyphens, commas, spaces)
        pattern = r'^[\d\s,\-]+$'
        return bool(re.match(pattern, input_string))
    
    @staticmethod
    def get_description(indices, max_display=5):
        """
        Get a human-readable description of the selected indices.
        
        Args:
            indices: Set of selected indices
            max_display: Maximum number of indices to display individually
        
        Returns:
            str: Description like "1-40 (40 items)" or "1, 5, 10, 15 (4 items)"
        """
        
        if not indices:
            return "None selected"
        
        # Sort indices for better display
        sorted_indices = sorted(indices)
        count = len(sorted_indices)
        
        # If small number of items, show them all
        if count <= max_display:
            return f"{', '.join(map(str, sorted_indices))} ({count} items)"
        
        # Try to find consecutive ranges for compact display
        ranges = RangeParser._find_ranges(sorted_indices)
        
        # Format ranges
        range_strs = []
        for start, end in ranges:
            if start == end:
                range_strs.append(str(start))
            else:
                range_strs.append(f"{start}-{end}")
        
        # Limit displayed ranges
        if len(range_strs) > 3:
            display = ", ".join(range_strs[:3]) + f", ... ({count} items)"
        else:
            display = ", ".join(range_strs) + f" ({count} items)"
        
        return display
    
    @staticmethod
    def _find_ranges(sorted_indices):
        """
        Find consecutive ranges in a sorted list of indices.
        
        Args:
            sorted_indices: Sorted list of indices
        
        Returns:
            list: List of (start, end) tuples representing ranges
        """
        
        if not sorted_indices:
            return []
        
        ranges = []
        start = sorted_indices[0]
        end = sorted_indices[0]
        
        for i in range(1, len(sorted_indices)):
            # If current number is consecutive
            if sorted_indices[i] == end + 1:
                end = sorted_indices[i]
            else:
                # Save current range and start new one
                ranges.append((start, end))
                start = sorted_indices[i]
                end = sorted_indices[i]
        
        # Don't forget the last range
        ranges.append((start, end))
        
        return ranges


# ═══════════════════════════════════════════════════════════════════════════════
#                              TEST (if run directly)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Test cases
    test_cases = [
        "1-40",
        "1-40,50-60",
        "5,10,15,20",
        "1-40,55,60-70",
        "all",
        "none",
        "1-10, 15, 20-25",  # With spaces
    ]
    
    print("Testing RangeParser:")
    print("=" * 50)
    
    for test in test_cases:
        indices, error = RangeParser.parse(test, 100)
        if error:
            print(f"Input: '{test}' -> Error: {error}")
        else:
            desc = RangeParser.get_description(indices)
            print(f"Input: '{test}' -> {desc}")
