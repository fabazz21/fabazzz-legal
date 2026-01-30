"""
Lens Database
24 professional lens models with throw ratios and lens shift
"""

LENS_DATABASE = {
    # ========== PANASONIC ET-D3L SERIES ==========
    "panasonic_et_d3leu100": {
        "name": "ET-D3LEU100",
        "brand": "Panasonic",
        "series": "ET-D3L Series",
        "throw_min": 0.36,
        "throw_max": 0.36,
        "fixed": True,
        "shift_v": 66.0,  # ±66%
        "shift_h": 27.5,  # ±25-30%
        "description": "Ultra Short Throw Fixed"
    },

    "panasonic_et_d3lew200": {
        "name": "ET-D3LEW200",
        "brand": "Panasonic",
        "series": "ET-D3L Series",
        "throw_min": 0.48,
        "throw_max": 0.55,
        "fixed": False,
        "shift_v": 57.0,
        "shift_h": 18.0,
        "description": "Short Throw Zoom"
    },

    "panasonic_et_d3lew60": {
        "name": "ET-D3LEW60",
        "brand": "Panasonic",
        "series": "ET-D3L Series",
        "throw_min": 0.68,
        "throw_max": 0.80,
        "fixed": False,
        "shift_v": 52.0,
        "shift_h": 18.0,
        "description": "Wide Zoom"
    },

    "panasonic_et_d3lew10": {
        "name": "ET-D3LEW10",
        "brand": "Panasonic",
        "series": "ET-D3L Series",
        "throw_min": 1.01,
        "throw_max": 1.30,
        "fixed": False,
        "shift_v": 66.0,
        "shift_h": 24.0,
        "description": "Standard Zoom"
    },

    "panasonic_et_d3les20": {
        "name": "ET-D3LES20",
        "brand": "Panasonic",
        "series": "ET-D3L Series",
        "throw_min": 1.36,
        "throw_max": 1.78,
        "fixed": False,
        "shift_v": 66.0,
        "shift_h": 24.0,
        "description": "Standard Zoom"
    },

    "panasonic_et_d3let80": {
        "name": "ET-D3LET80",
        "brand": "Panasonic",
        "series": "ET-D3L Series",
        "throw_min": 1.81,
        "throw_max": 2.56,
        "fixed": False,
        "shift_v": 66.0,
        "shift_h": 24.0,
        "description": "Long Throw Zoom"
    },

    # ========== PANASONIC ET-D75LE SERIES ==========
    "panasonic_et_d75le6": {
        "name": "ET-D75LE6",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 0.36,
        "throw_max": 0.36,
        "fixed": True,
        "shift_v": 0.0,  # Zero offset
        "shift_h": 0.0,
        "description": "Ultra Short Throw Fixed (Zero Offset)"
    },

    "panasonic_et_d75le8": {
        "name": "ET-D75LE8",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 0.38,
        "throw_max": 0.38,
        "fixed": True,
        "shift_v": 40.0,
        "shift_h": 10.0,
        "description": "Ultra Short Throw Fixed"
    },

    "panasonic_et_d75le10": {
        "name": "ET-D75LE10",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 0.80,
        "throw_max": 1.00,
        "fixed": False,
        "shift_v": 50.0,
        "shift_h": 18.0,
        "description": "Short Throw Zoom"
    },

    "panasonic_et_d75le20": {
        "name": "ET-D75LE20",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 0.97,
        "throw_max": 1.52,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 23.0,
        "description": "Standard Zoom"
    },

    "panasonic_et_d75le30": {
        "name": "ET-D75LE30",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 1.47,
        "throw_max": 2.41,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 23.0,
        "description": "Long Throw Zoom"
    },

    "panasonic_et_d75le40": {
        "name": "ET-D75LE40",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 2.29,
        "throw_max": 3.65,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 23.0,
        "description": "Long Throw Zoom"
    },

    "panasonic_et_d75le50": {
        "name": "ET-D75LE50",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 3.57,
        "throw_max": 5.67,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 23.0,
        "description": "Ultra Long Throw Zoom"
    },

    "panasonic_et_d75le90": {
        "name": "ET-D75LE90",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 5.40,
        "throw_max": 8.61,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 23.0,
        "description": "Ultra Long Throw Zoom"
    },

    "panasonic_et_d75le95": {
        "name": "ET-D75LE95",
        "brand": "Panasonic",
        "series": "ET-D75LE Series",
        "throw_min": 6.01,
        "throw_max": 10.01,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 23.0,
        "description": "Ultra Long Throw Zoom"
    },

    # ========== EPSON LENSES ==========
    "epson_elplx02s": {
        "name": "ELPLX02S",
        "brand": "Epson",
        "series": "ELPL Series",
        "throw_min": 0.35,
        "throw_max": 0.35,
        "fixed": True,
        "shift_v": 0.0,  # Zero offset
        "shift_h": 0.0,
        "description": "UST Zero Offset"
    },

    "epson_elplu03s": {
        "name": "ELPLU03S",
        "brand": "Epson",
        "series": "ELPL Series",
        "throw_min": 0.36,
        "throw_max": 0.36,
        "fixed": True,
        "shift_v": 45.0,
        "shift_h": 0.0,
        "description": "Ultra Short Throw"
    },

    "epson_elplw08": {
        "name": "ELPLW08",
        "brand": "Epson",
        "series": "ELPL Series",
        "throw_min": 0.65,
        "throw_max": 0.78,
        "fixed": False,
        "shift_v": 50.0,
        "shift_h": 10.0,
        "description": "Wide Zoom"
    },

    "epson_elplm15": {
        "name": "ELPLM15",
        "brand": "Epson",
        "series": "ELPL Series",
        "throw_min": 1.44,
        "throw_max": 2.32,
        "fixed": False,
        "shift_v": 65.0,
        "shift_h": 30.0,
        "description": "Middle Throw"
    },

    "epson_elpll08": {
        "name": "ELPLL08",
        "brand": "Epson",
        "series": "ELPL Series",
        "throw_min": 2.22,
        "throw_max": 3.61,
        "fixed": False,
        "shift_v": 65.0,
        "shift_h": 30.0,
        "description": "Long Throw"
    },

    "epson_fixed_st": {
        "name": "Fixed ST",
        "brand": "Epson",
        "series": "Standard",
        "throw_min": 0.80,
        "throw_max": 0.80,
        "fixed": True,
        "shift_v": 40.0,
        "shift_h": 0.0,
        "description": "Short Throw Fixed"
    },

    "epson_short_zoom": {
        "name": "Short Zoom",
        "brand": "Epson",
        "series": "Standard",
        "throw_min": 0.50,
        "throw_max": 0.70,
        "fixed": False,
        "shift_v": 45.0,
        "shift_h": 0.0,
        "description": "Short Zoom"
    },

    # ========== BARCO LENSES ==========
    "barco_r9801814": {
        "name": "R9801814",
        "brand": "Barco",
        "series": "UDX/G62 Lenses",
        "throw_min": 0.36,
        "throw_max": 0.36,
        "fixed": True,
        "shift_v": 50.0,
        "shift_h": 0.0,
        "description": "UST Fixed"
    },

    "barco_r9801815": {
        "name": "R9801815",
        "brand": "Barco",
        "series": "UDX/G62 Lenses",
        "throw_min": 0.75,
        "throw_max": 0.93,
        "fixed": False,
        "shift_v": 55.0,
        "shift_h": 20.0,
        "description": "Short Zoom"
    },

    "barco_r9801816": {
        "name": "R9801816",
        "brand": "Barco",
        "series": "UDX/G62 Lenses",
        "throw_min": 1.13,
        "throw_max": 1.73,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 25.0,
        "description": "Standard Zoom"
    },

    "barco_r9801817": {
        "name": "R9801817",
        "brand": "Barco",
        "series": "UDX/G62 Lenses",
        "throw_min": 1.73,
        "throw_max": 2.89,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 25.0,
        "description": "Long Zoom"
    },

    "barco_r9801818": {
        "name": "R9801818",
        "brand": "Barco",
        "series": "UDX/G62 Lenses",
        "throw_min": 2.90,
        "throw_max": 5.50,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 25.0,
        "description": "Ultra Long Zoom"
    },

    # ========== OPTOMA LENSES ==========
    "optoma_bx_cta21": {
        "name": "BX-CTA21",
        "brand": "Optoma",
        "series": "BX-CTA Series",
        "throw_min": 0.37,
        "throw_max": 0.37,
        "fixed": True,
        "shift_v": 40.0,
        "shift_h": 0.0,
        "description": "UST Fixed"
    },

    "optoma_bx_cta22": {
        "name": "BX-CTA22",
        "brand": "Optoma",
        "series": "BX-CTA Series",
        "throw_min": 0.80,
        "throw_max": 1.03,
        "fixed": False,
        "shift_v": 50.0,
        "shift_h": 20.0,
        "description": "Short Zoom"
    },

    "optoma_bx_cta23": {
        "name": "BX-CTA23",
        "brand": "Optoma",
        "series": "BX-CTA Series",
        "throw_min": 1.22,
        "throw_max": 1.95,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 25.0,
        "description": "Standard Zoom"
    },

    "optoma_bx_cta24": {
        "name": "BX-CTA24",
        "brand": "Optoma",
        "series": "BX-CTA Series",
        "throw_min": 1.87,
        "throw_max": 3.89,
        "fixed": False,
        "shift_v": 60.0,
        "shift_h": 25.0,
        "description": "Long Zoom"
    }
}


