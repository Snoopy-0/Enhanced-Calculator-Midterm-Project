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

        handled, msg = cmd_factory.execute(cmd, parts[1:])
        if handled:
            if msg:
                if msg.startswith("Error:"):
                    print(Fore.RED + msg + Style.RESET_ALL)
                elif msg.startswith(("History", "Loaded", "Undone", "Redid", "History cleared.")):
                    print(Fore.YELLOW + msg + Style.RESET_ALL)
                else:
                    print(Fore.MAGENTA + msg + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + msg + Style.RESET_ALL)

if __name__ == "__main__":
    main()
