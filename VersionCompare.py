import os
import streamlit as st
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
from PIL import ImageChops
from skimage.metrics import structural_similarity as ssim
import numpy as np

# Get the home directory
home_dir = os.path.expanduser("~")

# Set the Downloads path based on OS
downloads_path = os.path.join(home_dir, "Downloads")

def pdf_to_image(pdf_memoryview):
    """
    Convert a single-page PDF memoryview to an image.
    """
    poppler_utils_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poppler_folder', 'Library', 'bin')
    return convert_from_bytes(pdf_memoryview.tobytes(), poppler_path=poppler_utils_path)[0]

def images_are_same(img1, img2, threshold=0.99):
    """
    Compare two images using SSIM and return the similarity score.
    """
    img1 = img1.convert("L")  # Convert to grayscale
    img2 = img2.resize(img1.size).convert("L")  # Resize and convert to grayscale
    similarity, _ = ssim(np.array(img1), np.array(img2), full=True)
    return similarity

def compare_pdfs(old_pdfs, new_pdfs):
    """
    Compare single-page PDFs.
    Return a list of filenames where the PDFs differ.
    """
    differing_pdfs = []

    if len(old_pdfs) != len(new_pdfs):
        raise ValueError("The two sets of PDFs are not of the same length.")

    for old_pdf, new_pdf in zip(old_pdfs, new_pdfs):
        img1 = pdf_to_image(old_pdf.getbuffer())
        img2 = pdf_to_image(new_pdf.getbuffer())
        
        # Resize img2 to match img1's size for consistent comparison
        img2 = img2.resize(img1.size)
        
        # Save both images for inspection in the Downloads directory
        img1_path = os.path.join(downloads_path, f"{old_pdf.name}_old.png")
        img2_path = os.path.join(downloads_path, f"{old_pdf.name}_new.png")
        img1.save(img1_path)
        img2.save(img2_path)

        similarity = images_are_same(img1, img2)
        
        # Print the SSIM score with the PDF name
        st.write(f"SSIM Score for {old_pdf.name}: {similarity:.2f}")
        
        if similarity < 0.99:
            differing_pdfs.append(old_pdf.name)
            st.write(f"Difference found in {old_pdf.name}. Difference percentage: {100*(1-similarity):.2f}%")
           
    return differing_pdfs

def main():
    st.title("PDF Drawings Comparator")

    st.write("Upload the PDFs from the old and new construction drawings folders.")
    
    uploaded_old_drawings = st.file_uploader("Upload old drawings", type=['pdf'], accept_multiple_files=True)
    uploaded_new_drawings = st.file_uploader("Upload new drawings", type=['pdf'], accept_multiple_files=True)

    if st.button("Compare Drawings"):
        try:
            differences = compare_pdfs(uploaded_old_drawings, uploaded_new_drawings)

            if differences:
                st.write("Drawings that differ:")
                for diff in differences:
                    st.write(diff)
            else:
                st.write("All drawings are the same.")
        except Exception as e:
            st.write(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
