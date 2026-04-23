"""Channel name mappings for German TV."""

# Public broadcasters (Öffentlich-Rechtliche)
PUBLIC_CHANNELS = [
    "Das Erste",
    "ZDF",
    "3sat",
    "arte",
    "PHOENIX",
    "KiKA",
    "ZDFneo",
    "ZDFinfo",
    "ONE",
    "tagesschau24",
    "ARD alpha",
    "NDR",
    "WDR",
    "SWR",
    "BR",
    "HR",
    "MDR",
    "RBB",
    "SR",
    "Radio Bremen TV",
]

# Commercial channels (Private)
COMMERCIAL_CHANNELS = [
    "RTL",
    "SAT.1",
    "ProSieben",
    "VOX",
    "kabel eins",
    "RTL II",
    "SUPER RTL",
    "NITRO",
    "RTLplus",
    "SAT.1 Gold",
    "ProSieben MAXX",
    "sixx",
    "kabel eins Doku",
    "TELE 5",
    "DMAX",
    "TLC",
    "Welt",
    "N-TV",
    "SPORT1",
]

ALL_CHANNELS = PUBLIC_CHANNELS + COMMERCIAL_CHANNELS

# Mapping from common MagentaTV names to display names
CHANNEL_NAME_ALIASES = {
    "ard": "Das Erste",
    "das erste": "Das Erste",
    "zdf": "ZDF",
    "arte": "arte",
    "3sat": "3sat",
    "phoenix": "PHOENIX",
    "kika": "KiKA",
    "zdfneo": "ZDFneo",
    "zdfinfo": "ZDFinfo",
    "one": "ONE",
    "tagesschau24": "tagesschau24",
    "ard alpha": "ARD alpha",
    "alpha": "ARD alpha",
    "ndr": "NDR",
    "wdr": "WDR",
    "swr": "SWR",
    "br": "BR",
    "hr": "HR",
    "mdr": "MDR",
    "rbb": "RBB",
    "sr": "SR",
    "rtl": "RTL",
    "sat.1": "SAT.1",
    "sat1": "SAT.1",
    "prosieben": "ProSieben",
    "pro7": "ProSieben",
    "vox": "VOX",
    "kabel eins": "kabel eins",
    "kabeleins": "kabel eins",
    "rtl2": "RTL II",
    "rtl ii": "RTL II",
    "super rtl": "SUPER RTL",
    "nitro": "NITRO",
    "rtlplus": "RTLplus",
    "sat.1 gold": "SAT.1 Gold",
    "prosieben maxx": "ProSieben MAXX",
    "pro7 maxx": "ProSieben MAXX",
    "sixx": "sixx",
    "kabel eins doku": "kabel eins Doku",
    "tele 5": "TELE 5",
    "tele5": "TELE 5",
    "dmax": "DMAX",
    "tlc": "TLC",
    "welt": "Welt",
    "n-tv": "N-TV",
    "ntv": "N-TV",
    "sport1": "SPORT1",
}


def normalize_channel_name(name: str) -> str:
    """Normalize a channel name to its canonical display form."""
    if not name:
        return name
    lower = name.strip().lower()
    return CHANNEL_NAME_ALIASES.get(lower, name.strip())
