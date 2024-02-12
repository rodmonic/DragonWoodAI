
import random

# Initialize the shared random object
shared_random = random.Random()

def set_seed(seed):
    """Set the seed for the shared random object."""
    shared_random.seed(seed)