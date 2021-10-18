# Validity Checks for Cryptographic Values

#### Key Distribution

1. Create private and public key pairs for clients and validators (in `RunDiem`).
2. Pass the keys as relevant in the setup. Validator and client public keys sent to everyone.

#### Serialisation

1. Complex datatypes were implemented using dataclasses in Python.
2. These are serialized to tuple (or tuple of tuples) before **sending** in distalgo.
3. A string representation of methods are used for signing.

#### Libraries

PyNaCl is used hashing and signing messages. Wrapper functions over PyNaCl were defined to make hashing variable number of items together.

1. hasher(*items) appends items and hashes them using **SHA256** and returns a string.
2. sign(private_key, *items) appends and signs items using **ed25519** and returns a string.

#### 1. Validating authenticity of the sender

**Steps taken at the sender are as follows:**

1. Before sending a message, generate signature using private key of the sender. 
2. Send message and signature.

**Steps taken at the receiver are as follows:**

1. In the receive handler, bind message, signature and sender.
2. Use public key of the sender to retrieve message from the signature. 
3. Compare with plain-text message.

#### 2. Validating signatures contained in Messages (Vote and Proposal)

`valid_signatures()` is only ever called on **QC** and **TC** as these contain signatures on votes and timeouts.

**QC**

1. Verify `author_signatures` in **QC** using private key of the sender **(leader)**.
2. Verify all `signatures` by recovering `ledger_commit_info` from signature and matching it against `ledger_commit_info` provided in QC.

**TC**

1. Verify `tmo_high_qc_rounds` by recovering them from `tmo_signatures`.

#### 3. Hashing

Hash is verified using hasher