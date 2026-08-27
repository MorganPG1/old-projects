import gymnasium as gym
import sys
sys.setrecursionlimit(3000)
from gymnasium import spaces
import numpy as np
from pyboy import PyBoy
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
actions = ['','a', 'b', 'left', 'right', 'up', 'down', 'select']
rewards = 0
matrix_shape = (18, 20)
game_area_observation_space = spaces.Box(low=0, high=256, shape=matrix_shape, dtype=np.uint32)

class GenericPyBoyEnv(gym.Env):

    def __init__(self, pyboy=PyBoy("rom.gb"), debug=False):
        super().__init__()
        global rewards
        rewards = 0
        self.pyboy = pyboy
        self._fitness=0
        self.score = 0
        self.prevLevelSum = 0
        self.punishedForLongBattle = False
        self._previous_fitness=0
        self.displays = []
        self.mapList = []
        self.ticksInMap = 0
        self.timesPenalisedForMap = 0
        self.currentMap = None
        self.debug = debug
        self.ticks = 0
        self.prevMoney = 3
        self.prevPkmn = 0
        self.inBattle = False
        self.prevItems = 0
        self.lastAction = 0
        if not self.debug:
            self.pyboy.set_emulation_speed(0)

        self.action_space = spaces.Discrete(len(actions))
        self.observation_space = game_area_observation_space
        #print("init")
        self.state = open("rom.gb.state", "rb")
        self.pyboy.load_state(self.state)
        self.state.close()
        #print(self.pyboy.game_wrapper)

    def step(self, action):
        self.ticks +=1
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        #print("step")
        # Move the agent
        if action == 0:
            pass
        else:
            self.lastAction = action
            self.pyboy.button(actions[action])

        # Consider disabling renderer when not needed to improve speed:
        # self.pyboy.tick(1, False)
        self.pyboy.tick(1)

        #done = self.pyboy.game_wrapper.game_over()

        self._calculate_fitness()
        reward=self._fitness-self._previous_fitness
        if reward != 0:
            global rewards
            rewards += reward
            print("Reward:", reward)
        if self.ticks == 10000:
            print("hit 10,000 ticks")

            self.prevScore = self.score
            self.score = self._fitness
            print(self.score, self.prevScore, self.score)
            if self.prevScore == self.score or self.score < self.prevScore:
                done = True
                #print("score same")
            else:
                done = False
                #print("score increased")
            self.ticks = 0
        else:
            done = False
        observation=self.pyboy.game_area()
        info = {}
        truncated = False
        #print(observation)
        return observation, reward, done, truncated, info

    def _calculate_fitness(self):
        #print("calc  fit")
        self._previous_fitness=self._fitness

        # NOTE: Only some game wrappers will provide a score
        # If not, you'll have to investigate how to score the game yourself
        score = 0
        memory = self.pyboy.memory
        screen = self.pyboy.game_area()
        sumOfPixels = 0
        unique = True
        '''
        for line in screen:
            for pixel in line:
                sumOfPixels+=pixel
        mean = sumOfPixels/360
        
        for display in self.displays:
            if abs(mean-display) < 25:
                unique = False
                break
            
        if unique:
            print("unique display", self.displays, mean)
            score += 1
            self.displays.append(mean)
        else:
            #print("display not unique", self.displays, mean)

            pass


        '''
        currentmap = memory[0xd367:0xd396]
        if self.currentMap == currentmap and memory[0xd057] == 0:
            self.ticksInMap += 1
            if self.ticksInMap == 2000:
                self.ticksInMap = 0
                self.timesPenalisedForMap += 1
                self.score -= 0.15*self.timesPenalisedForMap
                print("too long in map")
        else:
            self.ticksInMap = 0
            self.currentMap = currentmap
            self.timesPenalisedForMap = 0

        if memory[0xd057] != 0:
            if self.inBattle == False:
                score += 5
                print("inc due to in battle")
                self.inBattle = True
            else:
                if memory[0xccd5] > 6:
                    if self.punishedForLongBattle == False:
                        score -= 0.2
                        print("too long in battle")
                        self.punishedForLongBattle = True
                else:
                    self.punishedForLongBattle = False
        else:
            if self.inBattle and not self.punishedForLongBattle:
                print("inc due to desired battle")
                self.score += 4
            self.inBattle = False

        if currentmap not in self.mapList:
            self.mapList.append(currentmap)
            if len(self.mapList) > 2:
                score += 1
                print("New map")
        
        items = memory[0xd31d]
         
        score += 0.5*(items-self.prevItems)
        if items-self.prevItems > 0:
            score += 0.5*(items-self.prevItems)
        else:
            score += 0.75*(items-self.prevItems)
        self.prevItems = items

        pkmn = memory[0xd163]
        if pkmn > self.prevPkmn:
            self.prevPkmn = pkmn
            score += (pkmn - self.prevPkmn)*5
            print("New pokemon")
        levelSum = memory[0xd18c]+memory[0xd1b8] + memory[0xd1e4]+memory[0xd210]+memory[0xd23c]+memory[0xd268]
        if levelSum > self.prevLevelSum:
            self.prevLevelSum = levelSum
            score += 3*(levelSum-self.prevLevelSum)
            print("Increased Level")
        '''
        if score + self._previous_fitness > 0:
            print("Score:",score+self._previous_fitness)
        '''
        self._fitness = score + self._previous_fitness
    def reset(self, seed=42,**kwargs):
        self.state = open("rom.gb.state", "rb")
        self.pyboy.load_state(self.state)
        self.state.close()
        self._fitness=0
        self.seed = seed

        self._previous_fitness=0
        self.displays = []
        self.mapList = []
        self.score = 0
        self.prevLevelSum = 0
        self.prevScore = 0
        self.ticks = 0
        self.prevItems = 0
        self.prevMoney = 3
        self.inBattle = False
        self.punishedForLongBattle = False
        self.timesPenalisedForMap
        self.ticksInMap = 0
        self.prevPkmn = 0
        self.lastAction = 0
        observation=self.pyboy.game_area()
        info = {}
        return observation, info

    def render(self, mode='human'):
        pass
    
    def __getstate__(self):
        data = {}
        data["fitness"] = self._fitness
        data["score"] = self.score
        data["prevLevelSum"] = self.prevLevelSum
        data["punishedForLongBattle"] = self.punishedForLongBattle
        data["previous_fitness"] = self._previous_fitness
        data["displays"] = self.displays
        data["ticksInMap"] = self.ticksInMap
        data["mapList"]=self.mapList
        data["timesPenalisedForMap"] = self.timesPenalisedForMap
        data["currentMap"] = self.currentMap
        data["debug"] = self.debug
        data["ticks"] = self.ticks
        data["prevMoney"] = self.prevMoney
        data["prevPkmn"] = self.prevPkmn
        data["inBattle"] = self.inBattle
        data["prevItems"] = self.prevItems
        data["lastAction"] = self.lastAction
        return data
    
    def __setstate__(self, data):
        self._fitness=data["fitness"]
        self.score = data["score"] 
        self.prevLevelSum = data["prevLevelSum"]
        self.punishedForLongBattle = data["punishedForLongBattle"] 
        self._previous_fitness = data["previous_fitness"]
        self.displays = data["displays"]
        self.ticksInMap = data["ticksInMap"]
        self.mapList = data["mapList"]
        self.timesPenalisedForMap = data["timesPenalisedForMap"]
        self.currentMap= data["currentMap"]
        self.debug = data["debug"]
        self.ticks=data["ticks"]
        self.prevMoney=data["prevMoney"]
        self.prevPkmn=data["prevPkmn"]
        self.inBattle = data["inBattle"]
        self.prevItems=data["prevItems"]
        self.lastAction=data["lastAction"]
        self.pyboy = PyBoy("rom.gb")
        self.state = open("rom.gb.state", "rb")
        self.pyboy.load_state(self.state)
        self.state.close()
        return self

    def close(self):
        print("close")
        self.pyboy.stop()

