import json
from pathlib import Path

from core.eligibility import check_eligibility


# ============================================================
# LOAD SCHEMES
# ============================================================

def load_schemes():
    """
    Load schemes from data/schemes.json
    """

    project_root = Path(__file__).resolve().parent.parent

    schemes_file = project_root / "data" / "schemes.json"

    with open(schemes_file, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# CALCULATE MATCH SCORE
# ============================================================

def calculate_match_score(profile, scheme):
    """
    Calculate a match score based on the information
    available in the user's profile.

    Missing information is NOT treated as a mismatch.
    """

    score = 0
    total = 0

    matched = []
    missing = []
    mismatched = []

    # --------------------------------------------------------
    # OCCUPATION
    # --------------------------------------------------------

    required_occupation = scheme.get("occupation")

    if required_occupation:

        total += 1

        user_occupation = profile.get("occupation")

        if user_occupation is None:

            missing.append(
                "Occupation information is missing."
            )

        elif user_occupation == required_occupation:

            score += 1

            matched.append(
                f"Occupation matches: {required_occupation}"
            )

        else:

            mismatched.append(
                "Occupation does not match the scheme."
            )

    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    required_education = scheme.get("education")

    if required_education:

        total += 1

        user_education = profile.get("education")

        if user_education is None:

            missing.append(
                "Education information is missing."
            )

        elif user_education == required_education:

            score += 1

            matched.append(
                f"Education matches: {required_education}"
            )

        else:

            mismatched.append(
                "Education level does not match the scheme."
            )

    # --------------------------------------------------------
    # INCOME
    # --------------------------------------------------------

    required_income = scheme.get("income_level")

    if required_income:

        total += 1

        user_income = profile.get("income_level")

        if user_income is None:

            missing.append(
                "Income information is missing."
            )

        elif user_income == required_income:

            score += 1

            matched.append(
                f"Income category matches: {required_income}"
            )

        else:

            mismatched.append(
                "Income category does not match the scheme."
            )

    # --------------------------------------------------------
    # MINIMUM AGE
    # --------------------------------------------------------

    minimum_age = scheme.get("min_age")

    if minimum_age is not None:

        total += 1

        user_age = profile.get("age")

        if user_age is None:

            missing.append(
                "Age information is missing."
            )

        elif user_age >= minimum_age:

            score += 1

            matched.append(
                f"Age satisfies minimum requirement: {minimum_age}+"
            )

        else:

            mismatched.append(
                f"User must be at least {minimum_age} years old."
            )

    # --------------------------------------------------------
    # MAXIMUM AGE
    # --------------------------------------------------------

    maximum_age = scheme.get("max_age")

    if maximum_age is not None:

        total += 1

        user_age = profile.get("age")

        if user_age is None:

            missing.append(
                "Age information is missing."
            )

        elif user_age <= maximum_age:

            score += 1

            matched.append(
                f"Age is within the maximum limit: {maximum_age}"
            )

        else:

            mismatched.append(
                f"User must be {maximum_age} or younger."
            )

    # --------------------------------------------------------
    # CALCULATE PERCENTAGE
    # --------------------------------------------------------

    if total > 0:

        match_percentage = round(
            (score / total) * 100
        )

    else:

        match_percentage = 0

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if mismatched:

        status = "Not Suitable"

    elif match_percentage >= 80:

        status = "Strong Match"

    elif match_percentage >= 50:

        status = "Potential Match"

    else:

        status = "Needs More Information"

    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {
        "score": match_percentage,
        "status": status,
        "matched": matched,
        "mismatched": mismatched,
        "missing": missing
    }


# ============================================================
# FIND MATCHING SCHEMES
# ============================================================

def find_matching_schemes(profile):
    """
    Find potentially relevant schemes.

    A scheme is rejected only when the user has provided
    information that directly conflicts with its requirements.
    """

    schemes = load_schemes()

    matches = []

    for scheme in schemes:

        result = calculate_match_score(
            profile,
            scheme
        )

        # ----------------------------------------------------
        # Skip schemes with known conflicts
        # ----------------------------------------------------

        if result["status"] == "Not Suitable":
            continue

        matches.append(
            {
                "scheme": scheme,
                "score": result["score"],
                "status": result["status"],
                "matched": result["matched"],
                "mismatched": result["mismatched"],
                "missing": result["missing"]
            }
        )

    # --------------------------------------------------------
    # Highest score first
    # --------------------------------------------------------

    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return matches