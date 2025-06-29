import json
import logging
import time
import random
from datetime import datetime

# Configure structured logging
class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        # Add custom fields if they exist
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'duration'):
            log_entry['duration'] = record.duration
        return json.dumps(log_entry)

# Set up logger
logger = logging.getLogger('demo-app')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(StructuredFormatter())
logger.addHandler(handler)

def simulate_user_actions():
    """Simulate user actions with structured logging"""
    actions = ['login', 'view_product', 'add_to_cart', 'checkout', 'logout']
    while True:
        user_id = f"user_{random.randint(1, 1000)}"
        request_id = f"req_{random.randint(10000, 99999)}"
        action = random.choice(actions)
        duration = random.uniform(0.1, 3.0)
        # Log with structured data
        logger.info(f"User action: {action}", extra={
            'user_id': user_id,
            'request_id': request_id,
            'duration': duration,
            'action': action
        })
        # Occasionally log errors
        if random.random() < 0.1:
            logger.error(f"Error during {action}", extra={
                'user_id': user_id,
                'request_id': request_id,
                'error_type': 'timeout',
                'action': action
            })
        time.sleep(random.uniform(1, 3))

if __name__ == '__main__':
    simulate_user_actions()