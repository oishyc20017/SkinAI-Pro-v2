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

    st.markdown("# 🔬 Skin Analysis")

    st.caption(
        "Upload a skin image for an AI-assisted skin lesion screening."
    )

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

        st.markdown("## 🧬 Prediction Result")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                "### Predicted Class"
            )

            st.markdown(
                f"## 🧬 {disease}"
            )

        with c2:

            st.markdown(
                "### AI Confidence"
            )

            st.markdown(
                f"## 📊 {confidence}%"
            )

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