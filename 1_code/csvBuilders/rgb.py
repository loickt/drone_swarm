from secondary_functiuns import *


def rgb_model(id=0, first_step=0, duration=10, fps=24, folder="example", extension="part1"):
    # 1. Add my specific function parameters to the function signature

    steps = fps * duration
    delta_t = round(duration / steps, 3)
    header = ['Step', 'Id', 'Command', 'X-R-L', 'Y-G', 'Z-B', 'Yaw-Intensity', 'Duration']

    # ----------------2. My specific constants-------------------
    r = 0
    g = 0
    b = 0
    intensity = 1
    duration = 0  # fade duration, 0 for hard
    # -------------------------------------------------------------

    # Do not modify
    if not os.path.exists('../csv/' + folder):
        os.makedirs('../csv/' + folder)
    file = file_name(folder=folder, mode='rgb', drone=id, extension=extension)
    with open('../csv/' + folder + '/' + file, 'w') as file:
        for i in range(len(header) - 1):
            file.write(str(header[i]) + ',')
        file.write(str(header[i + 1]) + '\n')  # prevent the last comma
        for i in range(steps + 1):
            # --------3. Variables dependent on the step------------------
            # Complete without considering offsets
            r = 1
            g = 1
            b = 1
            changed = 1  # set to zero if no change: the step (identical) will not be created
            # -------------------------------------------------------------
            # Do not modify
            if changed:
                changed = 0
                step = [first_step + i, id, "Ring", round(r), round(g), round(b), round(intensity, 3), duration]
                for i in range(len(step) - 1):
                    file.write(str(step[i]) + ',')
                file.write(str(step[i + 1]) + '\n')  # prevent the last comma
        print("Last step: {}".format(first_step + steps))
        return first_step + steps

def rgb_simple(id=0, step=0, folder="example", color="r", intensity=1, extension="part1"):
    header = ['Step', 'Id', 'Command', 'X-R-L', 'Y-G', 'Z-B', 'Yaw-Intensity', 'Duration']

    r = 0
    g = 0
    b = 0

    if not os.path.exists('../2_csv/' + folder):
        os.makedirs('../2_csv/' + folder)
    file = file_name(folder=folder, mode='rgb', drone=id, extension=extension)
    with open('../2_csv/' + folder + '/' + file, 'w') as file:
        for i in range(len(header) - 1):
            file.write(str(header[i]) + ',')
        file.write(str(header[i + 1]) + '\n')
        match color:
            case "r":
                r = 255
            case "g":
                g = 255
            case "b":
                b = 255
            case "w":
                r = 255
                g = 255
                b = 255
        step = [step, id, "Ring", round(r), round(g), round(b), round(intensity, 3), 0]  # It's probably not problematic if it overlaps with the previous fade, but avoid duration>
        for i in range(len(step) - 1):
            file.write(str(step[i]) + ',')
        file.write(str(step[i + 1]) + '\n')  # prevent the last comma

def led_rgb(id=0, first_step=0, duration=10, offset=0, modulo=24, fps=24, folder="example", extension="part1", colors=["r", "g", "b", "w"]):
    steps = fps * duration
    delta_t = round(1 / fps, 3)
    header = ['Step', 'Id', 'Command', 'X-R-L', 'Y-G', 'Z-B', 'Yaw-Intensity', 'Duration']
    r = 0
    g = 0
    b = 0

    # ------------------------------My specific variables-------------------------------------
    # Complete as needed

    index = offset
    intensity = 1
    duration = 0  # fade duration, 0 for hard
    # ---------------------------------------------------------------------------------------------

    # Do not modify
    if not os.path.exists('../2_csv/' + folder):
        os.makedirs('../2_csv/' + folder)
    file = file_name(folder=folder, mode='rgb', drone=id, extension=extension)
    with open('../2_csv/' + folder + '/' + file, 'w') as file:
        for i in range(len(header) - 1):
            file.write(str(header[i]) + ',')
        file.write(str(header[i + 1]) + '\n')
        for i in range(steps + 1):
            # ------------------------------Variables dependent on the step------------------------
            # Complete as needed
            if i % modulo == 0:
                index += 1
                if 'r' in colors[index % len(colors)]:
                    r = 255
                    g = 0
                    b = 0
                elif 'g' in colors[index % len(colors)]:
                    r = 0
                    g = 255
                    b = 0
                elif 'b' in colors[index % len(colors)]:
                    r = 0
                    g = 0
                    b = 255
                elif 'w' in colors[index % len(colors)]:
                    r = 255
                    g = 255
                    b = 255
                changed = 1  # set to zero if no change
            # -------------------------------------------------------------------------------------
            # Do not modify
            if changed:
                changed = 0
                step = [first_step + i, id, "Ring", round(r), round(g), round(b), round(intensity, 3), duration]  # It's probably not problematic if it overlaps with the previous fade, but avoid duration>
                for i in range(len(step) - 1):
                    file.write(str(step[i]) + ',')
                file.write(str(step[i + 1]) + '\n')  # prevent the last comma
        print("Last step: {}".format(first_step + steps))
        return first_step + steps

def rgb_several_drones_sync(nb_drones=3, offset=0, first_id=0, modulo=24, duration=10, first_step=0, folder="example", extension=""):
    for i in range(nb_drones):
        last_step = led_rgb(id=first_id + i, offset=offset, first_step=first_step, duration=duration, modulo=modulo, folder=folder, extension=extension)
    return last_step
