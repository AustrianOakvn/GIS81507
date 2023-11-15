import time 
import numpy as np 
#import torch 
from pyftg import AIInterface
from pyftg.struct import *

import logging

class SoundAgent(AIInterface):
    def __init__(self, **kwargs):
        self.actor = kwargs.get('actor')
        self.critic = kwargs.get('critic')
        self.device = kwargs.get('device')
        self.logger = kwargs.get('logger')
        self.collect_data_helper = kwargs.get('collect_data_helper')
        self.trajectory_data = None 

        self.actions = "AIR_A", "AIR_B", "AIR_D_DB_BA", "AIR_D_DB_BB", "AIR_D_DF_FA", "AIR_D_DF_FB", "AIR_DA", "AIR_DB", \
                       "AIR_F_D_DFA", "AIR_F_D_DFB", "AIR_FA", "AIR_FB", "AIR_UA", "AIR_UB", "BACK_JUMP", "BACK_STEP", \
                       "CROUCH_A", "CROUCH_B", "CROUCH_FA", "CROUCH_FB", "CROUCH_GUARD", "DASH", "FOR_JUMP", "FORWARD_WALK", \
                       "JUMP", "NEUTRAL", "STAND_A", "STAND_B", "STAND_D_DB_BA", "STAND_D_DB_BB", "STAND_D_DF_FA", \
                       "STAND_D_DF_FB", "STAND_D_DF_FC", "STAND_F_D_DFA", "STAND_F_D_DFB", "STAND_FA", "STAND_FB", \
                       "STAND_GUARD", "THROW_A", "THROW_B" 
        
        self.just_inited = None 
        self.pre_frame_data:FrameData = None 
        self.nonDelay: FrameData = None 

    def name(self)-> str:
        return self.__class__.__name__
    
    def initialize(self, gameData, player):
        self.inputKey = Key()
        self.frameData = FrameData()
        self.cc = CommandCenter()
        self.player = player 
        self.gameData = gameData 
        self.isGameJustStarted = True 
        return 0
    
    def get_information(self, frame_data:FrameData, is_control:bool, non_delay:FrameData):
        self.frameData = frame_data 
        self.cc.set_frame_data(self.frameData, self.player)
        self.pre_frame_data = self.nonDelay if self.nonDelay is not None else non_delay
        self.nonDelay = non_delay 
        self.isControl = is_control 
        self.currentFrameNum = self.frameData.current_frame_number

    def round_end(self, round_result:RoundResult):
        self.logger.info(round_result.remaining_hps[0])
        self.logger.info(round_result.remaining_hps[1])
        self.logger.info(round_result.elapsed_frame)
        self.just_inited = True 
    

    def processing(self):
        start_time = time.time()*1000
        if self.frameData.empty_flag or self.frameData.current_frame_number<=0:
            self.isGameJustStarted = True 
            return 
        
        self.inputKey.empty()
        self.cc.skill_cancel()
        action = "AIR_A"
        # perform action
        self.cc.command_call(self.actions[action])



