import re
from dataclasses import dataclass

@dataclass
class StrengthResult:
    score: int       # 0-4
    label: str       # Weak / Fair / Moderate / Strong / Very Strong
    color: str       # hex color
    tips: list[str]  # actionable hints

_COMMON = {
    "password", "123456", "qwerty", "abc123", "letmein",
    "monkey", "dragon", "master", "welcome", "login",
    "admin", "passw0rd", "iloveyou", "sunshine", "shadow",
}

def check_strength(pw: str) -> StrengthResult:
    score = 0
    tips: list[str] = []

    # length
    if len(pw) >= 16:
        score += 2
    elif len(pw) >= 10:
        score += 1
    else:
        tips.append("Use at least 10 characters")

    # character variety
    has_lower   = bool(re.search(r"[a-z]", pw))
    has_upper   = bool(re.search(r"[A-Z]", pw))
    has_digit   = bool(re.search(r"\d", pw))
    has_special = bool(re.search(r"[!@#$%^&*()\-_=+]", pw))

    variety = sum([has_lower, has_upper, has_digit, has_special])
    if variety >= 4:
        score += 2
    elif variety >= 3:
        score += 1
    else:
        if not has_upper:   tips.append("Add uppercase letters")
        if not has_digit:   tips.append("Add numbers")
        if not has_special: tips.append("Add symbols (!@#…)")

    # common password check
    if pw.lower() in _COMMON:
        score = 0
        tips = ["This is a very common password — change it"]

    # repeating chars
    if re.search(r"(.)\1{2,}", pw):
        score = max(0, score - 1)
        tips.append("Avoid repeated characters (aaa, 111)")

    # sequential patterns
    if re.search(r"(012|123|234|345|456|567|678|789|abc|bcd|cde|def)", pw.lower()):
        score = max(0, score - 1)
        tips.append("Avoid sequential patterns (123, abc)")

    score = min(score, 4)

    LEVELS = [
        (0, "Weak",        "#E05A5A"),
        (1, "Fair",        "#E09B5A"),
        (2, "Moderate",    "#E0D05A"),
        (3, "Strong",      "#5ABE8A"),
        (4, "Very Strong", "#5A9FBE"),
    ]
    label, color = LEVELS[score][1], LEVELS[score][2]
    return StrengthResult(score=score, label=label, color=color, tips=tips)