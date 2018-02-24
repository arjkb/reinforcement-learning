# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

import sys

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        self.actions = dict()

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # print " States: ", mdp.getStates()
        # for state in mdp.getStates():
        #     print " Actions from state {} = {}".format(state, mdp.getPossibleActions(state))
        #     for action in mdp.getPossibleActions(state):
        #         print " T({}, {}) = {}".format(state, action, mdp.getTransitionStatesAndProbs(state, action))
        #         # nextState, _ = mdp.getTransitionStatesAndProbs(state, action)
        #         for ns, _ in mdp.getTransitionStatesAndProbs(state, action):
        #             print " R({}, {}, {}) = {}".format(state, action, ns, mdp.getReward(state, action, ns))

        # print " Start State: ", self.mdp.getStartState()
        d = self.discount
        r = self.mdp.getReward
        for i in range(iterations):
            for st in self.mdp.getStates():
                q = list()
                for ac in self.mdp.getPossibleActions(st):
                    s = 0
                    # print " possible actions ({}): {}".format(st, self.mdp.getPossibleActions(st))
                    s = sum(map(lambda (ns, p): p * (r(st, ac, ns) + d * self.values[ns]) , self.mdp.getTransitionStatesAndProbs(st, ac)))

                    # # probabilities of ending up in ns after taking action ac
                    # for ns, p in self.mdp.getTransitionStatesAndProbs(st, ac):
                    #     r = self.mdp.getReward(st, ac, ns)
                    #     s += p * (r + self.discount * self.values[ns])
                    #     # print " ({}, {}) ns={} t={}, r={}, s={}".format(st, ac, ns, p, r, s)
                    print " SUM == ", s
                    # q.append((s, ac))

                max_q, max_ac = max(q, key=lambda x: x[0]) if (len(q) > 0) else (0, None)
                self.values[st] = max_q
                self.actions[st] = max_ac
                # print " q: {}, max(q)={}, max_action={}".format(q, max_q, max_ac)
        print " values: ", self.values
        print " actions: ", self.actions


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        print " Computing Q value for state = {}, action = {} ".format(state, action)
        s = 0
        for ns, p in self.mdp.getTransitionStatesAndProbs(state, action):
            r = self.mdp.getReward(state, action, ns)
            s += p * (r + self.discount * self.values[ns])
        return s
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        print " Computing action for state ", state

        max_action = None
        max_value = -sys.maxint

        for action in self.mdp.getPossibleActions(state):
            for ns, _ in self.mdp.getTransitionStatesAndProbs(state, action):
                print " ns={}, v={}".format(ns, self.values[ns])

                if self.values[ns] > max_value:
                    max_value = self.values[ns]
                    max_action = action


        print " A = {}, V = {}".format(max_action, max_value)
        if self.mdp.isTerminal(state):
            return None

        return max_action

        if state not in self.actions:
            return None
            print " {} Not Found!".format(state)

        return self.actions[state]
        return 'north'

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
