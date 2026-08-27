import pkAddresses
from random import randrange
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from gbAiLib import AIBoy
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
actions = ['','a', 'b', 'left', 'right', 'up', 'down',  'select']

matrix_shape = (18, 20)
#game_area_observation_space = spaces.Box(low=0, high=255, shape=matrix_shape, dtype=np.uint32)

game_area_observation_space = spaces.Dict({
    "screen":spaces.Box(low=0, high=255, shape=matrix_shape, dtype=np.uint32),

})
class GenericPyBoyEnv(gym.Env):

    def __init__(self, debug=False):
        super().__init__()
        global rewards
        self.game = AIBoy("rom.gb", "rom.gb.state", debug)
        self._fitness=0
        rewards = 0
        self._previous_fitness=0
        self.items = 0
        self.levelSum = 0
        self.inBattle = 0
        self.pkmn = 0
        self.debug = debug
        self.exploredAreas = []
        self.maps = []

        self.currentMap = {}
        self.ticksInMap = 0
        self.timesPenalisedForMap = 0
        
        self.action_space = spaces.Discrete(len(actions))
        self.observation_space = game_area_observation_space
        self.lastAction = 0
        
    def step(self, action, render=False):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        global rewards
        self.lastAction = action
        # Move the agent
        if action == 0:
            pass
        else:
            self.game.pyboy.button(actions[action])

        # Consider disabling renderer when not needed to improve speed:
        # self.pyboy.tick(1, False)
        self.game.step(1,render)

        #done = self.pyboy.game_wrapper.game_over
        done = False
        self._calculate_fitness()
        #print(self._fitness, self._previous_fitness)
        reward=self._fitness-self._previous_fitness
        rewards += self._fitness - self._previous_fitness
        observation={
            "screen":self.game.pyboy.game_area(),

        }
        info = {}
        '''
        if self.game.seconds > 360:
            truncated = True
        else:
            truncated = False
        '''
        truncated = False
        #print(observation)
        return observation, reward, truncated, truncated, info

    def _calculate_fitness(self):

        self._previous_fitness=self._fitness
        mapNum = self.game.readMem(pkAddresses.MapNumber)
        x = self.game.readMem(pkAddresses.PlayerXPos)
        y = self.game.readMem(pkAddresses.PlayerYPos)
        prevItems = self.items
        self.items = self.game.readMem(pkAddresses.NumItems)
        prevPkmn = self.pkmn
        self.pkmn = self.game.readMem(pkAddresses.NumPokemonInParty)
        prevInBattle = self.inBattle
        self.inBattle = self.game.readMem(pkAddresses.InBattle)
        areaData = {"map": mapNum, "x": x, "y":y}
        prevLevelSum = self.levelSum
        self.levelSum = self.game.readMem(pkAddresses.Pokemon1Level) + self.game.readMem(pkAddresses.Pokemon2Level) + self.game.readMem(pkAddresses.Pokemon3Level) + self.game.readMem(pkAddresses.Pokemon4Level) + self.game.readMem(pkAddresses.Pokemon5Level) + self.game.readMem(pkAddresses.Pokemon6Level) 
        '''
        if self.lastAction == 1:
            self._fitness += 0.015
        elif self.lastAction == 5: 
            self._fitness += 0.015
        elif self.lastAction == 6:
            self._fitness += 0.0155
        elif self.lastAction == 3 or self.lastAction == 4:
            self._fitness += 0.014
        '''
        if areaData not in self.exploredAreas:
            self.exploredAreas.append(areaData)
            self._fitness += .01
            #print("INC DUE TO NEW AREA")
        
        
        currentmap = self.game.memory[0xd367:0xd396]
        '''
        if self.currentMap == currentmap and self.game.memory[0xd057] == 0:
            self.ticksInMap += 1
            if self.ticksInMap == 2000:
                self.ticksInMap = 0
                self.timesPenalisedForMap += 1
                self._fitness -= 0.15*self.timesPenalisedForMap
                print("too long in map")
        else:
            self.ticksInMap = 0
            self.currentMap = currentmap
            self.timesPenalisedForMap = 0
        '''
        if mapNum not in self.maps:
            self.maps.append(mapNum)
            print("INC DUE TO NEW MAP")
            self._fitness+= 0.5
        if self.items-prevItems != 0:
            print("CHANGE DUE TO ITEMS")
        if self.pkmn-prevPkmn != 0:
            print("CHANGE DUE TO POKEMON")
        if self.levelSum - prevLevelSum != 0:
            print("CHANGE DUE TO LEVEL")
        if prevInBattle == 0 and self.inBattle != 0:
            self._fitness += 7
            print("INC DUE TO BATTLE")
        self._fitness += 1*(self.items-prevItems)
        self._fitness += 3*(self.pkmn-prevPkmn)
        self._fitness += 5*(self.levelSum-prevLevelSum)
        # NOTE: Only some game wrappers will provide a score
        # If not, you'll have to investigate how to score the game yourself
        #self._fitness=self.pyboy.game_wrapper.score
        
    def reset(self, seed:int=42,**kwargs):
        self.game.reset()
        self._fitness=0
        self.items = 0
        self.pkmn = 0
        self.inBattle = 0
        self.levelSum = 0
        self.exploredAreas = []
        self.maps = []
        self._previous_fitness=0

        observation={
            "screen":self.game.pyboy.game_area(),

        }
        info = {}
        self.currentMap = {}
        self.ticksInMap = 0
        self.timesPenalisedForMap = 0
        
        return observation, info

    def render(self, mode='human'):
        pass

    def close(self):
        self.game.stop()
gym.register("pkred/pkred-v1", GenericPyBoyEnv)
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
    env = SubprocVecEnv([make(i) for i in range(num_cpu)])
    #env = gym.make("pkred/pkred-v1")
    #model = PPO("MultiInputPolicy", env, verbose=0,gamma=0.998)
    model = PPO.load("Model-checkpoint-v5-29-10-2024 14-51-02.zip", env)
    ep = 0

    while True:
        
        for count in range(0,2): 
            model.learn(total_timesteps=100000)
            print(f"EP {ep} FINISHED")
            vec_env = model.get_env()
            obs = vec_env.reset()
            rewardList = [0,0]
            '''
            for i in range(0,36000):
                action, _state = model.predict(obs, deterministic=False)
                obs, reward, done, info = vec_env.step(action)
                
                i = 0
                for r in reward:
                    rewardList[i] = rewardList[i] + r
                    i+= 1

                #for count in range(0,vec_env.num_envs):
                    #if reward[count] != 0:
                        #print(f"reward[{count}] = {reward[count]}")
                
                if done[0] and done[1]:
                    break
                #vec_env.render("human")
                # VecEnv resets automatically
            '''
        #Uncomment this block when ai is trained

        

            
            print("a")
            ep += 1
            log = open("traininglog-v5.txt","a")
            log.write("\n")
            log.write(f"Ep {ep} \n")
            for reward in rewardList:
                log.write(f"Reward: {reward}\n")
            #global rewards
            #log.write(f"Total: {rewards}\n")
            rewards = 0
            log.close()
        import datetime
        
        model.save(f"Model-checkpoint-v5-{datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.zip")
