import time
from helpers import screen
from helpers import light
from helpers import color
from dotenv import load_dotenv, find_dotenv
from queue import Queue
from threading import Thread
from pathlib import Path

load_dotenv()

saturated = False
wait_for_transition=False

# A thread that produces data
def producer(out_q: Queue):
    current_color = screen.extract_color(saturated)
    while True:
        target_color = screen.extract_color(saturated)
        if current_color != target_color:
            out_q.put(target_color)
            current_color = target_color
          
# A thread that consumes data
def consumer(in_q: Queue):
    current_color = screen.extract_color(saturated)
    while True:
        target_color = in_q.get()
        if target_color != current_color:
            c_gradient, b_gradient = color.calculate_gradient(target_color, current_color, saturated, 25)
            for i in range(0, len(c_gradient)):
                start = time.time()
                if not wait_for_transition:
                    new_target = in_q.queue[0] if in_q.qsize() > 0 else None
                    if new_target != None and new_target != target_color:
                        target_color = new_target
                        print('switching target')
                        break
                light.set_color(c_gradient[i], b_gradient[i])
                print('color change from', color.to_terminal_color(current_color), 'to', color.to_terminal_color(target_color), b_gradient[i], ' took', time.time() - start, 'seconds')
                current_color = c_gradient[i]

# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target = consumer, args =(q, ))
t2 = Thread(target = producer, args =(q, ))
t1.start()
t2.start()
