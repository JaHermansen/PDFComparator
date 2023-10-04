# PDF Drawings Comparator

This tool allows users to compare construction drawings in PDF format. By converting these PDFs into images, it leverages the Structural Similarity Index (SSIM) to find differences between old and new drawings.

## Dependencies

- os
- streamlit
- pdf2image
- PIL
- skimage

## How to Use

1. Launch the Streamlit app.
2. Upload the old drawings in PDF format.
3. Upload the new drawings in PDF format.
4. Click on "Compare Drawings".
5. The tool will then display the SSIM score for each drawing. Drawings with a score less than 0.99 are considered different.

## Key Functions

### `pdf_to_image(pdf_memoryview)`

Converts a single-page PDF memoryview to an image. 

### `images_are_same(img1, img2, threshold=0.99)`

Compares two images using SSIM and returns the similarity score.

### `compare_pdfs(old_pdfs, new_pdfs)`

Compares single-page PDFs and returns a list of filenames where the PDFs differ.

## Code

[Embed your code here by using triple backticks followed by "python"]

```python
import os
import streamlit as st
from pdf2image import convert_from_path
...
...
...
if __name__ == "__main__":
    main()


For the "Embed your code here" section in the above markdown, you would use the triple backtick syntax to start a code block (```) followed by the word `python` to indicate the language, then paste your code, and end with another set of triple backticks to close the code block. The given markdown provides context and descriptions for your code to make it more readable and understandable to visitors to your GitHub repository.
