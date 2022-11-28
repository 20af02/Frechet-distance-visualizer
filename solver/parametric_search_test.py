import threading
class ParametricSearch:
    def __init__(self, decision_func, queue_size=10):
        self.decision_func = decision_func
        self.queue = []
        self.queue_size = queue_size
        self.lock = threading.Lock()

    def enqueue(self, x):
