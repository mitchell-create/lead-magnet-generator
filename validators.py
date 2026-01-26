"""
Validation functions for Slack command inputs.
Validates industry and seniority values against Prospeo's supported options.
"""
from typing import Dict, List, Tuple, Optional

# Valid seniority levels (from PROSPEO_SENIORITY_LEVELS.md)
VALID_SENIORITY_LEVELS = [
    "Founder/Owner",
    "C-Suite",
    "Partner",
    "Vice President",
    "Head",
    "Director",
    "Manager",
    "Senior",
    "Intern",
    "Entry"
]

# Valid industries - NOT USED
# Industry validation is handled by Prospeo API directly
# Users should use dashboard "API JSON" builder to find exact enum values
VALID_INDUSTRIES = []


def validate_seniority_levels(seniority_values: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate seniority levels against Prospeo's supported values.
    
    Args:
        seniority_values: List of seniority values to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if all values are valid
        - error_message: Error message if invalid, None if valid
    """
    if not seniority_values:
        return True, None  # Empty is valid (no seniority filter)
    
    invalid_values = []
    for value in seniority_values:
        # Trim whitespace and check
        value_clean = value.strip()
        if value_clean not in VALID_SENIORITY_LEVELS:
            invalid_values.append(value_clean)
    
    if invalid_values:
        valid_list = ", ".join(VALID_SENIORITY_LEVELS)
        error_msg = (
            f"❌ Invalid seniority level(s): {', '.join(invalid_values)}\n\n"
            f"**Valid seniority levels:**\n"
            f"`{valid_list}`\n\n"
            f"**Example:**\n"
            f"`/lead-magnet ... seniority=Founder/Owner,C-Suite`"
        )
        return False, error_msg
    
    return True, None


# Common industry mistakes: Prospeo has no "General", etc. Map to correct enum for pre-check.
INDUSTRY_QUICK_FIXES = {"general": "General Retail"}


def validate_industries(industry_values: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate industry values. Catches common mistakes (e.g. "General") and suggests
    the exact Prospeo value. See https://prospeo.io/api-docs/enum/industries
    """
    if not industry_values:
        return True, None
    for v in industry_values:
        vnorm = (v or "").strip().lower()
        if not vnorm:
            continue
        suggestion = INDUSTRY_QUICK_FIXES.get(vnorm)
        if suggestion:
            return False, (
                f"❌ Industry \"{v}\" is not a valid Prospeo value.\n\n"
                f"**Use instead:** `{suggestion}`\n\n"
                f"All values: https://prospeo.io/api-docs/enum/industries"
            )
    return True, None


def validate_slack_command(parsed_input: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate all filters in a parsed Slack command input.
    
    Args:
        parsed_input: Parsed input dictionary from parse_natural_language_input()
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if all values are valid
        - error_message: Combined error message if invalid, None if valid
    """
    prospeo_filters = parsed_input.get('prospeo_filters', {})
    
    errors = []
    
    # Validate seniority levels
    if 'person_seniority' in prospeo_filters:
        seniority_values = prospeo_filters['person_seniority']
        if isinstance(seniority_values, list):
            is_valid, error = validate_seniority_levels(seniority_values)
            if not is_valid:
                errors.append(error)
    
    # Validate industries
    if 'company_industry' in prospeo_filters:
        industry_values = prospeo_filters['company_industry']
        if isinstance(industry_values, list):
            is_valid, error = validate_industries(industry_values)
            if not is_valid:
                errors.append(error)
    
    if errors:
        combined_error = "\n\n---\n\n".join(errors)
        return False, combined_error
    
    return True, None
