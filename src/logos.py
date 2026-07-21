"""
Team Logo Provider for Hockey Analytics Dashboard.
Provides reliable CDN image URLs and primary team colors for NHL teams.
"""

TEAM_LOGOS = {
    "Boston Bruins": "https://assets.nhle.com/logos/nhl/svg/BOS_light.svg",
    "Buffalo Sabres": "https://assets.nhle.com/logos/nhl/svg/BUF_light.svg",
    "Calgary Flames": "https://assets.nhle.com/logos/nhl/svg/CGY_light.svg",
    "Chicago Blackhawks": "https://assets.nhle.com/logos/nhl/svg/CHI_light.svg",
    "Colorado Avalanche": "https://assets.nhle.com/logos/nhl/svg/COL_light.svg",
    "Dallas Stars": "https://assets.nhle.com/logos/nhl/svg/DAL_light.svg",
    "Detroit Red Wings": "https://assets.nhle.com/logos/nhl/svg/DET_light.svg",
    "Edmonton Oilers": "https://assets.nhle.com/logos/nhl/svg/EDM_light.svg",
    "Florida Panthers": "https://assets.nhle.com/logos/nhl/svg/FLA_light.svg",
    "Los Angeles Kings": "https://assets.nhle.com/logos/nhl/svg/LAK_light.svg",
    "Minnesota Wild": "https://assets.nhle.com/logos/nhl/svg/MIN_light.svg",
    "Montreal Canadiens": "https://assets.nhle.com/logos/nhl/svg/MTL_light.svg",
    "Nashville Predators": "https://assets.nhle.com/logos/nhl/svg/NSH_light.svg",
    "New Jersey Devils": "https://assets.nhle.com/logos/nhl/svg/NJD_light.svg",
    "New York Islanders": "https://assets.nhle.com/logos/nhl/svg/NYI_light.svg",
    "New York Rangers": "https://assets.nhle.com/logos/nhl/svg/NYR_light.svg",
    "Ottawa Senators": "https://assets.nhle.com/logos/nhl/svg/OTT_light.svg",
    "Philadelphia Flyers": "https://assets.nhle.com/logos/nhl/svg/PHI_light.svg",
    "Phoenix Coyotes": "https://assets.nhle.com/logos/nhl/svg/ARI_light.svg",
    "Arizona Coyotes": "https://assets.nhle.com/logos/nhl/svg/ARI_light.svg",
    "Pittsburgh Penguins": "https://assets.nhle.com/logos/nhl/svg/PIT_light.svg",
    "San Jose Sharks": "https://assets.nhle.com/logos/nhl/svg/SJS_light.svg",
    "St. Louis Blues": "https://assets.nhle.com/logos/nhl/svg/STL_light.svg",
    "Tampa Bay Lightning": "https://assets.nhle.com/logos/nhl/svg/TBL_light.svg",
    "Toronto Maple Leafs": "https://assets.nhle.com/logos/nhl/svg/TOR_light.svg",
    "Vancouver Canucks": "https://assets.nhle.com/logos/nhl/svg/VAN_light.svg",
    "Washington Capitals": "https://assets.nhle.com/logos/nhl/svg/WSH_light.svg",
    "Winnipeg Jets": "https://assets.nhle.com/logos/nhl/svg/WPG_light.svg",
    "Carolina Hurricanes": "https://assets.nhle.com/logos/nhl/svg/CAR_light.svg",
    "Anaheim Ducks": "https://assets.nhle.com/logos/nhl/svg/ANA_light.svg",
    "Mighty Ducks of Anaheim": "https://assets.nhle.com/logos/nhl/svg/ANA_light.svg",
    "Columbus Blue Jackets": "https://assets.nhle.com/logos/nhl/svg/CBJ_light.svg",
    "Atlanta Thrashers": "https://cdn.freebiesupply.com/logos/large/2x/atlanta-thrashers-logo-png-transparent.png"
}

TEAM_COLORS = {
    "Anaheim Ducks": "#F47A38",
    "Mighty Ducks of Anaheim": "#004B49",
    "Arizona Coyotes": "#8C2633",
    "Phoenix Coyotes": "#8C2633",
    "Atlanta Thrashers": "#5C768D",
    "Boston Bruins": "#FFB81C",
    "Buffalo Sabres": "#002654",
    "Calgary Flames": "#C8102E",
    "Carolina Hurricanes": "#CC0000",
    "Chicago Blackhawks": "#CF0A2C",
    "Colorado Avalanche": "#6F263D",
    "Columbus Blue Jackets": "#002654",
    "Dallas Stars": "#006847",
    "Detroit Red Wings": "#CE1126",
    "Edmonton Oilers": "#FF4C00",
    "Florida Panthers": "#041E42",
    "Hartford Whalers": "#008000",
    "Los Angeles Kings": "#111111",
    "Minnesota North Stars": "#008000",
    "Minnesota Wild": "#154734",
    "Montreal Canadiens": "#AF1E2D",
    "Nashville Predators": "#FFB81C",
    "New Jersey Devils": "#CE1126",
    "New York Islanders": "#00539B",
    "New York Rangers": "#0038A8",
    "Ottawa Senators": "#DA1A32",
    "Philadelphia Flyers": "#F47D30",
    "Pittsburgh Penguins": "#FCB514",
    "Quebec Nordiques": "#00539B",
    "San Jose Sharks": "#006D75",
    "St. Louis Blues": "#002F87",
    "Tampa Bay Lightning": "#002868",
    "Toronto Maple Leafs": "#00205B",
    "Vancouver Canucks": "#00205B",
    "Vegas Golden Knights": "#B4975A",
    "Washington Capitals": "#041E42",
    "Winnipeg Jets": "#041E42"
}

DEFAULT_LOGO = "https://assets.nhle.com/logos/nhl/svg/NHL_light.svg"

def get_team_logo(team_name: str) -> str:
    """Returns the SVG/PNG logo URL for a given team name."""
    return TEAM_LOGOS.get(team_name, DEFAULT_LOGO)

def get_team_color(team_name: str, fallback_color: str = "#38BDF8") -> str:
    """Returns primary team color hex code."""
    return TEAM_COLORS.get(team_name, fallback_color)
