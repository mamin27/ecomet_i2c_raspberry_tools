import re
import gpiod
from gpiod.line import Direction, Value

BOARD, BCM, OUT, IN, HIGH, LOW = 10, 11, 0, 1, 1, 0
_mode = BOARD
_reqs = {}

BOARD_TO_RK = {
    # zmeň až podľa gpioinfo + reálneho WP vodiča
    26: "GPIO0_B7",
}

_RK = re.compile(r"^GPIO(\d+)_([ABCD])(\d+)$", re.I)

def rk_to_chip_line(name):
    m = _RK.match(str(name).replace(" ", ""))
    if not m:
        raise ValueError("nie RK pin: %s" % name)
    bank = int(m.group(1))
    port = "ABCD".index(m.group(2).upper())
    idx = int(m.group(3))
    if idx > 7:
        raise ValueError(name)
    return "/dev/gpiochip%d" % bank, port * 8 + idx

def _resolve(pin):
    if isinstance(pin, str) and pin.upper().startswith("GPIO"):
        return rk_to_chip_line(pin)
    if pin in BOARD_TO_RK:
        return rk_to_chip_line(BOARD_TO_RK[pin])
    raise ValueError("pin %r nie je GPIO2_A5 ani v BOARD_TO_RK" % pin)

def setmode(mode):
    global _mode
    _mode = mode
    return _mode

def getmode():
    return _mode

def setwarnings(*a, **k):
    pass

def setup(pin, direction, *a, **k):
    path, offset = _resolve(pin)
    if not gpiod.is_gpiochip_device(path):
        raise FileNotFoundError(path)
    req = gpiod.request_lines(
        path,
        consumer="ecomet",
        config={
            offset: gpiod.LineSettings(
                direction=Direction.OUTPUT if direction == OUT else Direction.INPUT,
                output_value=Value.INACTIVE,
            )
        },
    )
    _reqs[pin] = (req, offset)

def output(pin, value):
    req, offset = _reqs[pin]
    req.set_value(offset, Value.ACTIVE if value else Value.INACTIVE)

def input(pin):
    req, offset = _reqs[pin]
    return 1 if req.get_value(offset) == Value.ACTIVE else 0

def cleanup(*a, **k):
    for req, _ in _reqs.values():
        try:
            req.release()
        except Exception:
            pass
    _reqs.clear()
