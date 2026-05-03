import re
import argostranslate.package
import argostranslate.translate
from processing.glossary import FOOTBALL_GLOSSARY

TRANSLATION_LANGUAGE = "am"


def setup_translation():
    try:
        argostranslate.package.update_package_index()
        available = argostranslate.package.get_available_packages()
        pkg = next((p for p in available if p.from_code == "en" and p.to_code == TRANSLATION_LANGUAGE), None)
        if pkg:
            argostranslate.package.install_from_path(pkg.download())
    except Exception as e:
        print(f"Translation setup warning: {e}")


def apply_glossary(text: str) -> str:
    for en_term, am_term in FOOTBALL_GLOSSARY.items():
        text = re.sub(rf"\b{re.escape(en_term)}\b", am_term, text, flags=re.IGNORECASE)
    return text


def preprocess_text(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"@[A-Za-z0-9_]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

async def translate_text(text: str) -> str:
    try:
        original = preprocess_text(text)
        preprocessed = apply_glossary(original)
        translated = argostranslate.translate.translate(preprocessed, "en", TRANSLATION_LANGUAGE)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text
