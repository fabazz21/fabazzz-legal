"""
Easing Functions for Timeline Animation
All 12 easing types from the original application
"""

import math


def linear(t):
    """Linear interpolation (no easing)"""
    return t


def ease_in_quad(t):
    """Quadratic ease in"""
    return t * t


def ease_out_quad(t):
    """Quadratic ease out"""
    return t * (2 - t)


def ease_in_out_quad(t):
    """Quadratic ease in/out"""
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t


def ease_in_cubic(t):
    """Cubic ease in"""
    return t * t * t


def ease_out_cubic(t):
    """Cubic ease out"""
    return (--t) * t * t + 1


def ease_in_out_cubic(t):
    """Cubic ease in/out"""
    if t < 0.5:
        return 4 * t * t * t
    return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1


def ease_in_quart(t):
    """Quartic ease in"""
    return t * t * t * t


def ease_out_quart(t):
    """Quartic ease out"""
    return 1 - (--t) * t * t * t


def ease_in_out_quart(t):
    """Quartic ease in/out"""
    if t < 0.5:
        return 8 * t * t * t * t
    return 1 - 8 * (--t) * t * t * t


def ease_in_sine(t):
    """Sinusoidal ease in"""
    return 1 - math.cos(t * math.pi / 2)


def ease_out_sine(t):
    """Sinusoidal ease out"""
    return math.sin(t * math.pi / 2)


def ease_in_out_sine(t):
    """Sinusoidal ease in/out"""
    return -(math.cos(math.pi * t) - 1) / 2


def ease_in_expo(t):
    """Exponential ease in"""
    return 0 if t == 0 else math.pow(2, 10 * (t - 1))


def ease_out_expo(t):
    """Exponential ease out"""
    return 1 if t == 1 else 1 - math.pow(2, -10 * t)


def ease_in_out_expo(t):
    """Exponential ease in/out"""
    if t == 0:
        return 0
    if t == 1:
        return 1
    if t < 0.5:
        return math.pow(2, 20 * t - 10) / 2
    return (2 - math.pow(2, -20 * t + 10)) / 2


def ease_in_circ(t):
    """Circular ease in"""
    return 1 - math.sqrt(1 - t * t)


def ease_out_circ(t):
    """Circular ease out"""
    return math.sqrt(1 - (--t) * t)


def ease_in_out_circ(t):
    """Circular ease in/out"""
    if t < 0.5:
        return (1 - math.sqrt(1 - 4 * t * t)) / 2
    return (math.sqrt(1 - (-2 * t + 2) ** 2) + 1) / 2


def ease_in_back(t):
    """Back ease in (overshoots)"""
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t


def ease_out_back(t):
    """Back ease out (overshoots)"""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * math.pow(t - 1, 3) + c1 * math.pow(t - 1, 2)


def ease_in_out_back(t):
    """Back ease in/out (overshoots)"""
    c1 = 1.70158
    c2 = c1 * 1.525
    if t < 0.5:
        return (math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
    return (math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2


def ease_in_elastic(t):
    """Elastic ease in (spring effect)"""
    c4 = (2 * math.pi) / 3
    if t == 0:
        return 0
    if t == 1:
        return 1
    return -math.pow(2, 10 * t - 10) * math.sin((t * 10 - 10.75) * c4)


def ease_out_elastic(t):
    """Elastic ease out (spring effect)"""
    c4 = (2 * math.pi) / 3
    if t == 0:
        return 0
    if t == 1:
        return 1
    return math.pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1


def ease_in_out_elastic(t):
    """Elastic ease in/out (spring effect)"""
    c5 = (2 * math.pi) / 4.5
    if t == 0:
        return 0
    if t == 1:
        return 1
    if t < 0.5:
        return -(math.pow(2, 20 * t - 10) * math.sin((20 * t - 11.125) * c5)) / 2
    return (math.pow(2, -20 * t + 10) * math.sin((20 * t - 11.125) * c5)) / 2 + 1


def ease_in_bounce(t):
    """Bounce ease in"""
    return 1 - ease_out_bounce(1 - t)


def ease_out_bounce(t):
    """Bounce ease out"""
    n1 = 7.5625
    d1 = 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def ease_in_out_bounce(t):
    """Bounce ease in/out"""
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    return (1 + ease_out_bounce(2 * t - 1)) / 2


# Easing function registry
EASING_FUNCTIONS = {
    'linear': linear,
    'easeInQuad': ease_in_quad,
    'easeOutQuad': ease_out_quad,
    'easeInOutQuad': ease_in_out_quad,
    'easeInCubic': ease_in_cubic,
    'easeOutCubic': ease_out_cubic,
    'easeInOutCubic': ease_in_out_cubic,
    'easeInQuart': ease_in_quart,
    'easeOutQuart': ease_out_quart,
    'easeInOutQuart': ease_in_out_quart,
    'easeInSine': ease_in_sine,
    'easeOutSine': ease_out_sine,
    'easeInOutSine': ease_in_out_sine,
    'easeInExpo': ease_in_expo,
    'easeOutExpo': ease_out_expo,
    'easeInOutExpo': ease_in_out_expo,
    'easeInCirc': ease_in_circ,
    'easeOutCirc': ease_out_circ,
    'easeInOutCirc': ease_in_out_circ,
    'easeInBack': ease_in_back,
    'easeOutBack': ease_out_back,
    'easeInOutBack': ease_in_out_back,
    'easeInElastic': ease_in_elastic,
    'easeOutElastic': ease_out_elastic,
    'easeInOutElastic': ease_in_out_elastic,
    'easeInBounce': ease_in_bounce,
    'easeOutBounce': ease_out_bounce,
    'easeInOutBounce': ease_in_out_bounce,
}


def get_easing_function(name):
    """Get easing function by name"""
    return EASING_FUNCTIONS.get(name, linear)


def get_easing_names():
    """Get list of all easing function names"""
    return list(EASING_FUNCTIONS.keys())
