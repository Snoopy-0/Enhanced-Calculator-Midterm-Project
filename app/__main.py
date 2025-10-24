
import sys
from .calculator import Calculator
from .calculator_config import load_config
from .logger import get_logger
from .commands import CommandFactory
from colorama import init as colorama_init, Fore, Style

def main():
    colorama_init()
    cfg = load_config()
    log = get_logger(cfg)
    calc = Calculator(cfg, log)
    cmd_factory = CommandFactory(calc)
    print(Fore.CYAN + "Advanced Calculator REPL. Type 'help' for commands. 'exit' to quit." + Style.RESET_ALL)

    while True:
        try:
            raw = input(Fore.GREEN + "calc> " + Style.RESET_ALL).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()

        if cmd in ("exit", "quit"):
            print(Fore.CYAN + "Goodbye!" + Style.RESET_ALL)
            break
        elif cmd in ("help",):
            print(calc.dynamic_help())
            continue
        elif cmd == "history":
            for i, c in enumerate(calc.history_list(), 1):
                print(f"{i:3d}. {c.operation}({c.a}, {c.b}) = {c.result} @ {c.timestamp}")
            continue
        elif cmd == "clear":
            calc.clear_history()
            print(Fore.YELLOW + "History cleared." + Style.RESET_ALL)
            continue
        elif cmd == "undo":
            if calc.undo():
                print(Fore.YELLOW + "Undone last operation." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Nothing to undo." + Style.RESET_ALL)
            continue
        elif cmd == "redo":
            if calc.redo():
                print(Fore.YELLOW + "Redid last operation." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Nothing to redo." + Style.RESET_ALL)
            continue
        elif cmd == "save":
            path = calc.save_history()
            print(Fore.CYAN + f"History saved to {path}" + Style.RESET_ALL)
            continue
        elif cmd == "load":
            cnt = calc.load_history()
            print(Fore.CYAN + f"Loaded {cnt} history entries." + Style.RESET_ALL)
            continue
        else:
            # operation commands expecting two numbers
            if cmd in calc.available_operations():
                try:
                    a, b = parse_two_numbers(parts[1:], cfg)
                    res = calc.calculate(cmd, a, b)
                    print(Fore.MAGENTA + f"Result: {res}" + Style.RESET_ALL)
                except Exception as ex:
                    print(Fore.RED + f"Error: {ex}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"Unknown command '{cmd}'. Type 'help'." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
