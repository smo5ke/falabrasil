# -*- coding: utf-8 -*-
"""
بناء dictionary.json الجديد من ملف الإكسل (5,000 كلمة) مع توليد النطق العربي.

المصدر: قاموس_البرتغالية_البرازيلية_5000.xlsx (ورقة "القاموس الكامل")
الأعمدة: 0:#  1:المستوى  2:الكلمة  3:المعنى  4:مثال  5:ترجمة المثال
         6:نوع الكلمة  7:الفعل/الكلمة الأساسية  8:الصيغة  9:الحفظ/المراجعة

الناتج: dictionary.json (id, word, phonetic, pos, translation, level, example, exampleTr, base, form)
النطق: كلمات مُثبّتة يدوياً + توليد قواعدي (نمط لفظ البرازيل).
"""
import json
import re
import shutil
import unicodedata

from openpyxl import load_workbook

XLSX = "قاموس_البرتغالية_البرازيلية_5000.xlsx"
OUT = "dictionary.json"
BACKUP = "dictionary_10000_backup.json"


def normalize(word: str) -> str:
    if not word:
        return ""
    s = str(word).strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\s+", " ", s)
    return s


# كلمات شائعة نطقها مُثبّت يدوياً (بأسلوب أمثلة التطبيق)
MANUAL_PHONETICS = {
    "ser": "سير", "ter": "تير", "ver": "فير", "ir": "إير", "vir": "فير",
    "estar": "إستار", "fazer": "فازير", "falar": "فالار", "comer": "كومير",
    "bom": "بوم", "bem": "بين", "tambem": "تامبين", "nao": "ناو",
    "sim": "سين", "obrigado": "أوبريغادو", "obrigada": "أوبريغادا",
    "voce": "فوسي", "voces": "فوسيس", "tudo": "تودو", "casa": "كازا",
    "amigo": "أميجو", "amiga": "أميغا", "trabalho": "تراباليو",
    "muito": "مونتا", "portugues": "بورتوجيس", "brasil": "برازيل",
    "hoje": "وجي", "tarde": "تارجي", "dia": "جيا", "praia": "برايا",
    "cara": "كارا", "beleza": "بيليزا", "valeu": "فاليو",
    "de": "دجي", "da": "دا", "do": "دو", "dos": "دوس", "das": "داس",
    "e": "ي", "em": "إن", "eu": "أيو",
    "a": "ا", "o": "و", "os": "أوس", "as": "أس", "um": "أون", "uma": "أونا",
    "ele": "إلي", "ela": "إيلا", "eles": "إيليس", "elas": "إيلاس",
    "nos": "نوس", "por": "بور", "para": "بارا", "com": "كون",
    "mundo": "موندو", "amor": "أمور", "vida": "فيذا", "tempo": "تيمبو",
    "noite": "نويشي", "gente": "جينشي", "mulher": "موليير",
    "dinheiro": "جينييرو", "cidade": "سيدادجي", "escola": "إسكولا",
    "livro": "ليفرو", "carro": "كاخو", "ola": "آلو", "banho": "بانيو",
}

# قواعد قبلية تعمل على نص ASCII-plain بعد إزالة النبرات
PRE_RULES = [
    (r"que", "كي"), (r"qui", "كي"), (r"qua", "كوا"), (r"quo", "كو"),
    (r"gua", "غوا"), (r"guo", "غو"), (r"gue", "غي"), (r"gui", "غي"),
    (r"lh", "لي"), (r"nh", "ني"), (r"ch", "ش"),
    (r"ss", "س"), (r"rr", "خر"),
    (r"cao", "ساو"),
    (r"x", "ش"),
    (r"g(?=[ei])", "ج"),
    (r"c(?=[ei])", "س"),
    # de/di/ti الوسطية والنهائية تصبح جيمية (نمط لفظ البرازيل)
    (r"(?<!^)de(?![aeiou])", "دجي"),
    (r"(?<!^)di", "دجي"),
    (r"(?<!^)ti", "تشي"),
    # s بين حرفي علّة -> ز
    (r"(?<=[aeiou])s(?=[aeiou])", "ز"),
]

