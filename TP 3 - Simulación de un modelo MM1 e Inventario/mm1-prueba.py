import random
import numpy as np

class MM1Simulation:
    def __init__(self, lam, mu, max_customers=10000, queue_capacity=float('inf')):
        self.lam = lam
        self.mu = mu
        self.max_customers = max_customers
        self.queue_capacity = queue_capacity
        
    def run_single_replication(self):
        clock = 0.0
        num_in_system = 0
        times_of_arrival = []
        
        total_system_time = 0.0
        customers_served = 0
        blocked_customers = 0
        total_customers_attempted = 0
        
        # Variables para almacenar las integrales de area (Enfoque Averill Law)
        area_system = 0.0
        area_queue = 0.0
        area_utilization = 0.0
        
        next_arrival = random.expovariate(self.lam)
        next_departure = float('inf')
        
        while customers_served < self.max_customers:
            # Mecanismo de avance al evento siguiente
            next_event_time = min(next_arrival, next_departure)
            time_passed = next_event_time - clock
            
            # Actualizacion de integrales de area
            area_system += num_in_system * time_passed
            area_queue += max(0, num_in_system - 1) * time_passed
            if num_in_system > 0:
                area_utilization += 1.0 * time_passed
                
            clock = next_event_time
            
            # Procesamiento del evento
            if next_event_time == next_arrival:
                total_customers_attempted += 1
                current_queue_size = max(0, num_in_system - 1)
                if current_queue_size < self.queue_capacity:
                    num_in_system += 1
                    times_of_arrival.append(clock)
                    if num_in_system == 1:
                        next_departure = clock + random.expovariate(self.mu)
                else:
                    blocked_customers += 1
                next_arrival = clock + random.expovariate(self.lam)
            else:
                num_in_system -= 1
                customers_served += 1
                arrival_time = times_of_arrival.pop(0)
                total_system_time += (clock - arrival_time)
                
                if num_in_system > 0:
                    next_departure = clock + random.expovariate(self.mu)
                else:
                    next_departure = float('inf')
                    
        return {
            "L": area_system / clock,
            "Lq": area_queue / clock,
            "W": total_system_time / customers_served,
            "Wq": area_queue / clock,
            "Rho": area_utilization / clock,
            "P_blocking": blocked_customers / total_customers_attempted if total_customers_attempted > 0 else 0
        }