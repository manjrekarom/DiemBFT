from collections import deque


class MemPool:    
    """
    Mempool class for storing validator comitted results and client commands 
    """
    def __init__(self):
        self.dq = deque()
        self.done_requests = dict()

    def try_to_add_to_mempool(self,message:tuple):
        proposal_no = message[1]
        client_id = message[2]
        message_content = message[3]
        print("I am trying to add to mempool")
        print("message_content is", message_content)
        print("message_content is", client_id)
        print("message_content is", proposal_no)
        if (proposal_no, client_id) in self.done_requests:
            return self.done_requests[(proposal_no, client_id)]
        else:
            self.add_to_mempool(proposal_no, client_id, message_content)
            return None

    def add_to_mempool(self, proposal_no, client_id, message_content):
        print("Adding to dq")
        self.dq.append((proposal_no, client_id, message_content))
        print(self.dq[0])

    def get_transactions(self):
        print(self.dq[0])
        proposal_no, client_id, message_content = self.dq[0] 
        while (proposal_no, client_id) in self.done_requests:
            if len(self.done_requests)==0:
                return None
            proposal_no, client_id, message_content = self.dq[0]
            self.dq.popleft()
        return f'{proposal_no}--{client_id}--{message_content}'
        
    def commit_to_cache(self,proposal_no, client_id, executed_state):
        self.done_requests[(proposal_no,client_id)] = executed_state
