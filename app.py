"""Entry point for local runs and Hugging Face Spaces."""

from app.ui.gradio_app import CUSTOM_CSS, build_app

demo = build_app()

if __name__ == "__main__":
    demo.launch(css=CUSTOM_CSS)
