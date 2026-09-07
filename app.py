import streamlit as st

from streamlit_mic_recorder import speech_to_text

from core.profile_parser import extract_profile
from core.matcher import find_matching_schemes
from utils.speech import speak_hindi


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VaaniAccess",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
"""
<style>

.main {
    padding-top: 1rem;
}

.hero {
    padding: 30px;
    border-radius: 18px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 18px;
    opacity: 0.75;
    line-height: 1.5;
}

.section-title {
    font-size: 26px;
    font-weight: 650;
    margin-top: 20px;
    margin-bottom: 8px;
}

.scheme-card {
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    margin-top: 15px;
    margin-bottom: 15px;
}

.scheme-name {
    font-size: 24px;
    font-weight: 650;
    margin-bottom: 8px;
}

.scheme-description {
    font-size: 16px;
    line-height: 1.5;
    opacity: 0.85;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: 600;
    margin-top: 8px;
}

.strong-badge {
    background: rgba(40, 167, 69, 0.15);
}

.potential-badge {
    background: rgba(255, 193, 7, 0.18);
}

.info-badge {
    background: rgba(108, 117, 125, 0.15);
}

.transcript-box {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    font-size: 17px;
    line-height: 1.6;
    margin-top: 8px;
}

.footer {
    text-align: center;
    opacity: 0.6;
    padding: 25px;
    font-size: 14px;
}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""

if "results" not in st.session_state:
    st.session_state.results = None

if "profile" not in st.session_state:
    st.session_state.profile = None


# ============================================================
# HERO
# ============================================================

st.markdown(
"""
<div class="hero">
<div class="hero-title">🎙️ VaaniAccess</div>
<div class="hero-subtitle">
Find potentially relevant government schemes using your own words
in Hindi, English, or Hinglish.
</div>
</div>
""",
unsafe_allow_html=True
)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(
"""
<div class="section-title">
🗣️ Tell us about yourself
</div>
""",
unsafe_allow_html=True
)

st.caption(
    'Speak naturally or type your situation. Example: '
    '"Main college student hoon aur meri family ki income bahut kam hai."'
)


# ============================================================
# INPUT COLUMNS
# ============================================================

voice_col, text_col = st.columns(2)


# ============================================================
# VOICE INPUT
# ============================================================

with voice_col:

    st.markdown("### 🎙️ Voice Input")

    st.caption(
        "Speak in Hindi or Hinglish."
    )

    new_voice_text = speech_to_text(
        language="hi-IN",
        start_prompt="🎙️ Start Speaking",
        stop_prompt="⏹️ Stop Speaking",
        just_once=True,
        use_container_width=True,
        key="vaani_voice"
    )

    if new_voice_text:

        st.session_state.voice_text = new_voice_text

        # Clear previous typed input when new voice input arrives
        st.session_state.typed_text = ""

        st.success(
            "Voice converted to text ✓"
        )


# ============================================================
# TEXT INPUT
# ============================================================

with text_col:

    st.markdown("### ⌨️ Text Input")

    typed_text = st.text_area(
        "Describe your situation",
        value=st.session_state.typed_text,
        placeholder=(
            "Example:\n"
            "Main college student hoon.\n"
            "Mere ghar ki income bahut kam hai."
        ),
        height=130,
        label_visibility="collapsed"
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Save typed text and clear old voice text when user types
    # --------------------------------------------------------

    if typed_text != st.session_state.typed_text:

        st.session_state.typed_text = typed_text

        if typed_text.strip():

            st.session_state.voice_text = ""


# ============================================================
# SHOW VOICE TRANSCRIPT
# ============================================================

if st.session_state.voice_text:

    st.markdown(
        "### 📝 Voice Transcript"
    )

    st.markdown(
        f"""
        <div class="transcript-box">
        {st.session_state.voice_text}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FIND SCHEMES
# ============================================================

st.write("")

find_button = st.button(
    "🔎 Find Suitable Schemes",
    type="primary",
    use_container_width=True
)


