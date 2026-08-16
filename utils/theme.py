PARASITE_COLORS = {
    "Ancylostoma caninum": "#E63946",
    "Toxocara canis": "#457B9D",
    "Giardia intestinalis": "#2A9D8F",
    "Trichuris vulpis": "#E9C46A",
}

PARASITE_NAMES = list(PARASITE_COLORS.keys())


def italicize(name: str, mode: str = "html") -> str:
    """Wrap parasite names in italic tags. mode='html' for Plotly, 'md' for Streamlit markdown."""
    if mode == "html":
        return f"<i>{name}</i>" if name in PARASITE_NAMES else name
    return f"*{name}*" if name in PARASITE_NAMES else name


# Pre-built color maps with italic keys for Plotly
PARASITE_COLORS_ITALIC = {italicize(k): v for k, v in PARASITE_COLORS.items()}

POSITIVE_COLOR = "#E63946"
NEGATIVE_COLOR = "#A8DADC"
AVERAGE_LINE_COLOR = "#264653"

PAGE_ICON = "🔬"
PAGE_TITLE = "Parásitos Zoonóticos - Valle del Aburrá"
