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
        d = self.discount
        r = self.mdp.getReward
        print " Discount: ", d
        for i in range(self.iterations):
            # q = list()
            for st in self.mdp.getStates():
                q = list()
                # print "{}".format(self.mdp.getTransitionStatesAndProbs(st, ac)
                for ac in self.mdp.getPossibleActions(st):
                    # print " possible actions ({}): {}".format(st, self.mdp.getPossibleActions(st))
                    # print "{}".format(self.mdp.getTransitionStatesAndProbs(st, ac))
                    s = 0
                    for ns, p in self.mdp.getTransitionStatesAndProbs(st, ac):
                        s += p * (r(st, ac, ns) + d*self.values[ns])
                        print "r({}, {}, {}) = {}, P = {}".format(st, ac, ns, r(st, ac, ns), p)
                        print " p = {}".format(p)
                        print " r = {}".format(r(st, ac, ns))
                        print " d = {}".format(d)
                        print " self.values[ns] = {}".format(self.values[ns])
                        print " temp sum = {}".format(p * (r(st, ac, ns) + d*self.values[ns]))
                    # s = sum(map(lambda (ns, p): p * (r(st, ac, ns) + d * self.values[ns]) , self.mdp.getTransitionStatesAndProbs(st, ac)))
                    q.append(s)

                max_q = max(q) if (len(q) > 0) else 0
                self.values[st] = max_q
                print "Value at ({}) = {}".format(st, self.values[st])


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
        # util.raiseNotDefined()
        s = 0
        for ns, p in self.mdp.getTransitionStatesAndProbs(state, action):
            r = self.mdp.getReward(state, action, ns)
            s += p * (r + self.discount * self.values[ns])
        return s

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

        max_action = None
        max_value = -sys.maxint
        for action in self.mdp.getPossibleActions(state):
            for ns, _ in self.mdp.getTransitionStatesAndProbs(state, action):
                if self.values[ns] > max_value:
                    max_value = self.values[ns]
                    max_action = action

        if self.mdp.isTerminal(state):
            return None
        return max_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
