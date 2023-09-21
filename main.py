#!/usr/bin/env python3

"""
Main
Runs trade agent with passed parameters
"""
from dotenv import load_dotenv

from tradeagent import TradeAgent

class textformat:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def main():
    ta = TradeAgent()
    ta.run()

if __name__ == "__main__":
    load_dotenv()

    print(
        f"{textformat.GREEN}%%-------------------------------------------%%{textformat.END}",
        f"\n{textformat.GREEN}%%----------%% TRADER AGENT v0.1 %%----------%%{textformat.END}",
        f"\n{textformat.GREEN}%%-------------------------------------------%%{textformat.END}",
    )

    main()