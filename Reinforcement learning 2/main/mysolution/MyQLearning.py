from main.QLearning import QLearning


class MyQLearning(QLearning):

    def update_q(self, state, action, r, state_next, possible_actions, alpha, gamma):
        # TODO Auto-generated method stub 
        # Q(s,a)new = Q(s,a)old + alpha(r + gamma * Q(s',amax) - Q(s,a)old) where Qmax(s',amax) is the value of the best action so far in state s'
        # currentq = self.get_q(state, action)
        
        actionvalues = super(MyQLearning, self).get_action_values(state=state_next, actions=possible_actions)
        maxindex = actionvalues.index(max(actionvalues))
        oldq = self.get_q(state, action)

        qmax = self.get_q(state_next, possible_actions[maxindex])
        
        newvalue = oldq + alpha * (r + gamma * qmax - oldq)
        # newvalue = 0.0
        # if r > 0:
        #     print(newvalue)
        self.set_q(state, action, newvalue)
