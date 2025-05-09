from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme


class ScoundrelHighlighter(RegexHighlighter):
    base_style = "scoundrel."
    highlights = [
        r"(?P<heart>\[\u2665 (?:[2-9]|10|[AKQJ])\])",
        r"(?P<diamond>\[\u2666 (?:[2-9]|10|[AKQJ])\])",
        r"(?P<club>\[\u2663 (?:[2-9]|10|[AKQJ])\])",
        r"(?P<spade>\[\u2660 (?:[2-9]|10|[AKQJ])\])",
        r"(?P<placeholder>\[ - \])",
    ]


_scoundrel_theme = Theme(
    {
        "scoundrel.heart": "bold red",
        "scoundrel.diamond": "bold orange1",
        "scoundrel.club": "bold cyan3",
        "scoundrel.spade": "bold blue",
        "scoundrel.placeholder": "grey30",
    }
)


highlighter = ScoundrelHighlighter()

console = Console(highlighter=highlighter, theme=_scoundrel_theme)
