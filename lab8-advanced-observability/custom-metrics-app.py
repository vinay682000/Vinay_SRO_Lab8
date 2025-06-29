from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import random
import threading

# Define custom metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_duration_seconds', 'Request latency')
ACTIVE_USERS = Gauge('app_active_users', 'Number of active users')
ERROR_RATE = Counter('app_errors_total', 'Total application errors', ['error_type'])

def simulate_web_traffic():
    """Simulate web application traffic with metrics"""
    endpoints = ['/api/users', '/api/orders', '/api/products', '/api/health']
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    error_types = ['timeout', 'validation', 'database', 'auth']
    
    while True:
        # Simulate request
        endpoint = random.choice(endpoints)
        method = random.choice(methods)
        
        # Record request
        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        
        # Simulate request processing time
        with REQUEST_LATENCY.time():
            processing_time = random.uniform(0.1, 2.0)
            # Occasionally simulate slow requests
            if random.random() < 0.05:  # 5% chance of slow request
                processing_time += random.uniform(3.0, 8.0)
            time.sleep(processing_time)
        
        # Simulate errors (10% error rate)
        if random.random() < 0.1:
            error_type = random.choice(error_types)
            ERROR_RATE.labels(error_type=error_type).inc()
        
        # Update active users (simulate fluctuation)
        current_users = max(0, 100 + random.randint(-20, 30))
        ACTIVE_USERS.set(current_users)
        
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == '__main__':
    # Start metrics server
    start_http_server(8000)
    print("Metrics server started on port 8000")
    
    # Start traffic simulation
    traffic_thread = threading.Thread(target=simulate_web_traffic)
    traffic_thread.daemon = True
    traffic_thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
