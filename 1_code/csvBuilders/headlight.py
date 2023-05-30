from secondary_functiuns import *

def headlight(id=0, first_step=1, duration=10, fps=24, folder="example", extension="part1", modulo=24):
    steps = fps * duration
    delta_t = round(1 / fps, 3)
    header = ['Step', 'Id', 'Command', 'X-R-L', 'Y-G', 'Z-B', 'Yaw-Intensity', 'Duration']
    
    # ------------------------------My specific constants-------------------------------------
    # Complete as needed
    led = 0
    # ---------------------------------------------------------------------------------------
    
    # Do not modify
    if not os.path.exists('../2_csv/' + folder):
        os.makedirs('../2_csv/' + folder)
    file = file_name(folder=folder, mode='headlight', drone=id, extension=extension)
    with open('../2_csv/' + folder + '/' + file, 'w') as file:
        for i in range(len(header) - 1):
            file.write(str(header[i]) + ',')
        file.write(str(header[i + 1]) + '\n')
        for i in range(steps + 1):
            # ------------------------------Variables dependent on the step------------------------
            # Complete as needed
            if i % modulo == 0:
                led = 1 - led  # 1 for on, 0 for off
                changed = 1  # set to zero if no change
            duration = 0  # duration of the lighting (unused if led=0), set to 0 to turn on without time limit
            # -------------------------------------------------------------------------------------
            
            # Do not modify
            if changed:
                changed = 0
                step = [first_step + i, id, "Headlight", led, 0, 0, 0, duration]
                for i in range(len(step) - 1):
                    file.write(str(step[i]) + ',')
                file.write(str(step[i + 1]) + '\n')  # prevent the last comma
        print("Last step: {}".format(first_step + steps))
        return first_step + steps


def simple_frontal_led(id=0, step=0, state=1, folder="example", extension="part1"):
    header = ['Step', 'Id', 'Command', 'X-R-L', 'Y-G', 'Z-B', 'Yaw-Intensity', 'Duration']

    if not os.path.exists('../2_csv/' + folder):
        os.makedirs('../2_csv/' + folder)
    file = file_name(folder=folder, mode='headlight', drone=id, extension=extension)
    with open('../2_csv/' + folder + '/' + file, 'w') as file:
        for i in range(len(header) - 1):
            file.write(str(header[i]) + ',')
        file.write(str(header[i + 1]) + '\n')

        step = [step, id, "Headlight", state, 0, 0, 0, 0]
        for i in range(len(step) - 1):
            file.write(str(step[i]) + ',')
        file.write(str(step[i + 1]) + '\n')