def get_lens_by_id(lens_id):
    """Get lens configuration by ID"""
    return LENS_DATABASE.get(lens_id)


def get_all_lenses():
    """Get all lens models"""
    return LENS_DATABASE


def get_lenses_by_brand(brand):
    """Get all lenses from a specific brand"""
    return {k: v for k, v in LENS_DATABASE.items() if v['brand'] == brand}


def get_compatible_lenses(projector_config):
    """Get lenses compatible with a projector"""
    if 'compatible_lenses' not in projector_config:
        return {}

    compatible = {}
    for lens_id in projector_config['compatible_lenses']:
        lens = get_lens_by_id(lens_id)
        if lens:
            compatible[lens_id] = lens

    return compatible


def throw_to_fov(throw_ratio, aspect=16/9):
    """
    Convert throw ratio to vertical field of view (degrees)

    Throw ratio = distance / width
    FOV calculation for vertical FOV:
    hFOV = 2 * atan(1 / (2 * throw_ratio))
    vFOV = 2 * atan(tan(hFOV/2) / aspect)
    """
    import math

    h_fov = 2 * math.atan(1 / (2 * throw_ratio))
    v_fov = 2 * math.atan(math.tan(h_fov / 2) / aspect)

    return math.degrees(v_fov)


def fov_to_throw(fov_degrees, aspect=16/9):
    """
    Convert vertical field of view (degrees) to throw ratio

    Inverse of throw_to_fov
    """
    import math

    v_fov_rad = math.radians(fov_degrees)
    h_fov = 2 * math.atan(math.tan(v_fov_rad / 2) * aspect)
    throw_ratio = 1 / (2 * math.tan(h_fov / 2))

    return throw_ratio
