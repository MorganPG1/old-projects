import gymnasium as gym
from gymnasium import spaces
import numpy as np
from pyboy import PyBoy

actions = ['','a', 'b', 'left', 'right', 'up', 'down', 'select']

matrix_shape = (16, 20)
game_area_observation_space = spaces.Box(low=0, high=256, shape=matrix_shape, dtype=np.uint32)

class GenericPyBoyEnv(gym.Env):

    def __init__(self, pyboy=PyBoy("rom.gb"), debug=False):
        super().__init__()

        self.pyboy = pyboy
        self._fitness=0
        self.score = 0
        self.prevLevelSum = 0
        self.punishedForLongBattle = False
        self._previous_fitness=0
        self.maps = []
        self.ticksInMap = 0
        self.timesPenalisedForMap = 0
        self.currentMap = None
        self.debug = debug
        self.ticks = 0
        self.prevMoney = 0
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


       
        money = memory[0xd347] + memory[0xd348] + memory[0xd349]
        if money > self.prevMoney:
            self.prevMoney = money
            score += 1
            print("inc due to money")
        pkm = memory[0xd163]
        if pkm > self.prevPkmn:
            self.prevPkmn = pkm
            score+=2*pkm-self.prevPkmn
            print("inc due to pkmn")
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
        items = memory[0xd31d]
        if items > self.prevItems:
            self.prevItems = items
            score += 2*items-self.prevItems
            print("inc due to items")
        levelSum = memory[0xd18c]+memory[0xd1b8] + memory[0xd1e4]+memory[0xd210]+memory[0xd23c]+memory[0xd268]
        if levelSum > self.prevLevelSum:
            self.prevLevelSum = levelSum
            score += 3*levelSum-self.prevLevelSum
            print("inc due to level sum")
        currentmap = memory[0xd367:0xd39c]
        if not currentmap in self.maps:
            self.maps.append(currentmap)
            score += 0.1*len(self.maps)
            self.ticksInMap = 0
            print("inc due to map")
            #print(score)

        if self.currentMap == currentmap and memory[0xd057] == 0:
            self.ticksInMap += 1
            if self.ticksInMap == 3500:
                self.ticksInMap = 0
                self.score -= 0.15*self.timesPenalisedForMap
                print("too long in map")
        else:
            self.ticksInMap = 0
            self.currentMap = currentmap
            self.timesPenalisedForMap = 0
        self._fitness = self._previous_fitness+score
        
        
    def reset(self, **kwargs):
        self.state = open("rom.gb.state", "rb")
        self.pyboy.load_state(self.state)
        self.state.close()
        self._fitness=0
        self._previous_fitness=0
        self.maps = []
        self.score = 0
        self.prevLevelSum = 0
        self.prevScore = 0
        self.ticks = 0
        self.prevItems = 0
        self.prevMoney = 0
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

    def close(self):
        print("close")
        self.pyboy.stop()

gym.register("pkred/pkred-v0", GenericPyBoyEnv)
env = gym.make("pkred/pkred-v0")

observation, info = env.reset(seed=42)
trainingAttempt = 0
while True:
    ep = 0
    epList = []
    rewardTotal = 0
    while ep <= 5:
        # this is where you would insert your policy
        action = env.action_space.sample()

        # step (transition) through the environment with the action
        # receiving the next observation, reward and if the episode has terminated or truncated
        observation, reward, terminated, truncated, info = env.step(action)

        rewardTotal +=reward
        # If the episode has ended then we can reset to start a new episode
        if terminated or truncated:
            ep+=1
            epList.append(rewardTotal)
            rewardTotal = 0
            observation, info = env.reset()
    i = 0
    trainingAttempt += 1
    sumOfReward = 0
    log = open("traininglog.txt", "a")
    print("Attempt: "+str(trainingAttempt)+"\n")
    log.write("Attempt: "+str(trainingAttempt)+"\n")

    for reward in epList:
        i+=1
        sumOfReward+= reward
        print(f"Episode {i}: {reward} \n")
        log.write(f"Episode {i}: {reward} \n")
    print(f"Mean is {sumOfReward/len(epList)} \n")
    log.write(f"Mean is {sumOfReward/len(epList)} \n")

    log.write("\n")
    log.close()
env.close()