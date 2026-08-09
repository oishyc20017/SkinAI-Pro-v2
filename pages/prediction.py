import streamlit as st
from PIL import Image

from services.prediction_service import predict_skin
from services.dashboard_service import save_prediction


DISEASE_INFO = {

    "Melanoma": {
        "about": (
            "Melanoma is a type of skin cancer that can develop in "
            "pigment-producing skin cells. Early evaluation is important."
        ),
        "warning": (
            "A new or changing spot, especially one with an irregular "
            "border, multiple colors, or noticeable changes in size or shape, "
            "should be assessed by a dermatologist."
        )
    },

    "Basal Cell Carcinoma": {
        "about": (
            "Basal cell carcinoma is a common type of skin cancer. "
            "It can appear in different forms, including raised or scaly "
            "skin growths."
        ),
        "warning": (
            "A skin growth that changes, bleeds, crusts, or does not heal "
            "should be checked by a dermatologist."
        )
    },

    "Benign Keratosis": {
        "about": (
            "Benign keratoses are non-cancerous skin growths. "
            "Their appearance can vary considerably."
        ),
        "warning": (
            "If a lesion changes noticeably, becomes painful, bleeds, "
            "or you are uncertain about it, arrange a professional skin exam."
        )
    },

    "Dermatofibroma": {
        "about": (
            "A dermatofibroma is a commonly occurring benign skin growth. "
            "A clinician can help distinguish it from other skin lesions."
        ),
        "warning": (
            "Seek professional evaluation if the spot changes, grows, "
            "bleeds, or becomes concerning."
        )
    },

    "Nevus": {
        "about": (
            "A nevus is commonly known as a mole. Most moles are benign, "
            "but changes in a mole can require medical assessment."
        ),
        "warning": (
            "A new or changing mole, particularly one with changes in "
            "shape, border, color, size, or appearance, should be assessed "
            "by a dermatologist."
        )
    },

    "Vascular Lesion": {
        "about": (
            "Vascular lesions are skin findings involving blood vessels "
            "and can have different causes and appearances."
        ),
        "warning": (
            "A lesion that changes, grows, bleeds, or causes persistent "
            "symptoms should be evaluated by a healthcare professional."
        )
    }
}


def prediction_page():
    st.markdown(
        """
        <style>

        .prediction-hero {
            text-align: center;
            padding: 20px 10px 28px 10px;
        }

        .prediction-icon {
            width: 70px;
            height: 70px;
            margin: auto;
            border-radius: 50%;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 32px;

            background: rgba(56, 189, 248, 0.10);
            border: 1px solid rgba(56, 189, 248, 0.35);

            box-shadow:
                0 0 20px rgba(56, 189, 248, 0.20);

            animation: predictionPulse 2.5s ease-in-out infinite;
        }

        .prediction-title {
            margin-top: 14px;
            font-size: 32px;
            font-weight: 700;
        }

        .prediction-subtitle {
            margin-top: 6px;
            color: #94A3B8;
            font-size: 15px;
        }

        .prediction-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;

            margin-top: 14px;
            padding: 6px 12px;

            border-radius: 20px;

            font-size: 12px;
            color: #94A3B8;

            background: rgba(15, 23, 42, 0.45);
            border: 1px solid rgba(148, 163, 184, 0.15);
        }

        .prediction-status span {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #22c55e;

            box-shadow:
                0 0 8px rgba(34, 197, 94, 0.8);

            animation: statusBlink 1.8s infinite;
        }

        @keyframes predictionPulse {

            0%, 100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.07);
            }

        }

        @keyframes statusBlink {

            0%, 100% {
                opacity: 1;
            }

            50% {
                opacity: 0.35;
            }

        }
        /* =========================================
        ANALYSIS RESULT CARD
        ========================================= */

        .result-card {
            margin-top: 20px;
            padding: 24px;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(56, 189, 248, 0.18);
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.18);
        }

        .result-label {
            color: #94A3B8;
            font-size: 13px;
            margin-bottom: 6px;
        }

        .result-disease {
            font-size: 27px;
            font-weight: 700;
            margin-bottom: 18px;
        }

        .confidence-label {
            display: flex;
            justify-content: space-between;
            color: #CBD5E1;
            font-size: 13px;
            margin-bottom: 8px;
        }

        .confidence-bar {
            width: 100%;
            height: 10px;
            border-radius: 10px;
            background: rgba(148, 163, 184, 0.15);
            overflow: hidden;
        }

        .confidence-fill {
            height: 100%;
            border-radius: 10px;
            background: linear-gradient(
                90deg,
                #38BDF8,
                #8B5CF6
            );
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.45);
            transition: width 0.8s ease;
        }

        .result-status {
            display: inline-block;
            margin-top: 18px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            color: #BAE6FD;
            background: rgba(56, 189, 248, 0.10);
            border: 1px solid rgba(56, 189, 248, 0.20);
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.html("""
    <div class="prediction-hero">

        <div class="prediction-icon">
            🔬
        </div>

        <div class="prediction-title">
            Skin Analysis
        </div>

        <div class="prediction-subtitle">
            Upload a skin image for AI-assisted skin lesion screening.
        </div>

        <div class="prediction-status">
            <span></span>
            AI Screening System Ready
        </div>

    </div>
    """,)
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        key="prediction_upload"
    )

    if uploaded_file is None:
        return

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    st.write("")

    if st.button(
        "🔍 Analyze Image",
        use_container_width=True,
        key="analyze_button"
    ):

        with st.spinner("AI is analyzing the image..."):

            result = predict_skin(image)

        # Save prediction once
        save_prediction(
            user_id=st.session_state.user_id,
            disease=result["disease"],
            confidence=result["confidence"]
        )

        disease = result["disease"]
        confidence = result["confidence"]

        info = DISEASE_INFO.get(
            disease,
            {
                "about": (
                    "This result is intended for educational screening "
                    "and should not be treated as a confirmed diagnosis."
                ),
                "warning": (
                    "If you are concerned about the lesion, consult "
                    "a qualified dermatologist."
                )
            }
        )

        # =====================================================
        # RESULT HEADER
        # =====================================================

        st.success("Analysis Completed ✅")

        st.html(f"""
        <div class="result-card">

            <div class="result-label">
                🧬 AI PREDICTION
            </div>

            <div class="result-disease">
                {disease}
            </div>

            <div class="confidence-label">
                <span>AI Confidence</span>
                <span>{confidence}%</span>
            </div>

            <div class="confidence-bar">
                <div
                    class="confidence-fill"
                    style="width: {confidence}%;">
                </div>
            </div>

            <div class="result-status">
                ✓ Analysis completed
            </div>

        </div>
        """)

        st.divider()

        # =====================================================
        # ABOUT RESULT
        # =====================================================

        st.markdown("### 📖 About This Result")

        st.info(
            info["about"]
        )

        # =====================================================
        # DOCTOR GUIDANCE
        # =====================================================

        st.markdown(
            "### 🩺 When Should You See a Doctor?"
        )

        st.warning(
            info["warning"]
        )

        # =====================================================
        # MEDICAL DISCLAIMER
        # =====================================================

        st.divider()

        st.markdown(
            "### ⚠️ Medical Disclaimer"
        )

        st.caption(
            "This AI result is not a confirmed medical diagnosis. "
            "Image-based screening can be inaccurate. A qualified "
            "dermatologist should evaluate any suspicious, changing, "
            "bleeding, painful, or persistent skin lesion."
        )