#import Pacemaker
#import Block_Tree
# #import 
import block
from src import pacemaker
from src import leader_election 


class Validator(process):

   def setup (servers):
        #self.broadcast = servers


    def process_certificate_qc(qc):
        block.BlockTree.process_qc(qc)
        leader_election.LeaderElection.update_leaders(qc)
        pacemaker.Pacemaker.advance_round(qc.vote_info.round)
    
    def process_proposal_msg(P):
        #process_certificate_qc(P.block.qc)
        #process_certificate_qc(P.block.qc)
        #Pacemaker.advance_round_tc(P.last_round_tc)
        round = pacemaker.current_round
        leader= leader_election.get_leader(current_round)
        if(P.block.round!=round or P.sender!=leader or P.block.author!= leader):
            return
        Block_Tree.execute_and_insert(P)
        vote_msg = Safety.make_vote(P.block,P.last_round_tc)
        if (vote_msg!=None):
            send(vote_msg, to=LeaderElection.get_leader(current_round))
        
    def process_timeout_msg(M):
        #process_certificate_qc(M.tmo_info.high_qc)
        #process_certificate_qc(M.high_commit_qc)
        PaceMaker.advance_round_tc(M.last_round_tc)
        tc = Pacemaker.process_remote_timeout(M)
        if tc != None:
            Pacemaker.advance_round(tc)
            process_new_round_event(tc)
    
    def process_vote_msg(M):
        qc= Block_Tree.process_vote(M)
        if qc!=None:
            process_certificate_qc(qc)
            process_new_round_event(None)
    
    def process_new_round_event(last_tc):
        u = LeaderElection.get_leader(Pacemaker.current_round)
        if(u==self.id):
            b =  Block_Tree.generate_block(MemPool.get_transactions(),PaceMaker.current_round)
            send(vote_msg, to=broadcast)

    def run():
        while(1):
            # process never stops
            if await(some(received((_, term, _, _, _, _, _)))):
                reset(received)

    def receive(msg=('LOCAL_TIMEOUT')):
        #Pacemaker.local_timeout_round()
        pass

    def receive(msg=('PROPOSAL_MESSAGE')):
        # process_proposal_msg(msg)
        pass

    def receive(msg=('VOTE_MESSAGE')):
        # process_vote_msg(msg)
        pass

    def receive(msg=('TIMEOUT_MSG')):
        #process_timeout_message(msg)
        pass


class Run(process):
    #def setup(config):
     #   self.nrounds = config['nrounds']
      #  self.npings = config['npings']
    
    def run():
        m = new(MainModule, num= 5)
        setup(m)
        start(m)

def main():
    config(clock='Lamport')
    configs = [{'nrounds':3, 'npings':3}, {'nrounds': 1, 'npings':2}]
    for config in configs:
        p = new(Run)
        setup(p,(config,))
        start(p)