import reflex as rx
import googletrans
from PIL import Image
import requests


class Translation(rx.Base):
    original_text: str
    translated_text: str


class TranslationState(rx.State):
    source_language: str = "auto"
    destination_language: str = "No selection yet"
    input_text: str
    show: bool = False
    current_translation = Translation(
        original_text="", translated_text=""
    )
    url = f"https://cdn-icons-png.flaticon.com/128/4305/4305572.png"
    image = Image.open(requests.get(url, stream=True).raw)

    def translate(self):
        if len(self.input_text) == 0:
            self.input_text = "#"
            return
        
        if self.destination_language == "No selection yet":
            return


        try:
            translation = googletrans.Translator().translate(self.input_text, dest=self.destination_language)
            if translation and hasattr(translation, 'text'):
                self.current_translation = Translation(
                    original_text=self.input_text,
                    translated_text=translation.text,
                )
            else:
                self.current_translation = Translation(
                    original_text=self.input_text,
                    translated_text="Translation not available",
                )

        except Exception as e:
            self.current_translation = Translation(
                original_text=self.input_text,
                translated_text="Error: " + str(e),
            )


    # clear all the fields and reset the state when web page is refreshed
    def on_load(self):
        self.reset()

    def change(self):
        self.show = not (self.show)

    def swap_languages(self):
        if self.source_language == "auto":
            self.change()
            return

        self.source_language, self.destination_language = self.destination_language, self.source_language
        self.input_text = self.current_translation.translated_text
        self.translate()



