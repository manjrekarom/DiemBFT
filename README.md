# DiemBFT #

Implementation of the Diem consensus protocol version 4 running on Diem blockchain responsible for formalizing agreement and finalizing transactions among a configurable set of validators when the system contains the Byzantine Failure.

## Platform
- Distalgo version: 1.1.0b15 
- Host machine
    - HP laptop running Ubuntu 20.04 and 18.04
    - HP laptop running Windows 10
- Python version: 3.7 CPython python.org 

## Workload Generation
main.da contains the implementation of the workload generation
- n_clients = config['n_clients']
- n_client_reqs = config['n_client_reqs']
- client_tmo = config['client_tmo']
- n_validators = config['n_validators']
- validator_rtt = config['validator_rtt']



## Timeouts
Client-round-trip-time : 
Validator-timeout : 

## Bugs and Limitations

## Main Files
1. DiemBFT/src/client.da
2. DiemBFT/src/ledger.py
3. DiemBFT/src/block.py
4. DiemBFT/srcsrc/pacemaker.da
5. DiemBFT/srcsrc/leader_election.da
6. DiemBFT/src/safety.da 
7. DiemBFT/src/mempool.da
8. DiemBFT/src/main.da
9. DiemBFT/src/client.da

## Code Size

## Language Feature Usage

## Contributions
* [Omkar Manjrekar](https://github.com/manjrekarom)
* [Archit Saxena](https://github.com/imarchit123)
* [Dinesh Tripathi](https://github.com/ditriparthi)

## Other comments
