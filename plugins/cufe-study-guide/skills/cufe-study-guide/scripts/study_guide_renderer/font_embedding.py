"""Embed freely distributable runtime DejaVu fonts in OOXML; no repo font files."""

import hashlib
import uuid
import zipfile
from xml.etree import ElementTree as ET

from matplotlib.ft2font import FT2Font

from .theme import font_files

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"


def embed_fonts(path):
    with zipfile.ZipFile(path) as package:
        entries = {name: package.read(name) for name in package.namelist()}
    fonts = ET.fromstring(entries["word/fontTable.xml"])
    relationships = ET.Element("{" + PR + "}Relationships")
    families = {}
    slots = {"body": ("DejaVu Sans", "embedRegular"), "bold": ("DejaVu Sans", "embedBold"),
             "italic": ("DejaVu Sans", "embedItalic"), "bold_italic": ("DejaVu Sans", "embedBoldItalic"),
             "mono": ("DejaVu Sans Mono", "embedRegular"), "mono_bold": ("DejaVu Sans Mono", "embedBold")}
    for key, filename in font_files().items():
        if FT2Font(str(filename)).get_sfnt_table("OS/2")["fsType"] != 0:
            raise ValueError(f"Runtime font does not allow unrestricted embedding: {filename}")
        family, slot = slots[key]
        if family not in families:
            families[family] = ET.SubElement(fonts, "{" + W + "}font", {"{" + W + "}name": family})
        font_data = bytearray(filename.read_bytes())
        guid = uuid.UUID(hashlib.sha256(font_data).hexdigest()[:32])
        mask = guid.bytes[::-1]
        for i in range(32):
            font_data[i] ^= mask[i % 16]
        target = f"fonts/{key}.odttf"
        rid = "rIdSG" + key
        entries["word/" + target] = bytes(font_data)
        ET.SubElement(relationships, "{" + PR + "}Relationship", {"Id": rid, "Target": target, "Type": R + "/font"})
        ET.SubElement(families[family], "{" + W + "}" + slot, {"{" + R + "}id": rid, "{" + W + "}fontKey": "{" + str(guid).upper() + "}"})
    entries["word/fontTable.xml"] = ET.tostring(fonts, encoding="utf-8", xml_declaration=True)
    entries["word/_rels/fontTable.xml.rels"] = ET.tostring(relationships, encoding="utf-8", xml_declaration=True)
    types = ET.fromstring(entries["[Content_Types].xml"])
    ET.SubElement(types, "{" + CT + "}Default", {"Extension": "odttf", "ContentType": "application/vnd.openxmlformats-officedocument.obfuscatedFont"})
    entries["[Content_Types].xml"] = ET.tostring(types, encoding="utf-8", xml_declaration=True)
    settings = ET.fromstring(entries["word/settings.xml"])
    ET.SubElement(settings, "{" + W + "}embedTrueTypeFonts")
    entries["word/settings.xml"] = ET.tostring(settings, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for name, data in entries.items():
            item = zipfile.ZipInfo(name, date_time=(2000, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            package.writestr(item, data)
