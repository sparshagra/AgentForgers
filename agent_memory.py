# agent_memory.py

class AgentMemory:
    """
    Memory module for agents supporting:
    - Short-term memory (STM) for recent history/context window
    - Long-term memory (LTM) for persistent learning/user preferences
    - Episodic memory for full session/task logs
    """

    def __init__(self, user_id=None, stm_size=5):
        self.user_id = user_id
        self.stm = []        # Short-term memory window
        self.ltm = []        # Long-term memory (can persist this to DB/file)
        self.episodic = []   # Detailed log of every step in a workflow
        self.stm_size = stm_size

    def remember(self, entry, ltm=False):
        """
        Add an entry to memories.
        If ltm=True, push to long-term as well.
        """
        self.stm.append(entry)
        self.episodic.append(entry)
        if len(self.stm) > self.stm_size:
            self.stm.pop(0)  # Limit STM window size
        if ltm:
            self.ltm.append(entry)

    def recall_stm(self, n=None):
        """
        Recall last n entries from short-term memory (default is stm_size).
        """
        window = n or self.stm_size
        return self.stm[-window:]

    def recall_ltm(self):
        """
        Recall all entries stored in long-term memory.
        """
        return self.ltm

    def recall_episodic(self):
        """
        Recall full log of agent task/session.
        """
        return self.episodic

    def reset(self, keep_ltm=True):
        """
        Reset the memory for a new session/episode.
        """
        self.stm = []
        self.episodic = []
        if not keep_ltm:
            self.ltm = []
