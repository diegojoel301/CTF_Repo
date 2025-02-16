import random
import sys

# define RAND_MAX
RAND_MAX = 40538974999

random.seed(0x67a69e90)

print(random.randint(1, RAND_MAX))