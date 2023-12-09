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
>From the responses of the "/admin/status" endpoint for each server, we can observe the following information:
>
>Server 127.0.0.1:6000 (server 0)
Leader: It identifies itself as the leader (leader = TCPNode('127.0.0.1:6000'))
Partner Nodes: Lists other nodes it's partnered with (partner_nodes_count = 2)
Raft Term: Current term is 1 (raft_term = 1)
>
>Server 127.0.0.1:6001 (server 1)
State: Follower (state = 0)
Leader: Indicates that server 127.0.0.1:6000 is the leader (leader = TCPNode('127.0.0.1:6000'))
Partner Nodes: Lists other nodes it's partnered with (partner_nodes_count = 2)
Raft Term: Current term is 1 (raft_term = 1)
>
>Server 127.0.0.1:6002 (server 2)
State: Follower (state = 0)
Leader: Indicates that server 127.0.0.1:6000 is the leader (leader = TCPNode('127.0.0.1:6000'))
Partner Nodes: Lists other nodes it's partnered with (partner_nodes_count = 2)
Raft Term: Current term is 1 (raft_term = 1)
>
>Leader: Server 127.0.0.1:6000 is identified as the leader by all servers.
>
>Typically there cannot be multiple leaders in a typical Raft consensus-based distributed system. In this scenario, all servers agree that 127.0.0.1:6000 is the leader, which aligns with the Raft consensus algorithm's design where a single leader is elected to maintain consistency and coordination among the nodes. However, in scenarios involving network partitions or network failures, the system might encounter situations where a node or set of nodes are isolated from each other, leading to a potential split vote.

2. Perform a Put request for the key ``a" on the leader. What is the new status? What changes occurred and why (if any)?

Ans:
>The values for log_len, last_applied, commit_idx, next_node_idx_server_127.0.0.1:6001, next_node_idx_server_127.0.0.1:6001, match_idx_server_127.0.0.1:6001, match_idx_server_127.0.0.1:6002 and leader_commit_idx went up from 2 to 3.
>
>The values for next_node_idx_server_127.0.0.1:6001 and next_node_idx_server_127.0.0.1:6002 on server 127.0.0.1:6000 went up from 3 to 4
>
>And the uptime increased by around 20.
>
>The Raft consensus algorithm ensures that put is replicated and committed across the nodes. The increase in last_applied and commit_idx indicates successful replication and commit of this change.

3. Perform an Append request for the key ``a" on the leader. What is the new status? What changes occurred and why (if any)?

Ans: 
>The values for log_len, last_applied, commit_idx, next_node_idx_server_127.0.0.1:6001, next_node_idx_server_127.0.0.1:6001, match_idx_server_127.0.0.1:6001, match_idx_server_127.0.0.1:6002 and leader_commit_idx went up from 3 to 4.
>
>The values for next_node_idx_server_127.0.0.1:6001 and next_node_idx_server_127.0.0.1:6002 on server 127.0.0.1:6000 went up from 4 to 5.
>
>And the uptime increased by around 15.
>
>The Raft consensus algorithm ensures that Append requests are replicated and committed across the nodes in the cluster to maintain consistency. The increase in last_applied and commit_idx indicates the successful replication and commitment of this change across the nodes, ensuring consistency within the cluster.


4. Perform a Get request for the key ``a" on the leader. What is the new status? What change (if any) happened and why?

Ans:
>Nothing has changed, except for the uptime slightly increasing by 15.
>
>The GET request simply retrieves the current value associated with the key a without making any modifications to the data store or the Raft log, thus keeping the status variables unchanged.


# Task 3

1. Shut down the server that acts as a leader. Report the status that you get from the servers that remain active after shutting down the leader.

Ans:
> Server 127.0.0.1:6001 (server 1)
>
> Before shutdown:
> - State Follower (State = 0)
> - 127.0.0.1:6000 as leader
>
> After Shutdown:
> - State Follower (State = 0)
> - log_len, last_applied, and commit indices increased from 2 to 3
> - raft_term increased from 1 to 3
>
> Server 127.0.0.1:6002 (server 2)
>
> Before shutdown:
> - State Follower (State = 0)
> - 127.0.0.1:6000 as leader
>
> After Shutdown:
> - State Leader (State = 2)
> - log_len, last_applied, and commit indices increased from 2 to 3
> - raft_term increased from 1 to 3
> - match_idx_server_127.0.0.1:6000 with value 0
> - match_idx_server_127.0.0.1:6000 with value 3
> - value for partner_node_status_server_127.0.0.1:6000 is 0 (non-operational / inactive state)

2. Perform a Put request for the key "a". Then, restart the server from the previous point, and indicate the new status for the three servers. Indicate the result of a Get request for the key ``a" to the previous leader.

