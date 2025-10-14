#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jeux de Nim (variante simple et de Marienbad)
"""

from typing import Tuple, Optional
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

    return remaining <= 0


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


def resolve_after_move(
    current: str, other: str, remaining: int
) -> Optional[Tuple[str, str]]:
    """End of turn resolver
    - current took the last one → current loses
    - other is forced to take the last one → other loses now
    - else → game continues

    Args:
        current (str): current player
        other (str): other player
        remaining (int): remaining number of matches left

    Returns:
        Optional[Tuple[str, str]]:
    """
    if remaining <= 0:
        print(f"\n{current} a pris la dernière allumette. {current} a perdu 😢")
        print(f"🏆 {other} gagne WOOT GG !")
        return other, current
    if remaining == 1:
        print(
            f"\nIl ne reste qu'une allumette. {other} est obligé de la prendre → {other} a perdu 😢"
        )
        print(f"🏆 {current} gagne WOOT GG !")
        return current, other
    return None


def ask_replay() -> bool:
    """Ask the user if they want to play another game

    Returns:
        bool
    """
    answer: str = ask_choice("Rejouer ? (oui/non) : ", ["oui", "non"])
    return answer == "oui"


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


def choose_game_mode() -> str:
    """Ask for game mode: 'PVP' or 'PVE'

    Returns:
        str: game mode
    """
    mode: str = ask_choice(
        "Mode : PVP = humain vs humain, PVE = humain vs machine ? ", ["PVP", "PVE"]
    )
    print(f"Game mode: {mode.upper()}")
    return mode


def choose_starter(p1: str, p2: str) -> str:
    """Ask who starts among the two names.

    Args:
        p1 (str): first player
        p2 (str): second player

    Returns:
        str: starter name
    """
    starter: str = ask_choice(f"Qui commence {p1} ou {p2} ? : ", [p1, p2])

    return starter


# ----------------------- PVE -----------------------


def bot_take_when_human_starts(last_human_take: int, remaining: int) -> int:
    """
    Optimal strategy when human starts

    Goal:
        Always make sure the total number of matches taken per round = 5.
        (human_take + bot_take = 5)
        This keeps the pile at 16, 11, 6, 1... and forces the human to lose

    Example:
        If human takes 3, bot takes 2 → together they remove 5.

    Args:
        last_human_take (int) : number of matches human took
        remaining (int) : matches still on the table before bot plays

    Returns:
        int: number of matches the bot should take to keep control of the game
    """
    # Ideal take so that human + bot = 5
    target: int = 5 - last_human_take

    # Make sure bot doesn't take more than allowed or remaining
    return max(MIN_TAKE, min(target, min(MAX_TAKE, remaining)))


def bot_first_move_when_bot_starts(remaining: int) -> int:
    """
    Strategy when bot starts :

        - With 21 matches, first player is in losing position
          if opponent plays perfectly because 21 is not a multiple of 5
        - Bot takes 1 match hoping player will make a mistake later

    Args:
        remaining (int): number of matches left

    Returns:
        int: number of matches bot takes for its first move
    """
    return min(1, remaining)


def bot_play(
    remaining: int, human_started: bool, last_human_take: Optional[int]
) -> int:
    """
    Decide bot take
    - If human started: use "5 - k" strategy based on last_human_take
    - If bot started: first move is 1, then use "5 - k" strategy after human has played once

    Args:
        remaining (int): remaining number of matches left
        human_started (bool): human play first
        last_human_take (Optional[int]): last human take

    Returns:
        int:
    """
    # If 2 to 5 remain, take (remaining - 1) to leave 1 → opponent loses immediately
    if 2 <= remaining <= 5:
        return remaining - 1

    if human_started:
        # Requires a human move first to know k
        if last_human_take is None:
            # Should not happen if called after human turn
            return min(1, remaining)
        return bot_take_when_human_starts(last_human_take, remaining)
    else:
        # Bot starts : on first move we have no human take yet
        if last_human_take is None:
            return bot_first_move_when_bot_starts(remaining)
        # After human played once, resume "5-k" strategy
        return bot_take_when_human_starts(last_human_take, remaining)


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

        outcome = resolve_after_move(current_player, other_player, remaining)
        if outcome:
            return outcome
        # swap players
        current_player, other_player = other_player, current_player


def run_pve_game(human: str, bot: str, human_starts: bool) -> Tuple[str, str]:
    """
    Run a PVE match & returns winner and loser
    """
    remaining: int = INITIAL_MATCHES
    current_player: str = human if human_starts else bot
    other_player: str = bot if current_player == human else human
    last_human_take: Optional[int] = None  # Track last human move for "5 - k" strategy

    print(
        f"\nIl y a {remaining} allumettes. {current_player} commence. (Rappel: celui qui prend la DERNIÈRE perd)"
    )

    while True:
        if current_player == human:
            take: int = human_turn(human, remaining)
            last_human_take = take
        else:
            take = bot_play(
                remaining, human_started=human_starts, last_human_take=last_human_take
            )

            print(f"{bot} prend {take}.")

        remaining = apply_move(remaining, take)
        print(f"Allumettes restantes: {remaining}")

        # End of turn resolution
        outcome = resolve_after_move(current_player, other_player, remaining)
        if outcome:
            return outcome

        # swap roles
        current_player, other_player = other_player, current_player


# ----------------------- Run -----------------------


def main() -> None:
    print("=== Jeu de Nim (21 allumettes) ===")
    while True:  # Replay loop
        mode: str = choose_game_mode()

        if mode.upper() == "PVP":
            p1: str = ask_player_name("joueur 1")
            p2: str = ask_player_name("joueur 2")
            starter: str = choose_starter(p1, p2)
            run_pvp_game(p1, p2, starter)
        else:
            human: str = ask_player_name("joueur").title()
            bot: str = "Machine"
            who_starts: str = ask_choice(
                f"Qui commence {human} ou {bot} ? ", [human, bot]
            )
            human_starts: bool = who_starts.title() == human
            run_pve_game(human, bot, human_starts)

        # Ask for replay at the end of the game
        if not ask_replay():
            print("Bye !")
            break


if __name__ == "__main__":
    main()