gym.register("pkred/pkred-v0", GenericPyBoyEnv)

def make(i):
    def _init():
        seed = 42
        seed += i
        env = GenericPyBoyEnv()
        env.reset(seed)
        return env
    return _init

if __name__ == '__main__':
    num_cpu = 4
    #env = DummyVecEnv([make(i) for i in range(num_cpu)])
    env = gym.make("pkred/pkred-v0")
    #model = PPO("MlpPolicy", env, verbose=1)
    model = PPO.load("Model-checkpoint-28-10-2024 12-58-36", env)
    ep = 0
    while True:
        for count in range(0,10):
            model.learn(total_timesteps=10_000)

            vec_env = model.get_env()
            obs = vec_env.reset()
            totalReward = 0

            for i in range(8500):
                action, _state = model.predict(obs, deterministic=True)
                obs, reward, done, info = vec_env.step(action)

                for r in reward:
                    totalReward += r
                #vec_env.render("human")
                # VecEnv resets automatically



            print("a")
            ep += 1
            log = open("traininglog-v2.txt","a")
            log.write("\n")
            log.write(f"Ep {ep} \n")
            log.write(f"Total reward: {rewards}\n")
            rewards = 0
            log.close()
        import datetime
        
        model.save(f"Model-checkpoint-{datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.zip")
        env.close()
        vec_env.close()