from controller import Robot

robot = Robot()

time = int(robot.getBasicTimeStep())

ds = []
ds_names = ["ds_left", "ds_mid", "ds_right"]
ds_val = [0] * len(ds_names)

for name in ds_names:
    ds.append(robot.getDevice(name))
    ds[-1].enable(time)

wheels = []
wheel_names = ["wheel1", "wheel2", "wheel3", "wheel4"]

for name in wheel_names:
    wheels.append(robot.getDevice(name))
    wheels[-1].setPosition(float('inf'))
    wheels[-1].setVelocity(0.0)

last_error = intg = diff = prop = error = 0
kp = 0.05
ki = 0
kd = 0.15
base_speed = 4


def pid(error):
    global last_error, intg, diff, prop, kp, ki, kd

    prop = error
    intg = error + intg
    diff = error - last_error

    balance = (kp * prop) + (ki * intg) + (kd * diff)
    last_error = error

    return balance


def set_speed(base_speed, balance):
    left_speed = base_speed - balance
    right_speed = base_speed + balance

    if left_speed == base_speed or right_speed == base_speed:
        wheels[0].setVelocity(right_speed)
        wheels[1].setVelocity(left_speed)
        wheels[2].setVelocity(right_speed)
        wheels[3].setVelocity(left_speed)

    if left_speed < 0 or right_speed > base_speed:
        wheels[0].setVelocity(0)
        wheels[1].setVelocity(right_speed)
        wheels[2].setVelocity(0)
        wheels[3].setVelocity(right_speed)

    if right_speed < 0 or left_speed > base_speed:
        wheels[0].setVelocity(left_speed)
        wheels[1].setVelocity(0)
        wheels[2].setVelocity(left_speed)
        wheels[3].setVelocity(0)


while robot.step(time) != -1:
    val = 675

    for i in range(len(ds)):
        ds_val[i] = ds[i].getValue()
        print(f"{ds_names[i]}: {ds_val[i]}\n")

    if ds_val[0] < val and ds_val[1] >= val and ds_val[2] < val:
        error = 0
        print("Need to move FORWARD\n" + "*"*40)
    elif ds_val[0] < val and ds_val[1] >= val and ds_val[2] >= val:
        error = -1
        print("Need to move SLIGHTLY RIGHT\n" + "*"*40)
    elif ds_val[0] >= val and ds_val[1] >= val and ds_val[2] < val:
        error = 1
        print("Need to move SLIGHTLY LEFT\n" + "*"*40)
    elif ds_val[0] >= val and ds_val[1] < val and ds_val[2] < val:
        error = 2
        print("Need to move LEFT\n" + "*"*40)
    elif ds_val[0] < val and ds_val[1] < val and ds_val[2] >= val:
        error = -2
        print("Need to move RIGHT\n" + "*"*40)

    set_speed(base_speed, pid(error))

    pass
