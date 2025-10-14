#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jeux  de Nim (variante simple et de Marienbad)
"""

from typing import Tuple
from utils import ask_choice, ask_int

# ----------------------- RULES -----------------------

INITIAL_MATCHES: int = 21
MIN_TAKE: int = 1
MAX_TAKE: int = 4


def is_game_over(remaining: int) -> bool:
    """Game ends when there's only one match left

    Args (int): remaining number of matches left

    Returns:
        bool

    """

    return remaining <= 1


def apply_move(remaining: int, taken: int) -> int:
    """Subtract taken matches

    Args:
        remaining (int): remaining number of matches left before move
        taken (int): taken number of matches

    Returns:
        int: remaining number of matches left after move
    """
    if taken < MIN_TAKE or taken > MAX_TAKE:
        raise ValueError(
            f"Prise invalide : {taken}. Le nombre d'allumette à prendre doit être compris entre {MIN_TAKE} et {MAX_TAKE})."
        )
    if taken > remaining:
        raise ValueError(
            f"Prise invalide: {taken}. Il ne reste que {remaining} allumettes."
        )
    return remaining - taken


# ----------------------- INTERACTIONS -----------------------


def ask_player_name(label: str) -> str:
    """Prompt for player pseudo

    Args:
        label (str): placeholder player label

    Returns:
        str: player pseudo
    """
    while True:
        pseudo: str = input(f"Entrez le pseudo du {label} : ").strip()
        if pseudo:
            return pseudo.title()
        print("Le pseudo ne peut pas être vide.")


def choose_starter(p1: str, p2: str) -> str:
    """Ask who starts among the two names.

    Args:
        p1 (str): first player
        p2 (str): second player

    Returns:
        str: starter name
    """
    starter: str = ask_choice(f"Qui commence {p1} ou {p2} ? : ", [p1, p2])
    # return original-cased name
    return p1 if starter == p1.lower() else p2


# ----------------------- GAME LOOP -----------------------


def human_turn(name: str, remaining: int) -> int:
    """Ask human for a valid take (1 to 4 & not exceeding remaining)

    Args:
        name (str): player name
        remaining (int): remaining number of matches left

    Returns:
        int: player take
    """
    prompt: str = (
        f"{name}, combien d'allumettes prends-tu entre {MIN_TAKE} et {MAX_TAKE} ? Il en reste : {remaining}) : "
    )
    while True:
        take: int = ask_int(prompt, min_value=MIN_TAKE, max_value=MAX_TAKE)
        if take <= remaining:
            return take
        print(
            f"Tu ne peux pas prendre {take} allumettes, il n'en reste que : {remaining})."
        )


def run_pvp_game(p1: str, p2: str, starter: str) -> Tuple[str, str]:
    """
    Run a PVP match &  returns winner and loser
    (loser is the one who takes the last match)

    Args:
        p1 (str) : first player
        p2 (str) : second player
        starter (str) : starter name

    Returns:
        Tuple[str, str]: loser
    """
    remaining: int = INITIAL_MATCHES
    current_player: str = starter
    other_player: str = p2 if current_player == p1 else p1

    print(
        f"\nIl y a {remaining} allumettes. {current_player} commence. (Rappel: celui qui prend la dernière allumette perd)"
    )

    while True:
        # current human player plays
        take: int = human_turn(current_player, remaining)
        remaining = apply_move(remaining, take)
        print(
            f"{current_player} prend {take} allumette{"s" if take >1 else "" }. Allumettes restantes : {remaining}"
        )
        if is_game_over(remaining):
            # current player took the last match-> current_player loses, other_player wins
            print(f"\nIl ne reste plus qu'une allumette. {current_player} a perdu 😢")
            print(f"🏆 {other_player} gagne !")
            return other_player, current_player

        # swap players
        current_player, other_player = other_player, current_player


# ----------------------- Entry point -----------------------


def main() -> None:
    print("=== Jeu de Nim (21 allumettes) ===")

    p1: str = ask_player_name("joueur 1")
    p2: str = ask_player_name("joueur 2")
    starter: str = choose_starter(p1, p2)
    run_pvp_game(p1, p2, starter)


if __name__ == "__main__":
    main()
