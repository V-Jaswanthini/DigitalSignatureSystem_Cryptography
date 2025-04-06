import streamlit as st
import json
from io import BytesIO
import zipfile
from crypto_utils import generate_keys
from signature_utils import sign_data, verify_signature
from visual_sign import create_overlay
from PyPDF2 import PdfReader, PdfWriter

st.set_page_config(page_title="Digital Signature App", layout="centered")
st.title("Digital Signature Authentication System")

tab1, tab2, tab3, tab4 = st.tabs(["Key Management", "Sign File", "Verify Signature", "Visual Sign PDF"])

with tab1:
    st.subheader("Key Management")
    algorithm = st.selectbox("Select Algorithm", ["RSA", "DSA"])
    signer = st.text_input("Signer Name", "Anonymous")

    if st.button("Generate Key Pair"):
        private_key, public_key = generate_keys(algorithm)
        st.session_state["private"] = private_key
        st.session_state["public"] = public_key
        st.success("Keys generated!")

    if "private" in st.session_state and "public" in st.session_state:
        col1, col2 = st.columns(2)
        col1.download_button("⬇️ Private Key", st.session_state["private"], file_name="private.pem")
        col2.download_button("⬇️ Public Key", st.session_state["public"], file_name="public.pem")
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a") as zf:
            zf.writestr("private.pem", st.session_state["private"])
            zf.writestr("public.pem", st.session_state["public"])
        zip_buffer.seek(0)
        st.download_button("⬇️ Download All as ZIP", zip_buffer, file_name="keys.zip")

with tab2:
    st.subheader("Sign a File")
    file = st.file_uploader("Upload a file to sign")
    private_key_file = st.file_uploader("Upload your private key (.pem)")
    algorithm = st.selectbox("Algorithm Used", ["RSA", "DSA"], key="alg2")
    signer = st.text_input("Signer", "Anonymous", key="signer2")

    if file and private_key_file and st.button("Sign Now"):
        metadata = sign_data(file.read(), private_key_file.read(), algorithm, signer)
        signature_json = json.dumps(metadata, indent=4)
        st.code(signature_json, language="json")
        st.download_button("⬇️ Download Signature", signature_json, file_name="signature.json")

with tab3:
    st.subheader("Verify a Signature")
    original = st.file_uploader("Upload Original File")
    signature_file = st.file_uploader("Upload Signature JSON", type=["json"])
    public_key_file = st.file_uploader("Upload Public Key (.pem)")

    if original and signature_file and public_key_file and st.button("Verify"):
        metadata = json.load(signature_file)
        is_valid = verify_signature(original.read(), public_key_file.read(), metadata)
        st.success("Valid Signature✅") if is_valid else st.error("Invalid Signature❌")
        st.json(metadata)

with tab4:
    st.subheader("Visual Signature on PDF")
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    signer = st.text_input("Signer Name", "Anonymous", key="pdfsigner")
    if pdf and signer and st.button("Stamp PDF"):
        overlay = create_overlay(signer)
        overlay_pdf = PdfReader(overlay)
        base_pdf = PdfReader(pdf)
        writer = PdfWriter()
        for page in base_pdf.pages:
            page.merge_page(overlay_pdf.pages[0])
            writer.add_page(page)
        output = BytesIO()
        writer.write(output)
        output.seek(0)
        st.download_button("⬇️ Download Stamped PDF", output, file_name="signed_output.pdf", mime="application/pdf")