# ============================================================
# PROCESS INPUT
# ============================================================

if find_button:

    # ========================================================
    # IMPORTANT INPUT PRIORITY
    # ========================================================
    #
    # Typed text gets priority if the user has entered text.
    #
    # Otherwise use the latest voice transcript.
    #
    # ========================================================

    if st.session_state.typed_text.strip():

        user_input = st.session_state.typed_text.strip()

        input_type = "text"

    elif st.session_state.voice_text.strip():

        user_input = st.session_state.voice_text.strip()

        input_type = "voice"

    else:

        user_input = ""

        input_type = None


    # ========================================================
    # EMPTY INPUT
    # ========================================================

    if not user_input:

        st.warning(
            "Please speak or type your situation first."
        )

    else:

        # ----------------------------------------------------
        # PROFILE EXTRACTION
        # ----------------------------------------------------

        with st.spinner(
            "🧠 Understanding your situation..."
        ):

            profile = extract_profile(
                user_input
            )

        st.session_state.profile = profile


        # ----------------------------------------------------
        # FIND MATCHES
        # ----------------------------------------------------

        with st.spinner(
            "🎯 Finding potentially suitable schemes..."
        ):

            matches = find_matching_schemes(
                profile
            )

        st.session_state.results = matches


# ============================================================
# DISPLAY RESULTS
# ============================================================