LETTER_MAP = {
    "b": "ب", "d": "د", "f": "ف", "z": "ز", "v": "ف", "p": "ب", "t": "ت",
    "l": "ل", "m": "م", "n": "ن", "j": "ج", "k": "ك", "w": "و", "y": "ي",
    "r": "ر", "s": "س", "g": "غ", "c": "ك", "h": "", "q": "ك",
    "a": "ا", "e": "ي", "i": "ي", "o": "و", "u": "و",
    "'": "", "-": "-",
}


def transliterate(word: str) -> str:
    """نطق عربي تقريبي لكلمة برتغالية برازيلية."""
    src = str(word).strip().lower()
    if not src:
        return ""
    key = normalize(src)
    if key in MANUAL_PHONETICS:
        return MANUAL_PHONETICS[key]

    # تأمين ç/ã/õ استثنائياً قبل إزالة النبرات
    s = src.replace("ç", "\u0001").replace("ã", "\u0002").replace("õ", "\u0003")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))

    for pattern, repl in PRE_RULES:
        s = re.sub(pattern, repl, s)

    # استبدال التوكنز بحروفها العربية
    s = s.replace("\u0001", "س").replace("\u0002", "ا").replace("\u0003", "و")

    # مرحلة الأحرف الواحدة
    text = "".join(LETTER_MAP.get(ch, ch) for ch in s)

    # دمج حروف العلة المتكررة المتتالية
    text = re.sub(r"([اييو])\1+", r"\1", text)

    # حرف العلة الابتدائي e/i -> إ
    first = normalize(src)[:1]
    if first in ("e", "i") and text:
        text = "إ" + text[1:]
    # حرف العلة الابتدائي o/u -> و
    if first in ("o", "u") and text and text[0] != "و" and text[0] != "أ":
        text = "و" + text

    return text


def main():
    # 1) قراءة الإكسل
    wb = load_workbook(XLSX, read_only=True)
    ws = wb["القاموس الكامل"]

    entries = []
    from_manual = 0
    generated = 0
    by_level = {}

    for row in ws.iter_rows(values_only=True):
        if not row or len(row) < 9:
            continue
        row_id = row[0]
        if not isinstance(row_id, (int, float)):
            continue
        level = str(row[1] or "").strip()
        word = str(row[2] or "").strip()
        translation = str(row[3] or "").strip()
        example = str(row[4] or "").strip()
        example_tr = str(row[5] or "").strip()
        pos = str(row[6] or "").strip()
        base = str(row[7] or "").strip()
        form = str(row[8] or "").strip()

        if not word:
            continue

        if normalize(word) in MANUAL_PHONETICS:
            phonetic = MANUAL_PHONETICS[normalize(word)]
            from_manual += 1
        else:
            phonetic = transliterate(word)
            generated += 1

        entries.append({
            "id": int(row_id),
            "word": word,
            "phonetic": phonetic,
            "pos": pos,
            "translation": translation,
            "level": level,
            "example": example,
            "exampleTr": example_tr,
            "base": base,
            "form": form,
        })
        by_level[level] = by_level.get(level, 0) + 1

    # 2) كتابة الناتج
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))

    # 3) تقرير
    total = len(entries)
    print("=== تقرير البناء ===")
    print(f"المجموع: {total} كلمة")
    print(f"نطق اليد المثبت: {from_manual}")
    print(f"نطق مولّد قواعدياً: {generated}")
    print("توزيع المستويات:")
    for level in sorted(by_level):
        print(f"  {level}: {by_level[level]}")
    print(f"الملف: {OUT}")
    print("عينات النطق:")
    for e in entries[:10]:
        print(f"  {e['word']!r} -> {e['phonetic']!r}  ({e['translation'][:25]})")


if __name__ == "__main__":
    main()