Ans:
>A PUT request for the key "a" was made to server 127.0.0.1:6002
>
>Server 127.0.0.1:6000 was restarted
>
>Post restart:
>Server 127.0.0.1:6000 (server 0):
>- Came back up with the state 0 and recognized 127.0.0.1:6002 as the leader
Server 127.0.0.1:6001 (server 1):
>- Continued in state 0 and recognized 127.0.0.1:6002 as the leader
Server 127.0.0.1:6002 (server 2):
>- Remained in state 2, recognized itself as the leader, and updated various indices
>- partner_node_status_server_127.0.0.1:6000 changed from 0 to 2 (operational / active state)
>
>In general:
>- log_len, last_applied, and commit indices increased from 3 to 4
>
>Result of Get request for key "a" to previous leader 127.0.0.1:6000:
>- returns ["cat", "dog"], which is the content that was set for the key "a" in the previous Put request.
>- therefore the content for key "a" was updated on the previously shut down server 127.0.0.1:6000 and holds the correct value.

3. Has the Put request been replicated? Indicate which steps lead to a new election and which ones do not. Justify your answer using the statuses returned by the servers.

Ans:
>From the provided information, the GET request for the key a on port 8080 returns ["cat", "dog"]. This indicates that the PUT request for the key "a" with the value ["cat", "dog"] has been successfully replicated across the servers.
>
>New election eccurence:
>- An election occurs when a server detects that the current leader is unavailable or if the leader cannot be reached.
>- In Raft, this usually happens due to the lack of communication or the inability to reach the leader within a specified time frame (election timeout).
>- The servers then initiate a new election by starting the election process and voting for a new leader.
>
>No reasons for new election occurence:
>- An election doesn't necessarily occur when the leader initiates a successful replication of a PUT request across the servers.
>- Replication of a PUT request doesn't directly trigger an election unless there's a failure in communication or a leader's unavailability, which forces the system to initiate a new leader election.
>- no new election occurs when a server that is in the state Follower (state = 0) shuts down.
>
>we can see if a new leader was set into place:
>- by looking if the value of raft_term has increased
>- if the value for Leader ex. leader = TCPNode('127.0.0.1:6002') has changed

4. Shut down two servers, including the leader --- starting with the server that is not the leader. Report the status of the remaining servers and explain what happened.

Ans:
>After shutting down 127.0.0.1:6001 (Follower) and then 127.0.0.1:6002 (Leader)
>status on 127.0.0.1:6000:
>- status for partner_node_status_server_127.0.0.1:6001 and partner_node_status_server_127.0.0.1:6002 change from 2 to 0
>- log_len, last_applied, and commit indices remain unchanged
>- status from has_quorum turns from True to False. 
>
>Explanation:
>- In Raft, maintaining quorum (a majority of nodes available) is crucial for system operations.
>- without quorum the system can't come to an agreement, the system can't operate correctly 
>- Maintaining quorum is crucial because it ensures that even if some nodes fail or become unreachable, the system can still make progress, agree on new changes, and maintain consistency without risking data loss or inconsistency

5. Can you perform Get, Put, or Append requests in this system state? Justify your answer.

Ans:
>Performing Get, Put, or Append requests might not guarantee the expected behavior or consistency due to the absence of a quorum. Here's why:
>- Get Request: It might returned data, but it was outdated and incomplete due to the lack of consensus and the unavailability of the majority of nodes to fetch the most recent data
>- Put and Append Requests: These operations might appear to succeed (returning a 204 status code) but the changes are not be properly replicated and committed across the majority of nodes.
>- The value has_quorum = False means it's in a degraded state where operations might not be reliable or consistent. While the requests seem to have been accepted (returning successful status codes), the absence of a quorum implies potential inconsistencies or data loss once the system returns to a functional state.
>- this is because there aren't other nodes in the system that can replicate the data because there isn't a majority that could confirm that the nodes have written the new entry and the leader can't notify the followers that the entry is commited.

6. Restart the servers and note down the new status. Describe what happened.

Ans:
>Upon restarting the servers 127.0.0.1:6001 and 127.0.0.1:6002, the system has now regained a quorum. Here the states:
>
>127.0.0.1:6000 (Server 0)
>- Leader (Status = 2)
>- has_quorum = True
>- log_len increased from 2 to 3
>- commit_index increased from 4 to 5
>- keys: Get request for "a" returns ["cat", "dog"]
>  
>127.0.0.1:6001 (Server 1) and 127.0.0.1:6002 (Server 2)
>- Follower (Status = 0)
>- keys: Get request for "a" returns ["cat", "dog"]
>
>The system has regained quorum and all nodes are in agreement, displaying the same log length, commit index, and leader information. The leader's log index has increased, indicating a new entry. In addition, retrieving the key "a" returns ["cat", "dog"], confirming the persistence of the data. This synchronization between nodes restores consistency and ensures proper replication of changes throughout the cluster. However, the previously appended value (while the other servers were down) "mouse" wasn't appended to the restarted servers. So the append without quorum wasn't commited into the cluster.

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
