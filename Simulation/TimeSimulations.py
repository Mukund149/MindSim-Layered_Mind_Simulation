from datetime import datetime, timedelta
import time

class Mind_clock:
    SIMULATION_SCALE = 96
    
    def __init__(self):
        self.SIMULATION_START_TIME = datetime(2026, 1, 1, 0, 0, 0)
        self.REAL_START_TIME = time.time()


    def now(self):
        self.elapsed_time = time.time() - self.REAL_START_TIME
        simulated_elapsed = self.elapsed_time * self.SIMULATION_SCALE
        current_simulated_time = self.SIMULATION_START_TIME + timedelta(seconds=simulated_elapsed)

        return current_simulated_time