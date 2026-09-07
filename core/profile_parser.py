import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# EMPTY PROFILE
# ============================================================

def create_empty_profile():
    return {
        "age": None,
        "occupation": None,
        "education": None,
        "income_level": None,
        "location": None
    }


# ============================================================
# VALIDATE PROFILE
# ============================================================

def validate_profile(profile):
    """
    Make sure the profile contains only the fields
    expected by the eligibility engine.
    """

    clean_profile = create_empty_profile()

    if not isinstance(profile, dict):
        return clean_profile

    # Age
    age = profile.get("age")

    if isinstance(age, int):
        if 0 < age < 120:
            clean_profile["age"] = age

    elif isinstance(age, str):
        age_match = re.search(r"\d{1,3}", age)

        if age_match:
            age_value = int(age_match.group())

            if 0 < age_value < 120:
                clean_profile["age"] = age_value

    # Occupation
    occupation = profile.get("occupation")

    if isinstance(occupation, str):
        occupation = occupation.lower().strip()

        allowed_occupations = [
            "student",
            "farmer",
            "senior_citizen"
        ]

        if occupation in allowed_occupations:
            clean_profile["occupation"] = occupation

    # Education
    education = profile.get("education")

    if isinstance(education, str):
        education = education.lower().strip()

        allowed_education = [
            "school",
            "undergraduate",
            "graduate",
            "postgraduate"
        ]

        if education in allowed_education:
            clean_profile["education"] = education

    # Income
    income = profile.get("income_level")

    if isinstance(income, str):
        income = income.lower().strip()

        allowed_income = [
            "low",
            "middle",
            "high"
        ]

        if income in allowed_income:
            clean_profile["income_level"] = income

    # Location
    location = profile.get("location")

    if isinstance(location, str):
        location = location.strip()

        if location:
            clean_profile["location"] = location

    return clean_profile


# ============================================================
# LOCAL PROFILE PARSER
# ============================================================

