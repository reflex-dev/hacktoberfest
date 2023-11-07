import reflex as rx

import pytesseract
from PIL import Image

class State(rx.State):
    """The app state."""

    extracted_text_heading: str

    extracted_text: str

    is_loading: bool = False

    loading_text: str = ""


    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of files and extraction of text.

        Args:
            files: The uploaded files.
        """

        # set the following values to spin the button and
        # show text
        self.is_loading = True
        self.loading_text = "uploading and extracting text...."
        yield



        for file in files:
            upload_data = await file.read()
            outfile = rx.get_asset_path(file.filename)

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Open an image using Pillow (PIL)
            image = Image.open(outfile)

            # Use Tesseract to extract text from the image
            text = pytesseract.image_to_string(image)
            text = text.encode("ascii", "ignore")
            self.extracted_text = text.decode()

            self.extracted_text_heading = "Extracted Text👇"

            # reset state variable again
            self.is_loading = False
            self.loading_text = ""
            yield