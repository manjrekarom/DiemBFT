from collections import deque


class MemPool:    
    """
    Mempool class for storing validator comitted results and client commands 
    """
    def __init__(self):
        self.dq = deque()
        self.done_requests = dict()

    def try_to_add_to_mempool(self, message: tuple):
        proposal_no = message[1]
        client_id = message[2]
        msg = message[3]
        try:
            self.dq.index((proposal_no, client_id, msg))
            return
        except ValueError:
            print('Item not contained in mempool:dq. Add!!')
        print(f'proposal_no {proposal_no}, client_id {client_id}, msg {msg}')
        if (proposal_no, client_id) in self.done_requests:
            return self.done_requests[(proposal_no, client_id)]
        self.add_to_mempool(proposal_no, client_id, msg)
        return None

    def add_to_mempool(self, proposal_no, client_id, msg):
        print("Adding to dq")
        self.dq.append((proposal_no, client_id, msg))
        # print(self.dq[0])

    # def remove_from_mempool(self, state):
    #     self.dq.remove(state)

    def get_transactions(self):
        print(self.dq)
        if len(self.dq) < 1:
            print("WARNING: No transactions in mempool; Sending dummy.")
            return 'DUMMY'
        proposal_no, client_id, msg = self.dq.popleft() 
        # while (proposal_no, client_id) in self.done_requests:
        #     if len(self.done_requests) == 0:
        #         return None
        #     proposal_no, client_id, msg = self.dq[0]
        #     self.dq.popleft()
        return f'{proposal_no}--{client_id}--{msg}'
        
    def commit_to_cache(self, proposal_no, client_id, executed_state):
        _, _, message = executed_state.state_value.split('--')
        self.dq.remove((proposal_no, client_id, message))
        self.done_requests[(proposal_no, client_id)] = executed_state
