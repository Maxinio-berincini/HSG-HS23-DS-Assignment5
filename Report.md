Assignment 5 
---------------------

# Team Members

- Leon Luca Klaus Muscat
- Felix Kappeler
- Max Beringer

# GitHub link to your (forked) repository

>https://github.com/Maxinio-berincini/HSG-HS23-DS-Assignment5/

# Task 1

Note: Some questions require you to take screenshots. In that case, please join the screenshots and indicate in your answer which image refer to which screenshot.

1. What happens when Raft starts? Why?

Ans: 
> A node can be in one of three states: leader, follower, or candidate.
> 
> At the start of the Raft, every node starts as a follower. The follower waits to hear from the leader, as the leader sends periodical heartbeats.
> If the follower does not hear from the leader for a random amount of time (election timeout), it becomes a candidate. 
> A candidate initiates a leader election, by requesting votes from the other nodes.
> If the candidate receives votes from a majority of the nodes, then it becomes leader.
> 
> A leader is crucial to achieve consensus with multiple nodes, to store data in a distributed system.
> 
> >Source: https://thesecretlivesofdata.com/raft/

2. Perform one request on the leader, wait until the leader is committed by all servers. Pause the simulation.
Then perform a new request on the leader. Take a screenshot, stop the leader and then resume the simulation.
Once, there is a new leader, perform a new request and then resume the previous leader. Once, this new request is committed by all servers, pause the simulation and take a screenshot. Explain what happened?

Ans: 
> As soon as the request was made, the request was appended to the leader's log.
> As the leader was paused, the request was never sent to the followers.
> A new leader was elected, and the new request was appended to the new leader's log.
> The new leader send the request to the followers, and the request was appended to the followers' logs and committed.
> When the old leader was resumed, it received a heartbeat from the new leader, and as the new leader had a higher term, the old leader stepped down and became a follower.
> Because the old leader had a lower term, the last uncommitted entry was rolled back, and the old leader's log was updated to match the new leader's log.
>> Source: https://thesecretlivesofdata.com/raft/#replication

3. Stop the current leader and two other servers. After a few increase in the Raft term, pause the simulation and take a screenshot. Then resume all servers and restart the simulation. After the leader election, pause the simulation and take a screenshot. Explain what happened.

Ans: 
> As soon as the leader was stopped, a follower became a candidate and started an election.
> As there were a total number of 5 nodes, the candidate needed 3 votes to become leader.
> The candidate only received 2 votes (his own and the one from the remaining node), the election failed and a new election was started.
> This raised the election term. 
> Because no leader was elected, the cycle repeated itself, until the other three nodes were started again.
> The current candidate periodically sent out vote request to all the nodes as long as it gets a vote, until it receives a heartbeat from a leader with a higher term, or until its time runs out.
> Because the old leader received a vote request from a candidate with a higher term, it stepped down and became a follower.
> The candidate became the new leader, and the term of the previously stopped nodes was updated to match the new leader's term.

# Task 2

1. Indicate the replies that you get from the "/admin/status" endpoint of the HTTP service for each servers. Which server is the leader? Can there be multiple leaders?

Ans: 

2. Perform a Put request for the key ``a" on the leader. What is the new status? What changes occurred and why (if any)?

Ans:

3. Perform an Append request for the key ``a" on the leader. What is the new status? What changes occurred and why (if any)?

Ans: 

4. Perform a Get request for the key ``a" on the leader. What is the new status? What change (if any) happened and why?

Ans:



# Task 3

1. Shut down the server that acts as a leader. Report the status that you get from the servers that remain active after shutting down the leader.

Ans:

 2. Perform a Put request for the key "a". Then, restart the server from the previous point, and indicate the new status for the three servers. Indicate the result of a Get request for the key ``a" to the previous leader.

Ans:

3. Has the Put request been replicated? Indicate which steps lead to a new election and which ones do not. Justify your answer using the statuses returned by the servers.

Ans:

4. Shut down two servers, including the leader --- starting with the server that is not the leader. Report the status of the remaining servers and explain what happened.

Ans:

5. Can you perform Get, Put, or Append requests in this system state? Justify your answer.

Ans:

6. Restart the servers and note down the new status. Describe what happened.

Ans:




# Task 4

1. What is a consensus algorithm? What are they used for in the context of replicated state machines? 

Ans: 
> A consensus algorithm is a process to achieve an agreement on a subject by multiple participants.
> It is used to achieve consensus in a distributed system, where multiple nodes need to agree on a value. 
> They are crucial for maintaining reliability and consistency in a distributed system.

2. What are the main features of the Raft algorithm? How does Raft enable fault tolerance? 

Ans: 
> Raft is a consensus algorithm. It uses a leader and follower model, where the leader is responsible for replicating the log to the followers.
> It uses a heartbeat mechanism to ensure that the followers are still alive and toggle a re-election if the leader dies.
> Raft enables fault tolerance by replicating the log to multiple nodes, so that if one node dies, the log can still be replicated to other nodes.


3. What are Byzantine failures? Can Raft handle them?

Ans: 
> Byzantine fault comes from the Byzantine Generals' Problem, where a group of generals need to agree on a common plan of action, but some generals are traitors and try to sabotage the plan.
> In a distributed system, a Byzantine failure is when a node sends conflicting information to other nodes.
> Raft cannot handle Byzantine failures, as it assumes that the nodes are not malicious and will not send conflicting information.
> It can only handle crash failures, where a node dies and stops sending information.