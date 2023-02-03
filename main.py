import time
from helpers import screen
from helpers import light
from helpers import color
from dotenv import load_dotenv

load_dotenv()

saturated = False
wait_for_transition=True
current_color = screen.extract_color(saturated)
target_color = current_color

while True:
    target_color = screen.extract_color(saturated)
    if target_color != current_color:
        c_gradient, b_gradient = color.calculate_gradient(target_color, current_color, saturated, 25)
        for i in range(0, len(c_gradient)):
            start = time.time()
            if not wait_for_transition:
                new_target = screen.extract_color(saturated)
                if new_target != target_color:
                    target_color = new_target
                    break
            light.set_color(c_gradient[i], b_gradient[i])
            current_color = c_gradient[i]
            print('color change to', current_color, b_gradient[i], target_color, ' took', time.time() - start, 'seconds')
