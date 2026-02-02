"""
Complete Projector Database - Copied from HTML App
29 professional projector models from 5 manufacturers
All lenses with full lens shift and throw ratio specs
"""

# ============================================================================
# LENS DATABASE
# ============================================================================

LENS_DATABASE = {
    # ========== PANASONIC LENSES ==========
    "ET-D3LEU100": {
        "name": "ET-D3LEU100",
        "brand": "Panasonic",
        "throw_min": 0.36,
        "throw_max": 0.36,
        "fixed": True,
        "shift_v": [-40, 50],  # Vertical shift range in %
        "shift_h": [-15, 15],  # Horizontal shift range in %
    },
    "ET-D3LEW200": {
        "name": "ET-D3LEW200",
        "brand": "Panasonic",
        "throw_min": 0.48,
        "throw_max": 0.55,
        "fixed": False,
        "shift_v": [-66, 66],
        "shift_h": [-24, 24],
    },
    "ET-D3LEW60": {
        "name": "ET-D3LEW60",
        "brand": "Panasonic",
        "throw_min": 0.68,
        "throw_max": 0.80,
        "fixed": False,
        "shift_v": [-66, 66],
        "shift_h": [-24, 24],
    },
    "ET-D75LE6": {
        "name": "ET-D75LE6",
        "brand": "Panasonic",
        "throw_min": 0.90,
        "throw_max": 1.10,
        "fixed": False,
        "shift_v": [-66, 66],
        "shift_h": [-24, 24],
    },
    "ET-D3LEW10": {
        "name": "ET-D3LEW10",
        "brand": "Panasonic",
        "throw_min": 1.01,
        "throw_max": 1.30,
        "fixed": False,
        "shift_v": [-66, 66],
        "shift_h": [-24, 24],
    },
    "ET-D3LES20": {
        "name": "ET-D3LES20",
        "brand": "Panasonic",
        "throw_min": 1.36,
        "throw_max": 1.78,
        "fixed": False,
        "shift_v": [-66, 66],
        "shift_h": [-24, 24],
    },
    "ET-D3LET80": {
        "name": "ET-D3LET80",
        "brand": "Panasonic",
        "throw_min": 1.81,
        "throw_max": 2.56,
        "fixed": False,
        "shift_v": [-66, 66],
        "shift_h": [-24, 24],
    },
    "ET-D75LE95": {
        "name": "ET-D75LE95",
        "brand": "Panasonic",
        "throw_min": 0.80,
        "throw_max": 0.80,
        "fixed": True,
        "shift_v": [-60, 60],
        "shift_h": [-20, 20],
    },

    # ========== CHRISTIE LENSES ==========
    "Christie-UST": {
        "name": "Christie UST",
        "brand": "Christie",
        "throw_min": 0.38,
        "throw_max": 0.38,
        "fixed": True,
        "shift_v": [-50, 50],
        "shift_h": [-20, 20],
    },
    "Christie-0.85-1.02": {
        "name": "Christie 0.85-1.02",
        "brand": "Christie",
        "throw_min": 0.85,
        "throw_max": 1.02,
        "fixed": False,
        "shift_v": [-100, 100],
        "shift_h": [-30, 30],
    },
    "Christie-1.02-1.36": {
        "name": "Christie 1.02-1.36",
        "brand": "Christie",
        "throw_min": 1.02,
        "throw_max": 1.36,
        "fixed": False,
        "shift_v": [-100, 100],
        "shift_h": [-30, 30],
    },
    "Christie-1.22-1.53": {
        "name": "Christie 1.22-1.53",
        "brand": "Christie",
        "throw_min": 1.22,
        "throw_max": 1.53,
        "fixed": False,
        "shift_v": [-100, 100],
        "shift_h": [-30, 30],
    },

    # ========== BARCO LENSES ==========
    "Barco-UST-0.36": {
        "name": "Barco UST 0.36",
        "brand": "Barco",
        "throw_min": 0.36,
        "throw_max": 0.36,
        "fixed": True,
        "shift_v": [-30, 30],
        "shift_h": [-15, 15],
    },
    "Barco-0.75-0.95": {
        "name": "Barco 0.75-0.95",
        "brand": "Barco",
        "throw_min": 0.75,
        "throw_max": 0.95,
        "fixed": False,
        "shift_v": [-120, 120],
        "shift_h": [-40, 40],
    },
    "Barco-1.2-1.5": {
        "name": "Barco 1.2-1.5",
        "brand": "Barco",
        "throw_min": 1.20,
        "throw_max": 1.50,
        "fixed": False,
        "shift_v": [-120, 120],
        "shift_h": [-40, 40],
    },

    # ========== EPSON LENSES (UST) ==========
    "Epson-ELPLX02S": {
        "name": "Epson ELPLX02S (UST)",
        "brand": "Epson",
        "throw_min": 0.35,
        "throw_max": 0.35,
        "fixed": True,
        "shift_v": [-60, 60],
        "shift_h": [-18, 18],
    },
    "Epson-ELPLU03S": {
        "name": "Epson ELPLU03S",
        "brand": "Epson",
        "throw_min": 0.65,
        "throw_max": 0.78,
        "fixed": False,
        "shift_v": [-60, 60],
        "shift_h": [-18, 18],
    },
    "Epson-ELPLS04": {
        "name": "Epson ELPLS04",
        "brand": "Epson",
        "throw_min": 1.44,
        "throw_max": 2.32,
        "fixed": False,
        "shift_v": [-60, 60],
        "shift_h": [-18, 18],
    },
}


