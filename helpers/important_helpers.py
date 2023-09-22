import random

NAMES = [
    "Sol",
    "Helios",
    "Ra",
    "Apollo",
    "Amaterasu",
    "Surya",
    "Huitzilopochtli",
    "Utu",
    "Savitar",
    "Inti",
    "Shamash",
    "Aten",
    "Dazhbog",
    "Mithra",
    "Lugh",
    "Hyperion",
    "Igaluk",
    "Nyame",
    "Tsohanoai",
    "Maui",
    "Xihe",
    "Tonatiuh",
    "Horus",
    "Adonis",
    "Belenus",
    "Hvar Khshaita",
    "Arinna",
    "Malina",
    "Surtr",
    "Oshunmare",
    "Saule",
    "Soorej",
    "Amun-Ra",
    "Khepri",
    "Liza",
    "Tsukuyomi",
    "Marici",
    "Atum",
    "Janus",
    "Solntse",
    "Elagabalus",
    "Malakbel",
    "Liza",
    "Atar",
    "Svarog",
    "Pawahtun",
    "Haikili",
    "Elatha",
    "Bel"
    "Lelantos",
    "Caprisun",
    "Sunny",
    "cprogrammer1994"
]

TITLES = [
    "Sunbringer",
    "Dawnbringer",
    "Radiant One",
    "Lightbearer",
    "Solar King",
    "Daystar",
    "Sunlord",
    "Sunbeam Sovereign",
    "Illuminator",
    "Luminous God",
    "Daybringer",
    "Sunfire Guardian",
    "Sunweaver",
    "Celestial Ruler",
    "Golden Guardian",
    "Beacon of Light",
    "Solar Emperor",
    "Dawnbreaker",
    "Sun Herald",
    "Resplendent One",
    "Brilliance Incarnate",
    "Solar Deity",
    "Daymaker",
    "Sunforged",
    "Luminary Monarch",
    "Radiance Wielder",
    "Solar Luminaire",
    "Sunstone Sentinel",
    "Emissary of Light",
    "Sunburst Sovereign",
    "Daylight Champion",
    "Sun Guardian",
    "Lightbringer King",
    "Sunburst Savior",
    "Dawnbearer of Hope",
    "Solar Radiator",
    "Beacon of Radiance",
    "Daystar Monarch",
    "Solaris Supreme",
    "Dawn Herald",
    "Sunforged Guardian",
    "Golden Conqueror",
    "Celestial Sovereign",
    "Illuminated One",
    "Luminous Leader",
    "Sun Incarnate",
    "Daybreak Guardian",
    "Sun Seraph",
    "Radiant Ruler",
    "Sun King",
    "Pyweek destroyer",
    "The Shiny"
]


def get_boss_name():
    return "{} ({})".format(random.choice(NAMES), random.choice(TITLES))

