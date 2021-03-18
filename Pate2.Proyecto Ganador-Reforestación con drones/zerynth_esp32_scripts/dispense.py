import streams

streams.serial()

# small hack recommended as alternative to global variables
# https://stackoverflow.com/a/44089781/11326330
class MyVars:
    """
    This holds variables used for dispenser
    """
    dispense_started = False
    seeds_to_dispense = 0

def decrease_seeds_to_dispense():
    # this check is for preventing changing state whenever dispense is not active
    if MyVars.dispense_started:
        MyVars.seeds_to_dispense-=1
        print("Remaining seeds:", MyVars.seeds_to_dispense)
    


pinMode(D4, OUTPUT)
pinMode(D16, OUTPUT)
pinMode(D17, OUTPUT)
pinMode(D5, OUTPUT)

# as documentation says (https://docs.zerynth.com/latest/reference/core/stdlib/docs/builtins/)
# this is an interrupt, so function called should be fast
# also, this is "like a thread running"
pinMode(D23,INPUT_PULLDOWN)
onPinRise(D23,decrease_seeds_to_dispense,debounce=500) # debounce is in millis

pins = [
    D4, D16, D17, D5,
]

steps = [
    [D4],
    [D4, D16],
    [D16],
    [D16, D17],
    [D17],
    [D17, D5],
    [D5],
    [D5, D4],
]


def set_pins_low(pins):
    [digitalWrite(pin, LOW) for pin in pins]

def set_pins_high(pins):
    [digitalWrite(pin, HIGH) for pin in pins]


def seeds(seeds_number):
    """
    Function blocking, dispense seeds up to the required.

    @params seeds_number

    TODO: Stop after time has passed if sensor or motor fails.
    """
    # acquire seeds to dispense
    MyVars.seeds_to_dispense = seeds_number
    MyVars.dispense_started = True

    current_step = 0
    
    # TODO: continue_rotation is for a future implementation for emergency stop
    continue_rotation = True

    print("Dispense started")
    # taken from this blog
    # https://rk.edu.pl/en/zerynth-custom-python-implementation-programming-iot-devices/
    while continue_rotation and MyVars.seeds_to_dispense > 0:
        high_pins = steps[current_step]
        set_pins_low(pins)
        set_pins_high(high_pins)
        current_step += 1
        if current_step == len(steps):
            # reset to continue motion correctly
            current_step = 0
        sleep(2)
    
    # prevent MyVars.seeds_to_dispense decreasing further
    MyVars.dispense_started = False
    pass