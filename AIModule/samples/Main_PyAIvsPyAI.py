import logging
import argparse
from pyftg import Gateway
from KickAI import KickAI
from DisplayInfo import DisplayInfo

from DemoAI import DemoAI_2
from multiprocessing import Process


def start_game(port: int):
    gateway = Gateway(port=port)
    character = 'ZEN'
    game_num = 1

    #agent1 = KickAI()
    #agent2 = DisplayInfo()
    agent1 = DemoAI_2()
    agent2 = DemoAI_2()
    gateway.register_ai("KickAI", agent1)

    gateway.register_ai("DisplayInfo", agent2)
    gateway.run_game([character, character], ["KickAI", "DisplayInfo"], game_num)
    # gateway.run_game([character, character], ["DemoAI_1", "DemoAI_2"], game_num)
    gateway.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', default='INFO', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('--port', default=50051, type=int, help='Port used by DareFightingICE')
    args = parser.parse_args()
    logging.basicConfig(level=args.log)
    start_game(args.port)