# ============================================================================
# PROJECTOR DATABASE
# ============================================================================

PROJECTOR_DATABASE = {
    # ========== PANASONIC PROJECTORS ==========
    "PT-RQ25K": {
        "name": "PT-RQ25K",
        "brand": "Panasonic",
        "lumens": 25000,
        "resolution": "4K",
        "resolution_pixels": (4096, 2160),
        "native_aspect": 16 / 9,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": [
            "ET-D3LEU100", "ET-D3LEW200", "ET-D3LEW60", "ET-D75LE6",
            "ET-D3LEW10", "ET-D3LES20", "ET-D3LET80", "ET-D75LE95",
        ],
    },
    "PT-RQ18K": {
        "name": "PT-RQ18K",
        "brand": "Panasonic",
        "lumens": 18000,
        "resolution": "4K",
        "resolution_pixels": (4096, 2160),
        "native_aspect": 16 / 9,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": [
            "ET-D3LEU100", "ET-D3LEW200", "ET-D3LEW60", "ET-D75LE6",
            "ET-D3LEW10", "ET-D3LES20", "ET-D3LET80",
        ],
    },
    "PT-RQ13K": {
        "name": "PT-RQ13K",
        "brand": "Panasonic",
        "lumens": 13000,
        "resolution": "4K",
        "resolution_pixels": (4096, 2160),
        "native_aspect": 16 / 9,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": [
            "ET-D3LEW60", "ET-D75LE6", "ET-D3LEW10", "ET-D3LES20", "ET-D3LET80",
        ],
    },
    "PT-RZ31K": {
        "name": "PT-RZ31K",
        "brand": "Panasonic",
        "lumens": 31000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": [
            "ET-D3LEU100", "ET-D3LEW200", "ET-D3LEW60", "ET-D75LE6",
            "ET-D3LEW10", "ET-D3LES20", "ET-D3LET80",
        ],
    },
    "PT-RZ21K": {
        "name": "PT-RZ21K",
        "brand": "Panasonic",
        "lumens": 21000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": [
            "ET-D3LEU100", "ET-D3LEW200", "ET-D3LEW60", "ET-D75LE6",
            "ET-D3LEW10", "ET-D3LES20", "ET-D3LET80",
        ],
    },
    "PT-MZ880": {
        "name": "PT-MZ880",
        "brand": "Panasonic",
        "lumens": 8000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": ["ET-D3LEW60", "ET-D3LES20", "ET-D3LET80"],
    },
    "PT-MZ680": {
        "name": "PT-MZ680",
        "brand": "Panasonic",
        "lumens": 6000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": ["ET-D3LEW60", "ET-D3LES20", "ET-D3LET80"],
    },

    # ========== CHRISTIE PROJECTORS ==========
    "HS-P1": {
        "name": "HS-P1",
        "brand": "Christie",
        "lumens": 36500,
        "resolution": "4K",
        "resolution_pixels": (4096, 2400),
        "native_aspect": 1.9,
        "default_lens": "Christie-1.02-1.36",
        "compatible_lenses": [
            "Christie-UST", "Christie-0.85-1.02", "Christie-1.02-1.36", "Christie-1.22-1.53"
        ],
    },
    "Crimson-HD31": {
        "name": "Crimson HD31",
        "brand": "Christie",
        "lumens": 31000,
        "resolution": "HD",
        "resolution_pixels": (1920, 1080),
        "native_aspect": 16 / 9,
        "default_lens": "Christie-1.02-1.36",
        "compatible_lenses": [
            "Christie-0.85-1.02", "Christie-1.02-1.36", "Christie-1.22-1.53"
        ],
    },
    "Crimson-HD25": {
        "name": "Crimson HD25",
        "brand": "Christie",
        "lumens": 25000,
        "resolution": "HD",
        "resolution_pixels": (1920, 1080),
        "native_aspect": 16 / 9,
        "default_lens": "Christie-1.02-1.36",
        "compatible_lenses": [
            "Christie-0.85-1.02", "Christie-1.02-1.36", "Christie-1.22-1.53"
        ],
    },
    "Griffyn-4K32-RGB": {
        "name": "Griffyn 4K32-RGB",
        "brand": "Christie",
        "lumens": 32000,
        "resolution": "4K",
        "resolution_pixels": (4096, 2160),
        "native_aspect": 16 / 9,
        "default_lens": "Christie-1.02-1.36",
        "compatible_lenses": [
            "Christie-UST", "Christie-0.85-1.02", "Christie-1.02-1.36", "Christie-1.22-1.53"
        ],
    },
    "M-4K15-RGB": {
        "name": "M 4K15 RGB",
        "brand": "Christie",
        "lumens": 15000,
        "resolution": "4K",
        "resolution_pixels": (4096, 2160),
        "native_aspect": 16 / 9,
        "default_lens": "Christie-1.02-1.36",
        "compatible_lenses": [
            "Christie-0.85-1.02", "Christie-1.02-1.36", "Christie-1.22-1.53"
        ],
    },
    "M-4K25-RGB": {
        "name": "M 4K25 RGB",
        "brand": "Christie",
        "lumens": 25500,
        "resolution": "4K",
        "resolution_pixels": (4096, 2160),
        "native_aspect": 16 / 9,
        "default_lens": "Christie-1.02-1.36",
        "compatible_lenses": [
            "Christie-UST", "Christie-0.85-1.02", "Christie-1.02-1.36", "Christie-1.22-1.53"
        ],
    },

    # ========== BARCO PROJECTORS ==========
    "D4K40-RGB": {
        "name": "D4K40-RGB",
        "brand": "Barco",
        "lumens": 40000,
        "resolution": "4K",
        "resolution_pixels": (4096, 2160),
        "native_aspect": 16 / 9,
        "default_lens": "Barco-1.2-1.5",
        "compatible_lenses": ["Barco-UST-0.36", "Barco-0.75-0.95", "Barco-1.2-1.5"],
    },
    "UDX-4K32": {
        "name": "UDX-4K32",
        "brand": "Barco",
        "lumens": 32000,
        "resolution": "4K",
        "resolution_pixels": (3840, 2400),
        "native_aspect": 16 / 10,
        "default_lens": "Barco-1.2-1.5",
        "compatible_lenses": ["Barco-0.75-0.95", "Barco-1.2-1.5"],
    },
    "UDX-4K22": {
        "name": "UDX-4K22",
        "brand": "Barco",
        "lumens": 22000,
        "resolution": "4K",
        "resolution_pixels": (3840, 2400),
        "native_aspect": 16 / 10,
        "default_lens": "Barco-1.2-1.5",
        "compatible_lenses": ["Barco-0.75-0.95", "Barco-1.2-1.5"],
    },
    "UDM-4K22": {
        "name": "UDM-4K22",
        "brand": "Barco",
        "lumens": 22000,
        "resolution": "4K",
        "resolution_pixels": (3840, 2160),
        "native_aspect": 16 / 9,
        "default_lens": "Barco-1.2-1.5",
        "compatible_lenses": ["Barco-UST-0.36", "Barco-0.75-0.95", "Barco-1.2-1.5"],
    },
    "UDM-W22": {
        "name": "UDM-W22",
        "brand": "Barco",
        "lumens": 22000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "Barco-1.2-1.5",
        "compatible_lenses": ["Barco-UST-0.36", "Barco-0.75-0.95", "Barco-1.2-1.5"],
    },
    "UDM-W19": {
        "name": "UDM-W19",
        "brand": "Barco",
        "lumens": 19000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "Barco-1.2-1.5",
        "compatible_lenses": ["Barco-0.75-0.95", "Barco-1.2-1.5"],
    },
    "UDM-W15": {
        "name": "UDM-W15",
        "brand": "Barco",
        "lumens": 15000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "Barco-1.2-1.5",
        "compatible_lenses": ["Barco-0.75-0.95", "Barco-1.2-1.5"],
    },

    # ========== EPSON PROJECTORS (INCLUDING UST) ==========
    "EB-PU2220B": {
        "name": "EB-PU2220B",
        "brand": "Epson",
        "lumens": 20000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "Epson-ELPLS04",
        "compatible_lenses": ["Epson-ELPLX02S", "Epson-ELPLU03S", "Epson-ELPLS04"],
    },
    "EB-PU2120W": {
        "name": "EB-PU2120W",
        "brand": "Epson",
        "lumens": 12000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "Epson-ELPLS04",
        "compatible_lenses": ["Epson-ELPLX02S", "Epson-ELPLU03S", "Epson-ELPLS04"],
    },
    "EB-PU1008W": {
        "name": "EB-PU1008W",
        "brand": "Epson",
        "lumens": 8500,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "Epson-ELPLS04",
        "compatible_lenses": ["Epson-ELPLX02S", "Epson-ELPLU03S", "Epson-ELPLS04"],
    },
    "EB-PU1007W": {
        "name": "EB-PU1007W",
        "brand": "Epson",
        "lumens": 7000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "Epson-ELPLS04",
        "compatible_lenses": ["Epson-ELPLU03S", "Epson-ELPLS04"],
    },
    "Pro-L30000U": {
        "name": "Pro L30000U",
        "brand": "Epson",
        "lumens": 30000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "Epson-ELPLS04",
        "compatible_lenses": ["Epson-ELPLX02S", "Epson-ELPLU03S", "Epson-ELPLS04"],
    },

    # ========== DIGITAL PROJECTION ==========
    "Titan-Laser-37000": {
        "name": "Titan Laser 37000",
        "brand": "Digital Projection",
        "lumens": 37000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": ["ET-D3LEW60", "ET-D75LE6", "ET-D3LEW10", "ET-D3LES20", "ET-D3LET80"],
    },
    "Titan-Laser-26000": {
        "name": "Titan Laser 26000",
        "brand": "Digital Projection",
        "lumens": 26000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": ["ET-D3LEW60", "ET-D75LE6", "ET-D3LEW10", "ET-D3LES20", "ET-D3LET80"],
    },
    "M-Vision-21000": {
        "name": "M-Vision 21000",
        "brand": "Digital Projection",
        "lumens": 21000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": ["ET-D3LEW60", "ET-D3LES20", "ET-D3LET80"],
    },
    "E-Vision-15000": {
        "name": "E-Vision 15000",
        "brand": "Digital Projection",
        "lumens": 15000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "native_aspect": 16 / 10,
        "default_lens": "ET-D3LES20",
        "compatible_lenses": ["ET-D3LEW60", "ET-D3LES20", "ET-D3LET80"],
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_brands():
    """Get list of all brands"""
    brands = set()
    for proj in PROJECTOR_DATABASE.values():
        brands.add(proj['brand'])
    return sorted(list(brands))


def get_projectors_by_brand(brand):
    """Get all projectors for a specific brand"""
    return {
        key: value for key, value in PROJECTOR_DATABASE.items()
        if value['brand'] == brand
    }


def get_lenses_by_brand(brand):
    """Get all lenses for a specific brand"""
    return {
        key: value for key, value in LENS_DATABASE.items()
        if value['brand'] == brand
    }


def calculate_fov(throw_ratio):
    """Calculate field of view from throw ratio"""
    import math
    return 2 * math.atan(0.5 / throw_ratio) * (180 / math.pi)


def calculate_throw_ratio(fov):
    """Calculate throw ratio from field of view"""
    import math
    return 0.5 / math.tan((fov * math.pi / 180) / 2)


# Summary
print(f"Loaded {len(PROJECTOR_DATABASE)} projectors from {len(get_brands())} brands")
print(f"Loaded {len(LENS_DATABASE)} lenses")
print(f"Brands: {', '.join(get_brands())}")
