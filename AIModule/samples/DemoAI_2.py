from pyftg import AIInterface 
from pyftg.struct import *
from pyftg.struct import AudioData, GameData, ScreenData
from action_mapping import *
import time 
class DemoAI_2(AIInterface):
    def __init__(self) -> None:
        self.blind_flag = False
        self.width = 96
        self.height = 64 
        self.selected_move = None 
        self.selected_attk = None
        

    def name(self)->str:
        return self.__class__.__name__
    
    def is_blind(self)->str:
        return self.blind_flag
    
    def initialize(self, game_data: GameData, player: bool):
        self.input_key = Key()
        self.cc = CommandCenter()
        self.player = player 

    def input(self):
        return self.input_key
    
    def get_information(self, frame_data:FrameData, is_control:bool, non_delay:FrameData):
        self.frame_data = frame_data 
        self.cc.set_frame_data(frame_data, self.player)

    def get_screen_data(self, screen_data: ScreenData):
        self.screen_data = screen_data

    def get_audio_data(self, audio_data: AudioData):
        pass 

    def processing(self):
        if self.frame_data.empty_flag or self.frame_data.current_frame_number <= 0:
            return
        
        if self.cc.get_skill_flag():
            self.input_key = self.cc.get_skill_key()
            return 
        
        self.input_key.empty()
        self.cc.skill_cancel()
        # print("generate random action")
        distance = self.calculate_distance()
        action = self.self_generate_action()
        self.selected_move = action["move"]
        self.selected_attk = action["attack"]
        if distance <= 50:
            self.selected_attk = generate_random_attack()
            self.cc.command_call(self.selected_attk)
            self.selected_attk = None
        else:
            if self.selected_move == None and self.selected_attk== None:
                time.sleep(0.5)
                return 
            elif self.selected_move == None and self.selected_attk!= None:
                time.sleep(0.5)
                self.cc.command_call(self.selected_attk)
                self.selected_attk = None
            elif self.selected_move != None and self.selected_attk == None:
                time.sleep(0.5)
                self.cc.command_call(self.selected_move)
                self.selected_move = None 
            else:
                time.sleep(0.5)
                self.cc.command_call(self.selected_move)
                self.cc.command_call(self.selected_attk)
                self.selected_move = None 
                self.selected_attk = None

    def calculate_distance(self):
        self.get_information(self.frame_data, is_control=False, non_delay=self.frame_data)
        player_xs = []
        for ch in self.frame_data.character_data:
            player_xs.append(ch.x)
        return abs(player_xs[0] - player_xs[1])
    
    def set_action(self, move, attk):
        self.selected_move = move 
        self.selected_attk = attk

    def self_generate_action(self):
        rand = generate_random_keys(key_length=5)
        action = keys2action(rand)
        return action



    