def local_profile_parser(text):
    """
    Local fallback parser.

    This is used when Gemini is unavailable or unable
    to understand the input.

    Supports:
    - English
    - Hinglish
    - Hindi
    """

    profile = create_empty_profile()

    if not text:
        return profile

    text_lower = text.lower().strip()

    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    age_patterns = [
        r"\b(\d{1,3})\s*(?:years?|year)\b",
        r"\b(\d{1,3})\s*(?:saal)\b",
        r"\b(\d{1,3})\s*(?:वर्ष|साल)\b"
    ]

    for pattern in age_patterns:

        age_match = re.search(pattern, text_lower)

        if age_match:
            age = int(age_match.group(1))

            if 0 < age < 120:
                profile["age"] = age

            break

    # --------------------------------------------------------
    # OCCUPATION - STUDENT
    # --------------------------------------------------------

    student_keywords = [
        "student",
        "college student",
        "school student",
        "undergraduate",
        "studying",
        "college",
        "स्टूडेंट",
        "छात्र",
        "छात्रा",
        "विद्यार्थी",
        "कॉलेज",
        "पढ़ाई",
        "पढ़ रहा",
        "पढ़ रही",
        "पढ़ता",
        "पढ़ती"
    ]

    if any(keyword in text_lower for keyword in student_keywords):
        profile["occupation"] = "student"

    # --------------------------------------------------------
    # OCCUPATION - FARMER
    # --------------------------------------------------------

    farmer_keywords = [
        "farmer",
        "agriculture",
        "agricultural",
        "farming",
        "किसान",
        "खेती",
        "कृषक"
    ]

    if any(keyword in text_lower for keyword in farmer_keywords):
        profile["occupation"] = "farmer"

    # --------------------------------------------------------
    # OCCUPATION - SENIOR CITIZEN
    # --------------------------------------------------------

    senior_keywords = [
        "senior citizen",
        "senior_citizen",
        "elderly",
        "old person",
        "वरिष्ठ नागरिक",
        "बुजुर्ग",
        "वृद्ध"
    ]

    if any(keyword in text_lower for keyword in senior_keywords):
        profile["occupation"] = "senior_citizen"

    # --------------------------------------------------------
    # EDUCATION - UNDERGRADUATE
    # --------------------------------------------------------

    undergraduate_keywords = [
        "undergraduate",
        "graduation",
        "graduate",
        "college",
        "college student",
        "bachelor",
        "btech",
        "b.tech",
        "be ",
        "b.sc",
        "bsc",
        "b.com",
        "bcom",
        "ba ",
        "graduating",
        "graduation kar",
        "graduation kar raha",
        "graduation kar rahi",
        "ग्रेजुएशन",
        "स्नातक",
        "कॉलेज",
        "कॉलेज में",
        "स्नातक कर",
        "स्नातक की पढ़ाई"
    ]

    if any(keyword in text_lower for keyword in undergraduate_keywords):
        profile["education"] = "undergraduate"

    # --------------------------------------------------------
    # EDUCATION - SCHOOL
    # --------------------------------------------------------

    school_keywords = [
        "school",
        "school student",
        "class 10",
        "class 12",
        "10th",
        "12th",
        "tenth",
        "twelfth",
        "स्कूल",
        "स्कूली",
        "10वीं",
        "12वीं",
        "दसवीं",
        "बारहवीं"
    ]

    if any(keyword in text_lower for keyword in school_keywords):
        profile["education"] = "school"

    # --------------------------------------------------------
    # EDUCATION - POSTGRADUATE
    # --------------------------------------------------------

    postgraduate_keywords = [
        "postgraduate",
        "post graduate",
        "masters",
        "master's",
        "mtech",
        "m.tech",
        "m.sc",
        "msc",
        "m.com",
        "mcom",
        "mba",
        "एमटेक",
        "मास्टर्स",
        "स्नातकोत्तर"
    ]

    if any(keyword in text_lower for keyword in postgraduate_keywords):
        profile["education"] = "postgraduate"

    # --------------------------------------------------------
    # INCOME - LOW
    # --------------------------------------------------------

    low_income_keywords = [
        "low income",
        "income is low",
        "income low",
        "income kam",
        "income bahut kam",
        "income bohot kam",
        "income बहुत कम",
        "कम income",
        "कम इनकम",
        "इनकम कम",
        "इनकम बहुत कम",
        "income कम",
        "low earning",
        "financially weak",
        "poor family",
        "poor income",
        "कम आय",
        "आय कम",
        "आय बहुत कम",
        "कम आमदनी",
        "आमदनी कम",
        "आमदनी बहुत कम",
        "गरीब परिवार",
        "आर्थिक रूप से कमजोर",
        "कम कमाई"
    ]

    if any(keyword in text_lower for keyword in low_income_keywords):
        profile["income_level"] = "low"

    # --------------------------------------------------------
    # INCOME - HIGH
    # --------------------------------------------------------

    high_income_keywords = [
        "high income",
        "income is high",
        "income high",
        "income zyada",
        "income jyada",
        "income bahut zyada",
        "high earning",
        "rich family",
        "उच्च आय",
        "आय ज्यादा",
        "आय अधिक",
        "इनकम ज्यादा",
        "इनकम अधिक",
        "ज्यादा कमाई"
    ]

    if any(keyword in text_lower for keyword in high_income_keywords):
        profile["income_level"] = "high"

    # --------------------------------------------------------
    # INCOME - MIDDLE
    # --------------------------------------------------------

    middle_income_keywords = [
        "middle income",
        "middle class",
        "average income",
        "medium income",
        "मध्यम आय",
        "मध्यम वर्ग",
        "मिडिल क्लास"
    ]

    if any(keyword in text_lower for keyword in middle_income_keywords):
        profile["income_level"] = "middle"

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    indian_states = {
        "andhra pradesh": "Andhra Pradesh",
        "arunachal pradesh": "Arunachal Pradesh",
        "assam": "Assam",
        "bihar": "Bihar",
        "chhattisgarh": "Chhattisgarh",
        "goa": "Goa",
        "gujarat": "Gujarat",
        "haryana": "Haryana",
        "himachal pradesh": "Himachal Pradesh",
        "jharkhand": "Jharkhand",
        "karnataka": "Karnataka",
        "kerala": "Kerala",
        "madhya pradesh": "Madhya Pradesh",
        "maharashtra": "Maharashtra",
        "manipur": "Manipur",
        "meghalaya": "Meghalaya",
        "mizoram": "Mizoram",
        "nagaland": "Nagaland",
        "odisha": "Odisha",
        "punjab": "Punjab",
        "rajasthan": "Rajasthan",
        "sikkim": "Sikkim",
        "tamil nadu": "Tamil Nadu",
        "telangana": "Telangana",
        "tripura": "Tripura",
        "uttar pradesh": "Uttar Pradesh",
        "uttarakhand": "Uttarakhand",
        "west bengal": "West Bengal",
        "delhi": "Delhi"
    }

    for state_key, state_name in indian_states.items():

        if state_key in text_lower:
            profile["location"] = state_name
            break

    return validate_profile(profile)


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    try:
        client = genai.Client(api_key=api_key)
        return client

    except Exception:
        return None


