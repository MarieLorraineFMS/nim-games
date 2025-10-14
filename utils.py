#!/usr/bin/env python
# -*- coding: utf-8 -*-
# utils.py
"""
Utility functions
"""
from typing import Optional, Iterable, List, Dict


def is_none_or_empty(value: Optional[str]) -> bool:
    """
     Check if a string is None or empty

    Args:
         value (Optional[str]): The input string to check

     Returns:
         bool: True if the string is None or empty, False otherwise
    """
    return value is None or value.strip() == ""


def safe_int(value: str) -> Optional[int]:
    """
    Convert string to integer

    Args:
        value (str): String to convert

    Returns:
        Optional[int]: Int value if conversion succeeds, None otherwise
    """
    try:
        result: int = int(value)
        return result
    except ValueError:
        return None


def ask_int(
    prompt: str, min_value: int = 1, max_value: Optional[int] = None
) -> int | None:
    """
    Ask user to enter an int within an optional range

    Args:
        prompt (str): message to be displayed
        min_value (int): minimum value
        max_value (Optional[int]): maximum value

    Returns:
        int: checked user value
    """
    while True:
        raw_text: str = input(prompt)
        if is_none_or_empty(raw_text):
            print("La saisie ne peut pas être vide.")
            continue

        raw_text_stripped: str = raw_text.strip()
        parsed: Optional[int] = safe_int(raw_text_stripped)

        if (
            parsed is not None
            and parsed >= min_value
            and (max_value is None or parsed <= max_value)
        ):
            return parsed

        if max_value is None:
            print(f"Veuillez entrer un nombre entier ≥ {min_value}.")
        else:
            print(f"Veuillez entrer un nombre entier entre {min_value} et {max_value}.")


def ask_choice(prompt: str, choices: Iterable[str]) -> str | None:
    """
    Ask user to choose an option

    Args:
        prompt (str): message to be displayed
        choices (Iterable[str]): allowed choices

    Returns:
        str: lowered value
    """
    allowed_map: Dict[str, str] = {}
    for choice in choices:
        allowed_map[choice.lower()] = choice

    allowed_lower_values: List[str] = list(allowed_map.keys())

    while True:
        user_input: str = input(prompt)
        if is_none_or_empty(user_input):
            print("Veuillez renseigner le champ.")
            continue

        normalized: str = user_input.strip().lower()
        if normalized in allowed_map:
            return normalized

        print(f"Veuillez choisir une valeur : {', '.join(allowed_lower_values)}.")
