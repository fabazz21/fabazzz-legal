"""
Projector Database
18 professional projector models from 4 manufacturers
"""

PROJECTOR_DATABASE = {
    # ========== PANASONIC PT-RQ SERIES ==========
    "panasonic_pt_rq13k": {
        "name": "Panasonic PT-RQ13K",
        "brand": "Panasonic",
        "series": "PT-RQ Series",
        "lumens": 10000,
        "resolution": "5K",
        "resolution_pixels": (5120, 3200),
        "aspect": 16/10,
        "chip_size": '0.9"',
        "type": "3-Chip DLP™",
        "contrast": "10,000:1",
        "weight": 52.0,  # kg
        "dimensions": (550, 290, 700),  # mm (W, H, D)
        "default_lens": "panasonic_et_d3lew10",
        "compatible_lenses": [
            "panasonic_et_d3leu100", "panasonic_et_d3lew200",
            "panasonic_et_d3lew60", "panasonic_et_d3lew10",
            "panasonic_et_d3les20", "panasonic_et_d3let80"
        ]
    },

    "panasonic_pt_rq18k": {
        "name": "Panasonic PT-RQ18K",
        "brand": "Panasonic",
        "series": "PT-RQ Series",
        "lumens": 16000,
        "resolution": "4K",
        "resolution_pixels": (3840, 2400),
        "aspect": 16/10,
        "chip_size": '0.8"',
        "type": "3-Chip DLP™",
        "contrast": "10,000:1",
        "weight": 48.0,
        "dimensions": (550, 270, 650),
        "default_lens": "panasonic_et_d75le20",
        "compatible_lenses": [
            "panasonic_et_d75le6", "panasonic_et_d75le8",
            "panasonic_et_d75le10", "panasonic_et_d75le20",
            "panasonic_et_d75le30", "panasonic_et_d75le40"
        ]
    },

    "panasonic_pt_rq25k": {
        "name": "Panasonic PT-RQ25K",
        "brand": "Panasonic",
        "series": "PT-RQ Series",
        "lumens": 20000,
        "resolution": "4K",
        "resolution_pixels": (3840, 2400),
        "aspect": 16/10,
        "chip_size": '0.8"',
        "type": "3-Chip DLP™",
        "contrast": "10,000:1",
        "weight": 52.0,
        "dimensions": (550, 290, 700),
        "default_lens": "panasonic_et_d75le20",
        "compatible_lenses": [
            "panasonic_et_d75le6", "panasonic_et_d75le8",
            "panasonic_et_d75le10", "panasonic_et_d75le20",
            "panasonic_et_d75le30", "panasonic_et_d75le40"
        ]
    },

    "panasonic_pt_rq35k": {
        "name": "Panasonic PT-RQ35K",
        "brand": "Panasonic",
        "series": "PT-RQ Series",
        "lumens": 30500,
        "resolution": "4K",
        "resolution_pixels": (3840, 2400),
        "aspect": 16/10,
        "chip_size": '0.96"',
        "type": "3-Chip DLP™",
        "contrast": "10,000:1",
        "weight": 62.0,
        "dimensions": (600, 320, 750),
        "default_lens": "panasonic_et_d75le20",
        "compatible_lenses": [
            "panasonic_et_d75le6", "panasonic_et_d75le8",
            "panasonic_et_d75le10", "panasonic_et_d75le20",
            "panasonic_et_d75le30", "panasonic_et_d75le40",
            "panasonic_et_d75le50", "panasonic_et_d75le90"
        ]
    },

    "panasonic_pt_rz24k": {
        "name": "Panasonic PT-RZ24K",
        "brand": "Panasonic",
        "series": "PT-RZ Series",
        "lumens": 20000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.8"',
        "type": "3-Chip DLP™",
        "contrast": "10,000:1",
        "weight": 52.0,
        "dimensions": (550, 290, 700),
        "default_lens": "panasonic_et_d75le20",
        "compatible_lenses": [
            "panasonic_et_d75le6", "panasonic_et_d75le8",
            "panasonic_et_d75le10", "panasonic_et_d75le20",
            "panasonic_et_d75le30", "panasonic_et_d75le40"
        ]
    },

    "panasonic_pt_rz17k": {
        "name": "Panasonic PT-RZ17K",
        "brand": "Panasonic",
        "series": "PT-RZ Series",
        "lumens": 16000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.8"',
        "type": "3-Chip DLP™",
        "contrast": "10,000:1",
        "weight": 48.0,
        "dimensions": (550, 270, 650),
        "default_lens": "panasonic_et_d75le20",
        "compatible_lenses": [
            "panasonic_et_d75le6", "panasonic_et_d75le8",
            "panasonic_et_d75le10", "panasonic_et_d75le20",
            "panasonic_et_d75le30"
        ]
    },

    "panasonic_pt_rz34k": {
        "name": "Panasonic PT-RZ34K",
        "brand": "Panasonic",
        "series": "PT-RZ Series",
        "lumens": 30500,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.96"',
        "type": "3-Chip DLP™",
        "contrast": "10,000:1",
        "weight": 62.0,
        "dimensions": (600, 320, 750),
        "default_lens": "panasonic_et_d75le20",
        "compatible_lenses": [
            "panasonic_et_d75le6", "panasonic_et_d75le8",
            "panasonic_et_d75le10", "panasonic_et_d75le20",
            "panasonic_et_d75le30", "panasonic_et_d75le40",
            "panasonic_et_d75le50", "panasonic_et_d75le90"
        ]
    },

    # ========== EPSON EB SERIES ==========
    "epson_eb_pu2220b": {
        "name": "Epson EB-PU2220B",
        "brand": "Epson",
        "series": "EB-PU Series",
        "lumens": 20000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.76"',
        "type": "3LCD",
        "contrast": "2,500,000:1",
        "weight": 47.0,
        "dimensions": (591, 265, 675),
        "default_lens": "epson_elplm15",
        "compatible_lenses": [
            "epson_elplx02s", "epson_elplu03s",
            "epson_elplw08", "epson_elplm15", "epson_elpll08"
        ]
    },

    "epson_eb_pu2120w": {
        "name": "Epson EB-PU2120W",
        "brand": "Epson",
        "series": "EB-PU Series",
        "lumens": 12000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.76"',
        "type": "3LCD",
        "contrast": "2,500,000:1",
        "weight": 42.0,
        "dimensions": (591, 220, 675),
        "default_lens": "epson_elplm15",
        "compatible_lenses": [
            "epson_elplx02s", "epson_elplu03s",
            "epson_elplw08", "epson_elplm15", "epson_elpll08"
        ]
    },

    "epson_eb_l30000u": {
        "name": "Epson EB-L30000U",
        "brand": "Epson",
        "series": "EB-L Series",
        "lumens": 30000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '1.0"',
        "type": "3LCD Laser",
        "contrast": "2,500,000:1",
        "weight": 75.0,
        "dimensions": (705, 360, 852),
        "default_lens": "epson_elplm15",
        "compatible_lenses": [
            "epson_elplu03s", "epson_elplw08",
            "epson_elplm15", "epson_elpll08"
        ]
    },

    "epson_eb_pq2200b": {
        "name": "Epson EB-PQ2200B",
        "brand": "Epson",
        "series": "EB-PQ Series",
        "lumens": 20000,
        "resolution": "4K",
        "resolution_pixels": (4096, 2160),
        "aspect": 17/9,
        "chip_size": '0.74"',
        "type": "3LCD",
        "contrast": "5,000,000:1",
        "weight": 50.0,
        "dimensions": (591, 290, 675),
        "default_lens": "epson_elplm15",
        "compatible_lenses": [
            "epson_elplx02s", "epson_elplu03s",
            "epson_elplw08", "epson_elplm15", "epson_elpll08"
        ]
    },

    "epson_eb_l630su": {
        "name": "Epson EB-L630SU",
        "brand": "Epson",
        "series": "EB-L Series",
        "lumens": 6000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "3LCD Laser",
        "contrast": "2,500,000:1",
        "weight": 11.8,
        "dimensions": (445, 162, 366),
        "default_lens": "epson_fixed_st",
        "compatible_lenses": ["epson_fixed_st", "epson_short_zoom"]
    },

    "epson_powerlite_l690se": {
        "name": "Epson PowerLite L690SE",
        "brand": "Epson",
        "series": "PowerLite L Series",
        "lumens": 6000,
        "resolution": "WUXGA+",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "3LCD Laser",
        "contrast": "2,500,000:1",
        "weight": 11.8,
        "dimensions": (445, 162, 366),
        "default_lens": "epson_fixed_st",
        "compatible_lenses": ["epson_fixed_st", "epson_short_zoom"]
    },

    # ========== BARCO UDX/G62 SERIES ==========
    "barco_udx_4k32": {
        "name": "Barco UDX-4K32",
        "brand": "Barco",
        "series": "UDX Series",
        "lumens": 31000,
        "resolution": "4K-UHD",
        "resolution_pixels": (3840, 2160),
        "aspect": 16/9,
        "chip_size": '0.9"',
        "type": "3-Chip DLP",
        "contrast": "2,000:1",
        "weight": 60.0,
        "dimensions": (649, 329, 782),
        "default_lens": "barco_r9801816",
        "compatible_lenses": [
            "barco_r9801814", "barco_r9801815",
            "barco_r9801816", "barco_r9801817", "barco_r9801818"
        ]
    },

    "barco_udx_4k26": {
        "name": "Barco UDX-4K26",
        "brand": "Barco",
        "series": "UDX Series",
        "lumens": 26000,
        "resolution": "4K-UHD",
        "resolution_pixels": (3840, 2160),
        "aspect": 16/9,
        "chip_size": '0.9"',
        "type": "3-Chip DLP",
        "contrast": "2,000:1",
        "weight": 58.0,
        "dimensions": (649, 329, 782),
        "default_lens": "barco_r9801816",
        "compatible_lenses": [
            "barco_r9801814", "barco_r9801815",
            "barco_r9801816", "barco_r9801817", "barco_r9801818"
        ]
    },

    "barco_udx_w32": {
        "name": "Barco UDX-W32",
        "brand": "Barco",
        "series": "UDX Series",
        "lumens": 31000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.96"',
        "type": "3-Chip DLP",
        "contrast": "2,000:1",
        "weight": 60.0,
        "dimensions": (649, 329, 782),
        "default_lens": "barco_r9801816",
        "compatible_lenses": [
            "barco_r9801814", "barco_r9801815",
            "barco_r9801816", "barco_r9801817", "barco_r9801818"
        ]
    },

    "barco_g62_w11": {
        "name": "Barco G62-W11",
        "brand": "Barco",
        "series": "G62 Series",
        "lumens": 11000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "1-Chip DLP",
        "contrast": "2,000:1",
        "weight": 25.0,
        "dimensions": (497, 237, 551),
        "default_lens": "barco_r9801816",
        "compatible_lenses": [
            "barco_r9801815", "barco_r9801816", "barco_r9801817"
        ]
    },

    "barco_g62_w14": {
        "name": "Barco G62-W14",
        "brand": "Barco",
        "series": "G62 Series",
        "lumens": 14000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "1-Chip DLP",
        "contrast": "2,000:1",
        "weight": 26.0,
        "dimensions": (497, 237, 551),
        "default_lens": "barco_r9801816",
        "compatible_lenses": [
            "barco_r9801815", "barco_r9801816", "barco_r9801817"
        ]
    },

    # ========== OPTOMA ZU SERIES ==========
    "optoma_zu2200": {
        "name": "Optoma ZU2200",
        "brand": "Optoma",
        "series": "ZU Series",
        "lumens": 22000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "1-Chip DLP",
        "contrast": "2,000:1",
        "weight": 29.0,
        "dimensions": (560, 281, 610),
        "default_lens": "optoma_bx_cta22",
        "compatible_lenses": [
            "optoma_bx_cta21", "optoma_bx_cta22",
            "optoma_bx_cta23", "optoma_bx_cta24"
        ]
    },

    "optoma_zu1700": {
        "name": "Optoma ZU1700",
        "brand": "Optoma",
        "series": "ZU Series",
        "lumens": 17000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "1-Chip DLP",
        "contrast": "2,000:1",
        "weight": 27.0,
        "dimensions": (560, 281, 610),
        "default_lens": "optoma_bx_cta22",
        "compatible_lenses": [
            "optoma_bx_cta21", "optoma_bx_cta22",
            "optoma_bx_cta23", "optoma_bx_cta24"
        ]
    },

    "optoma_zu1300": {
        "name": "Optoma ZU1300",
        "brand": "Optoma",
        "series": "ZU Series",
        "lumens": 13000,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "1-Chip DLP",
        "contrast": "2,000:1",
        "weight": 25.0,
        "dimensions": (560, 281, 610),
        "default_lens": "optoma_bx_cta22",
        "compatible_lenses": [
            "optoma_bx_cta21", "optoma_bx_cta22",
            "optoma_bx_cta23", "optoma_bx_cta24"
        ]
    },

    "optoma_proscene_zu920t": {
        "name": "Optoma ProScene ZU920T",
        "brand": "Optoma",
        "series": "ProScene ZU Series",
        "lumens": 9200,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "1-Chip DLP",
        "contrast": "2,000:1",
        "weight": 22.0,
        "dimensions": (504, 230, 538),
        "default_lens": "optoma_bx_cta22",
        "compatible_lenses": [
            "optoma_bx_cta21", "optoma_bx_cta22",
            "optoma_bx_cta23", "optoma_bx_cta24"
        ]
    },

    "optoma_proscene_zu725t": {
        "name": "Optoma ProScene ZU725T",
        "brand": "Optoma",
        "series": "ProScene ZU Series",
        "lumens": 7500,
        "resolution": "WUXGA",
        "resolution_pixels": (1920, 1200),
        "aspect": 16/10,
        "chip_size": '0.67"',
        "type": "1-Chip DLP",
        "contrast": "2,000:1",
        "weight": 20.0,
        "dimensions": (504, 230, 538),
        "default_lens": "optoma_bx_cta22",
        "compatible_lenses": [
            "optoma_bx_cta21", "optoma_bx_cta22",
            "optoma_bx_cta23", "optoma_bx_cta24"
        ]
    }
}


def get_projector_by_id(projector_id):
    """Get projector configuration by ID"""
    return PROJECTOR_DATABASE.get(projector_id)


def get_all_projectors():
    """Get all projector models"""
    return PROJECTOR_DATABASE


def get_projectors_by_brand(brand):
    """Get all projectors from a specific brand"""
    return {k: v for k, v in PROJECTOR_DATABASE.items() if v['brand'] == brand}


def get_brands():
    """Get list of all brands"""
    brands = set()
    for projector in PROJECTOR_DATABASE.values():
        brands.add(projector['brand'])
    return sorted(list(brands))
