import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random

MAX_EPISODE_LEN = 5000
JOINTS=[0,1,5,6]
MAX_TORQUE=500
FORCE_ACTION={
#    0: 0,
#    1: 0,
#    2: 0,
#    3: 0,
}

class NFEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    _max_episode_steps=MAX_EPISODE_LEN

    def __init__(self,show_gui=False):
        self.step_counter = 0
        if show_gui:
            p.connect(p.GUI)
        else:
            p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.action_space = spaces.Box(np.array([-1]*4), np.array([1]*4))
        self.prev_pos=None

    def reset(self):
        self.step_counter = 0
        p.resetSimulation()
        p.setGravity(0,0,-10)
        self.plane_id = p.loadURDF("plane.urdf")
        #self.wall1_id = p.loadURDF("plane.urdf",[-0.7,0,0],p.getQuaternionFromEuler([0,math.pi/2,0]))
        #self.wall2_id = p.loadURDF("plane.urdf",[0.7,0,0],p.getQuaternionFromEuler([0,-math.pi/2,0]))
        cubeStartPos = [0,0,2]
        cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
        try:
            self.bot_id = p.loadURDF("/Users/dj/stuff/bot/urdf/bot8.urdf", cubeStartPos, cubeStartOrientation)
        except:
            self.bot_id = p.loadURDF("/content/drive/My Drive/bot/bot8.urdf", cubeStartPos, cubeStartOrientation)

        maxForce = 0
        mode = p.VELOCITY_CONTROL
        for i in range(10):
            p.setJointMotorControl2(self.bot_id, i, controlMode=mode, force=maxForce)

        c = p.createConstraint(self.bot_id, 1, self.bot_id, 3, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 1, self.bot_id, 2, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 6, self.bot_id, 8, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 6, self.bot_id, 7, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        res=p.getBasePositionAndOrientation(self.bot_id)
        pos=res[0]
        rot=p.getEulerFromQuaternion(res[1])

        obs=[]
        joint_states=[p.getJointState(self.bot_id, JOINTS[i]) for i in range(4)]
        for s in joint_states:
            obs.append(s[0]) # pos
        for s in joint_states:
            obs.append(s[1]) # vel
        for s in joint_states:
            obs.append(s[3]) # torque
        res=p.getBaseVelocity(self.bot_id)
        obs+=rot # orient (3)
        obs+=res[0] # lin vel (3)
        obs+=res[1] # ang vel (3)
        self.observation = obs 
        return np.array(self.observation).astype(np.float32)

    def step(self, action):
        mode = p.POSITION_CONTROL
        for i in range(4):
            a=action[i]
            if i in FORCE_ACTION:
                a=FORCE_ACTION[i]
            pos=a*math.pi
            joint_no=JOINTS[i]
            p.setJointMotorControl2(self.bot_id, joint_no, controlMode=mode, targetPosition=pos, force=MAX_TORQUE)

        p.stepSimulation()

        res=p.getBasePositionAndOrientation(self.bot_id)
        pos=res[0]
        #print("pos",pos)
        rot=p.getEulerFromQuaternion(res[1])

        obs=[]
        joint_states=[p.getJointState(self.bot_id, JOINTS[i]) for i in range(4)]
        for s in joint_states:
            obs.append(s[0]) # pos
        for s in joint_states:
            obs.append(s[1]) # vel
        for s in joint_states:
            obs.append(s[3]) # torque
        res=p.getBaseVelocity(self.bot_id)
        obs+=rot # orient (3)
        obs+=res[0] # lin vel (3)
        obs+=res[1] # ang vel (3)
        self.observation = obs 


        if self.prev_pos:
            reward=pos[1]-self.prev_pos[1]
        else:
            reward=0
        done = False

        if pos[2]<0.7:
            reward=0
            done=True

        self.step_counter += 1
        if not done and self.step_counter > MAX_EPISODE_LEN:
            reward = 0
            done = True

        info = {}

        self.prev_pos=pos
        return np.array(self.observation).astype(np.float32), reward, done, info

    def render(self):
        pass

    def _get_state(self):
        return self.observation

    def close(self):
        p.disconnect()
