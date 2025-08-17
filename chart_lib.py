import fitz  # PyMuPDF
import os

def extract_charts_from_pdf(pdf_path, output_dir):
    """
    Extracts all images (charts, figures, etc.) from a PDF and saves them as PNG files.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str): Directory where extracted images will be saved.
    """
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Open PDF
    doc = fitz.open(pdf_path)
    img_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)  # Extract all images on page

        for img_index, img in enumerate(images):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            # Convert CMYK or other color spaces to RGB
            if pix.n > 3:
                pix = fitz.Pixmap(fitz.csRGB, pix)

            img_count += 1
            img_filename = os.path.join(output_dir, f"page{page_num+1}_img{img_index+1}.png")
            pix.save(img_filename)
            pix = None  # free memory

    print(f"✅ Extracted {img_count} images from {pdf_path} into {output_dir}")


# Example usage
pdf_file = "JP Morgan - 03 Sep 2024.pdf"   # your PDF file
output_folder = "charts_output"
extract_charts_from_pdf(pdf_file, output_folder)
