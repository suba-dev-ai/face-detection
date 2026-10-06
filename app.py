import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import io

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="VISION AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(255, 190, 210, 0.55), transparent 28%),
        radial-gradient(circle at 80% 90%, rgba(255, 220, 230, 0.7), transparent 30%),
        #fff5f8;
}

/* Hide Streamlit default */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main portrait container */

.block-container {
    max-width: 720px !important;
    min-height: 100vh;
    padding: 30px 25px 50px 25px !important;
    margin: auto;
}

/* Top bar */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(255,170,195,0.35);
    border-radius: 22px;
    padding: 15px 20px;
    box-shadow: 0 8px 30px rgba(225,120,150,0.10);
    backdrop-filter: blur(15px);
    margin-bottom: 40px;
}

.logo {
    font-size: 20px;
    font-weight: 700;
    color: #29212a;
    letter-spacing: 1px;
}

.online {
    color: #d95f82;
    font-size: 12px;
    font-weight: 600;
}

.dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #ef7195;
    border-radius: 50%;
    margin-right: 5px;
}

/* Hero */

.hero {
    text-align: center;
    margin-bottom: 35px;
}

.hero-small {
    color: #d56b89;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 3px;
    margin-bottom: 8px;
}

.hero-title {
    font-size: 46px;
    font-weight: 700;
    color: #2d2228;
    line-height: 1;
    margin: 0;
}

.hero-line {
    width: 55px;
    height: 4px;
    background: #efa0b7;
    border-radius: 20px;
    margin: 18px auto;
}

/* Cards */

.card {
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(238,157,181,0.35);
    border-radius: 28px;
    padding: 25px;
    margin-bottom: 18px;
    box-shadow: 0 12px 35px rgba(210,110,140,0.10);
    transition: 0.25s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 40px rgba(210,110,140,0.17);
}

.icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ffe1ea;
    border-radius: 16px;
    color: #d65f82;
    font-size: 23px;
    margin-bottom: 15px;
}

.card-title {
    color: #2b2227;
    font-size: 19px;
    font-weight: 600;
    margin-bottom: 15px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border: none !important;
    border-radius: 15px !important;
    background: #efa0b7 !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px !important;
    transition: 0.2s ease !important;
}

.stButton > button:hover {
    background: #df7898 !important;
    transform: translateY(-2px);
}

/* Back button */

.back-button .stButton > button {
    width: auto !important;
    background: white !important;
    color: #d15e80 !important;
    border: 1px solid #f0bdcc !important;
}

/* Upload */

[data-testid="stFileUploader"] {
    background: white;
    border-radius: 20px;
    padding: 10px;
    border: 1px solid #f0c2cf;
}

/* Image */

.stImage img {
    border-radius: 20px;
}

/* Metrics */

.metric-box {
    background: white;
    border: 1px solid #f2c5d1;
    border-radius: 18px;
    padding: 15px;
    text-align: center;
}

.metric-value {
    font-size: 24px;
    font-weight: 700;
    color: #d65f82;
}

.metric-label {
    font-size: 11px;
    color: #8c737c;
}

/* Result */

.result-match {
    background: #e9f9f0;
    color: #26915b;
    padding: 15px;
    border-radius: 18px;
    text-align: center;
    font-weight: 700;
    margin: 15px 0;
}

.result-no {
    background: #fff0f2;
    color: #d94d68;
    padding: 15px;
    border-radius: 18px;
    text-align: center;
    font-weight: 700;
    margin: 15px 0;
}

/* Footer */