# ============================================================
# GEMINI PROFILE PARSER
# ============================================================

def gemini_profile_parser(text):

    client = get_gemini_client()

    if client is None:
        return None

    prompt = f"""
You are a profile extraction system for an Indian government scheme
recommendation application.

The user may speak in:
- Hindi
- English
- Hinglish
- Hindi written in Devanagari
- Hindi written using English letters

Extract ONLY the following information:

1. age
2. occupation
3. education
4. income_level
5. location

Allowed values:

occupation:
- student
- farmer
- senior_citizen

education:
- school
- undergraduate
- graduate
- postgraduate

income_level:
- low
- middle
- high

If information is not available, use null.

Important interpretation rules:

- "college student" usually means occupation = student
- "graduation kar raha hoon" means education = undergraduate
- "graduation kar rahi hoon" means education = undergraduate
- "college mein padh raha hoon" means education = undergraduate
- "college student hoon" means education = undergraduate
- "इनकम बहुत कम है" means income_level = low
- "इनकम कम है" means income_level = low
- "आय बहुत कम है" means income_level = low
- "आमदनी कम है" means income_level = low
- "कम आय" means income_level = low
- "गरीब परिवार" means income_level = low

Return ONLY valid JSON.

Required JSON format:

{{
    "age": null,
    "occupation": null,
    "education": null,
    "income_level": null,
    "location": null
}}

User statement:
{text}
"""

    # --------------------------------------------------------
    # RETRY
    # --------------------------------------------------------

    for attempt in range(2):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            raw_text = response.text.strip()

            # Remove markdown code fences if model adds them
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")
            raw_text = raw_text.strip()

            profile = json.loads(raw_text)

            return validate_profile(profile)

        except Exception as error:

            print(
                f"Gemini attempt {attempt + 1} failed: {error}"
            )

            if attempt == 0:
                time.sleep(1)

    return None


# ============================================================
# MAIN PROFILE EXTRACTION FUNCTION
# ============================================================

def extract_profile(text):

    if not text or not text.strip():
        return create_empty_profile()

    text = text.strip()

    # --------------------------------------------------------
    # FIRST: LOCAL PARSER
    # --------------------------------------------------------

    local_profile = local_profile_parser(text)

    # --------------------------------------------------------
    # TRY GEMINI
    # --------------------------------------------------------

    gemini_profile = gemini_profile_parser(text)

    # --------------------------------------------------------
    # IF GEMINI WORKS, COMBINE IT WITH LOCAL EXTRACTION
    # --------------------------------------------------------

    if gemini_profile:

        final_profile = create_empty_profile()

        for key in final_profile:

            gemini_value = gemini_profile.get(key)
            local_value = local_profile.get(key)

            # Prefer Gemini when it provides a valid value
            if gemini_value is not None:
                final_profile[key] = gemini_value

            # Otherwise use local parser
            elif local_value is not None:
                final_profile[key] = local_value

        # ----------------------------------------------------
        # IMPORTANT FALLBACK OVERRIDES
        # ----------------------------------------------------
        # If local parser confidently understands a phrase,
        # don't allow Gemini's null value to remove it.
        # ----------------------------------------------------

        if local_profile["occupation"] is not None:
            final_profile["occupation"] = local_profile["occupation"]

        if local_profile["education"] is not None:
            final_profile["education"] = local_profile["education"]

        if local_profile["income_level"] is not None:
            final_profile["income_level"] = local_profile["income_level"]

        if local_profile["age"] is not None:
            final_profile["age"] = local_profile["age"]

        if local_profile["location"] is not None:
            final_profile["location"] = local_profile["location"]

        return validate_profile(final_profile)

    # --------------------------------------------------------
    # GEMINI FAILED → USE LOCAL PARSER
    # --------------------------------------------------------

    return local_profile