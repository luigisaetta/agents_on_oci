"""
Provide notification from backend in a queue
"""

# notification_queue.py
import queue

# Create a global in-memory queue
notification_queue = queue.Queue()


def send_notification(message, level="info"):
    """Send a notification message to the queue."""
    notification_queue.put((message, level))
