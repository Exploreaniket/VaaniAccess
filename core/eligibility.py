def check_eligibility(profile, scheme):
    """
    Check whether a user's profile satisfies
    the available eligibility conditions of a scheme.

    Returns:
        (is_eligible, reasons)
    """

    reasons = []

    # -----------------------------------
    # Occupation
    # -----------------------------------

    required_occupation = scheme.get("occupation")

    if required_occupation:

        if profile.get("occupation") != required_occupation:
            return False, [
                f"Occupation does not match: "
                f"required {required_occupation}"
            ]

        reasons.append(
            f"Occupation matches: {required_occupation}"
        )

    # -----------------------------------
    # Education
    # -----------------------------------

    required_education = scheme.get("education")

    if required_education:

        if profile.get("education") != required_education:
            return False, [
                f"Education does not match: "
                f"required {required_education}"
            ]

        reasons.append(
            f"Education matches: {required_education}"
        )

    # -----------------------------------
    # Income
    # -----------------------------------

    required_income = scheme.get("income_level")

    if required_income:

        if profile.get("income_level") != required_income:
            return False, [
                f"Income level does not match: "
                f"required {required_income}"
            ]

        reasons.append(
            f"Income level matches: {required_income}"
        )

    # -----------------------------------
    # Minimum Age
    # -----------------------------------

    minimum_age = scheme.get("min_age")

    if minimum_age is not None:

        user_age = profile.get("age")

        if user_age is None:
            return False, [
                f"Age information required "
                f"(minimum age: {minimum_age})"
            ]

        if user_age < minimum_age:
            return False, [
                f"User is below the minimum age of {minimum_age}"
            ]

        reasons.append(
            f"Age requirement satisfied: {minimum_age}+"
        )

    # -----------------------------------
    # Maximum Age
    # -----------------------------------

    maximum_age = scheme.get("max_age")

    if maximum_age is not None:

        user_age = profile.get("age")

        if user_age is None:
            return False, [
                f"Age information required "
                f"(maximum age: {maximum_age})"
            ]

        if user_age > maximum_age:
            return False, [
                f"User is above the maximum age of {maximum_age}"
            ]

        reasons.append(
            f"Age requirement satisfied: <= {maximum_age}"
        )

    # -----------------------------------
    # All available conditions passed
    # -----------------------------------

    return True, reasons