if st.session_state.results is not None:

    profile = st.session_state.profile

    matches = st.session_state.results


    # ========================================================
    # PROFILE
    # ========================================================

    st.divider()

    st.markdown(
        """
        <div class="section-title">
        👤 What we understood
        </div>
        """,
        unsafe_allow_html=True
    )


    profile_col1, profile_col2, profile_col3, profile_col4 = st.columns(4)


    with profile_col1:

        st.metric(
            "Occupation",
            profile.get("occupation") or "Not provided"
        )


    with profile_col2:

        st.metric(
            "Education",
            profile.get("education") or "Not provided"
        )


    with profile_col3:

        st.metric(
            "Income",
            profile.get("income_level") or "Not provided"
        )


    with profile_col4:

        age = profile.get("age")

        st.metric(
            "Age",
            str(age) if age else "Not provided"
        )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.markdown(
        """
        <div class="section-title">
        🎯 Recommended Schemes
        </div>
        """,
        unsafe_allow_html=True
    )


    if matches:

        # ====================================================
        # BEST MATCH
        # ====================================================

        best_match = matches[0]

        best_scheme = best_match["scheme"]

        best_score = best_match["score"]

        best_status = best_match["status"]


        st.markdown(
            "### ⭐ Best Match"
        )


        st.markdown(
            f"""
            <div class="scheme-card">

            <div class="scheme-name">
            🎯 {best_scheme["name"]}
            </div>

            <div class="scheme-description">
            {best_scheme["description"]}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        score_col, status_col = st.columns(2)


        with score_col:

            st.metric(
                "Match Score",
                f"{best_score}%"
            )


        with status_col:

            if best_status == "Strong Match":

                st.markdown(
                    """
                    <div class="badge strong-badge">
                    🟢 Strong Match
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif best_status == "Potential Match":

                st.markdown(
                    """
                    <div class="badge potential-badge">
                    🟡 Potential Match
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="badge info-badge">
                    ⚪ Needs More Information
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # ----------------------------------------------------
        # WHY IT MATCHES
        # ----------------------------------------------------

        if best_match["matched"]:

            st.markdown(
                "#### ✅ Why it matches"
            )

            for item in best_match["matched"]:

                st.write(
                    f"✓ {item}"
                )


        # ----------------------------------------------------
        # MISSING INFORMATION
        # ----------------------------------------------------

        if best_match["missing"]:

            st.markdown(
                "#### ⚠️ Information still needed"
            )

            for item in best_match["missing"]:

                st.write(
                    f"• {item}"
                )


        # ----------------------------------------------------
        # WARNING
        # ----------------------------------------------------

        st.warning(
            "This is a potential recommendation based on "
            "the information you provided. Final eligibility "
            "must be verified using the official scheme requirements."
        )


        # ----------------------------------------------------
        # DOCUMENTS + STEPS
        # ----------------------------------------------------

        with st.expander(
            "📋 Documents and Application Steps",
            expanded=True
        ):

            st.markdown(
                "#### 📋 Documents / Information"
            )

            documents = best_scheme.get(
                "documents",
                []
            )

            if documents:

                for document in documents:

                    st.write(
                        f"• {document}"
                    )

            else:

                st.write(
                    "No document information available."
                )


            st.markdown(
                "#### 🪜 Suggested Steps"
            )

            steps = best_scheme.get(
                "steps",
                []
            )

            if steps:

                for index, step in enumerate(
                    steps,
                    start=1
                ):

                    st.write(
                        f"{index}. {step}"
                    )

            else:

                st.write(
                    "No application steps available."
                )


        # ----------------------------------------------------
        # OFFICIAL SOURCE
        # ----------------------------------------------------

        official_source = best_scheme.get(
            "official_source"
        )

        if official_source:

            st.link_button(
                "🔗 Verify on Official Website",
                official_source,
                use_container_width=True
            )


        # ----------------------------------------------------
        # VERIFICATION NOTE
        # ----------------------------------------------------

        verification_note = best_scheme.get(
            "verification_note"
        )

        if verification_note:

            st.info(
                f"ℹ️ {verification_note}"
            )


        # ----------------------------------------------------
        # HINDI VOICE
        # ----------------------------------------------------

        st.markdown(
            "#### 🔊 Listen in Hindi"
        )


        speech_text = (
            f"Aapke liye {best_scheme['name']} "
            f"ek potentially suitable scheme ho sakti hai. "
            f"{best_scheme['description']} "
            f"Kripya official website par eligibility verify karein."
        )


        speak_hindi(
            speech_text
        )


        # ====================================================
        # OTHER MATCHES
        # ====================================================

        if len(matches) > 1:

            st.divider()

            st.markdown(
                "### 📚 Other Potential Matches"
            )


            for index, match in enumerate(
                matches[1:],
                start=2
            ):

                scheme = match["scheme"]

                score = match["score"]

                status = match["status"]


                with st.expander(
                    f"{index}. {scheme['name']} — {score}%"
                ):

                    st.write(
                        scheme["description"]
                    )


                    if status == "Strong Match":

                        st.success(
                            f"🟢 {status} — {score}%"
                        )

                    elif status == "Potential Match":

                        st.warning(
                            f"🟡 {status} — {score}%"
                        )

                    else:

                        st.info(
                            f"⚪ {status} — {score}%"
                        )


                    if match["matched"]:

                        st.markdown(
                            "#### ✅ Matching Information"
                        )

                        for item in match["matched"]:

                            st.write(
                                f"✓ {item}"
                            )


                    if match["missing"]:

                        st.markdown(
                            "#### ⚠️ Still Needed"
                        )

                        for item in match["missing"]:

                            st.write(
                                f"• {item}"
                            )


                    st.markdown(
                        "#### 📋 Documents"
                    )

                    for document in scheme.get(
                        "documents",
                        []
                    ):

                        st.write(
                            f"• {document}"
                        )


                    if scheme.get(
                        "official_source"
                    ):

                        st.link_button(
                            "🔗 Verify Official Source",
                            scheme["official_source"]
                        )


    # ========================================================
    # NO MATCHES
    # ========================================================

    else:

        st.info(
            "No potentially suitable scheme was found "
            "from the current dataset."
        )

        st.write(
            "Try providing more information such as your "
            "occupation, education, age, income or location."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
"""
<div class="footer">
<b>VaaniAccess</b> · Voice-first Public Scheme Navigator
<br>
AI-assisted understanding + rule-based eligibility matching
</div>
""",
unsafe_allow_html=True
)