.footer {
    text-align: center;
    color: #ad8c97;
    font-size: 11px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"


def go_home():
    st.session_state.page = "home"


def go_detection():
    st.session_state.page = "detection"


def go_verification():
    st.session_state.page = "verification"


def go_pattern():
    st.session_state.page = "pattern"


# =========================================================
# TOP BAR
# =========================================================

st.markdown("""
<div class="topbar">
    <div class="logo">◈ VISION AI</div>
    <div class="online">
        <span class="dot"></span>ONLINE
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# IMAGE CONVERTER
# =========================================================

def uploaded_to_cv(uploaded_file):

    image_bytes = uploaded_file.read()

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    image_np = np.array(image)

    return cv2.cvtColor(
        image_np,
        cv2.COLOR_RGB2BGR
    )


def cv_to_rgb(image):

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )


# =========================================================
# FACE CASCADE
# =========================================================

CASCADE_PATH = os.path.join(
    cv2.data.haarcascades,
    "haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

if face_cascade.empty():
    st.error("❌ Haar Cascade file could not be loaded.")
    st.stop()


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    st.markdown("""
    <div class="hero">
        <div class="hero-small">COMPUTER VISION</div>
        <div class="hero-title">VISION AI</div>
        <div class="hero-line"></div>
    </div>
    """, unsafe_allow_html=True)

    # Face Detection
    st.markdown("""
    <div class="card">
        <div class="icon">◉</div>
        <div class="card-title">FACE DETECTION</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("OPEN  →", key="detection_home"):
        go_detection()
        st.rerun()

    # Face Verification
    st.markdown("""
    <div class="card">
        <div class="icon">◎</div>
        <div class="card-title">FACE VERIFICATION</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("OPEN  →", key="verification_home"):
        go_verification()
        st.rerun()

    # Pattern Localization
    st.markdown("""
    <div class="card">
        <div class="icon">⌖</div>
        <div class="card-title">PATTERN LOCALIZATION</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("OPEN  →", key="pattern_home"):
        go_pattern()
        st.rerun()

    st.markdown(
        '<div class="footer">VISION AI • 2026</div>',
        unsafe_allow_html=True
    )


# =========================================================
# BACK BUTTON
# =========================================================

def back_button():

    st.markdown(
        '<div class="back-button">',
        unsafe_allow_html=True
    )

    if st.button("←  BACK", key="back"):
        go_home()
        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# FACE DETECTION
# =========================================================

def face_detection_page():

    back_button()

    st.markdown("""
    <div class="hero">
        <div class="hero-small">MODULE 01</div>
        <div class="hero-title">FACE DETECTION</div>
        <div class="hero-line"></div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"],
        key="face_detection_upload"
    )

    if uploaded:

        image = uploaded_to_cv(uploaded)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        output = image.copy()

        for (x, y, w, h) in faces:

            cv2.rectangle(
                output,
                (x, y),
                (x + w, y + h),
                (255, 255, 255),
                3
            )

        st.image(
            cv_to_rgb(output),
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{len(faces)}</div>
                <div class="metric-label">FACES</div>
            </div>
            """, unsafe_allow_html=True)

        if len(faces) > 0:

            x, y, w, h = faces[0]

            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{w}</div>
                    <div class="metric-label">WIDTH</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{h}</div>
                    <div class="metric-label">HEIGHT</div>
                </div>
                """, unsafe_allow_html=True)


# =========================================================
# FACE VERIFICATION HELPERS
# =========================================================

def get_largest_face(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if len(faces) == 0:
        return None

    largest = max(
        faces,
        key=lambda rect: rect[2] * rect[3]
    )

    x, y, w, h = largest

    return image[y:y+h, x:x+w]


def prepare_face(face):

    gray = cv2.cvtColor(
        face,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.resize(
        gray,
        (128, 128)
    )

    gray = cv2.equalizeHist(gray)

    return gray.flatten().astype(np.float32)


# =========================================================
# FACE VERIFICATION
# =========================================================

def face_verification_page():

    back_button()

    st.markdown("""
    <div class="hero">
        <div class="hero-small">MODULE 02</div>
        <div class="hero-title">FACE VERIFICATION</div>
        <div class="hero-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        img1_file = st.file_uploader(
            "Image 01",
            type=["jpg", "jpeg", "png"],
            key="verify_1"
        )

    with col2:

        img2_file = st.file_uploader(
            "Image 02",
            type=["jpg", "jpeg", "png"],
            key="verify_2"
        )

    if img1_file and img2_file:

        image1 = uploaded_to_cv(img1_file)
        image2 = uploaded_to_cv(img2_file)

        face1 = get_largest_face(image1)
        face2 = get_largest_face(image2)

        if face1 is None or face2 is None:

            st.error("Face not detected.")

            return

        face_data1 = prepare_face(face1)
        face_data2 = prepare_face(face2)

        correlation = np.corrcoef(
            face_data1,
            face_data2
        )[0, 1]

        similarity = (
            (correlation + 1.0) / 2.0
        ) * 100.0

        similarity = max(
            0,
            min(100, similarity)
        )

        is_match = similarity >= 70

        if is_match:

            st.markdown("""
            <div class="result-match">
                ✓ MATCH
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="result-no">
                ✕ NO MATCH
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">
                {similarity:.2f}%
            </div>
            <div class="metric-label">
                SIMILARITY
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                cv_to_rgb(face1),
                use_container_width=True
            )

        with col2:

            st.image(
                cv_to_rgb(face2),
                use_container_width=True
            )


# =========================================================
# PATTERN LOCALIZATION
# =========================================================

def pattern_localization_page():

    back_button()

    st.markdown("""
    <div class="hero">
        <div class="hero-small">MODULE 03</div>
        <div class="hero-title">PATTERN LOCALIZATION</div>
        <div class="hero-line"></div>
    </div>
    """, unsafe_allow_html=True)

    main_file = st.file_uploader(
        "Main Image",
        type=["jpg", "jpeg", "png"],
        key="main_image"
    )

    template_file = st.file_uploader(
        "Template Image",
        type=["jpg", "jpeg", "png"],
        key="template_image"
    )

    if main_file and template_file:

        main_image = uploaded_to_cv(main_file)
        template_image = uploaded_to_cv(template_file)

        main_gray = cv2.cvtColor(
            main_image,
            cv2.COLOR_BGR2GRAY
        )

        template_gray = cv2.cvtColor(
            template_image,
            cv2.COLOR_BGR2GRAY
        )

        main_h, main_w = main_gray.shape
        template_h, template_w = template_gray.shape

        if template_h > main_h or template_w > main_w:

            st.error(
                "Template image must be smaller than main image."
            )

            return

        result = cv2.matchTemplate(
            main_gray,
            template_gray,
            cv2.TM_CCOEFF_NORMED
        )

        min_val, max_val, min_loc, max_loc = \
            cv2.minMaxLoc(result)

        x, y = max_loc

        output = main_image.copy()

        cv2.rectangle(
            output,
            (x, y),
            (x + template_w, y + template_h),
            (255, 255, 255),
            3
        )

        st.image(
            cv_to_rgb(output),
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">
                    {max_val:.2f}
                </div>
                <div class="metric-label">
                    MATCH SCORE
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">
                    {x}
                </div>
                <div class="metric-label">
                    X POSITION
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">
                    {y}
                </div>
                <div class="metric-label">
                    Y POSITION
                </div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# ROUTING
# =========================================================

if st.session_state.page == "home":

    home_page()

elif st.session_state.page == "detection":

    face_detection_page()

elif st.session_state.page == "verification":

    face_verification_page()

elif st.session_state.page == "pattern":

    pattern_localization_page()
