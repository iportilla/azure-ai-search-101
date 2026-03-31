"""Generate one PDF per product from product_data_flat.json into a pdfs/ sub-directory."""

import json
import os
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
JSON_FILE = BASE_DIR / "product_data_flat.json"
PDF_DIR = BASE_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

# ── Palette ────────────────────────────────────────────────────────────────────
BRAND_BLUE = colors.HexColor("#1B4F8A")
BRAND_ORANGE = colors.HexColor("#E87722")
LIGHT_GREY = colors.HexColor("#F5F7FA")
MID_GREY = colors.HexColor("#C8CFD8")
DARK_GREY = colors.HexColor("#4A5568")
WHITE = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

style_brand = ParagraphStyle(
    "Brand",
    fontName="Helvetica-Bold",
    fontSize=9,
    textColor=WHITE,
    leading=12,
    spaceAfter=0,
)
style_sku = ParagraphStyle(
    "SKU",
    fontName="Helvetica",
    fontSize=8,
    textColor=colors.HexColor("#BDC6D4"),
    leading=10,
)
style_title = ParagraphStyle(
    "Title",
    fontName="Helvetica-Bold",
    fontSize=20,
    textColor=BRAND_BLUE,
    leading=24,
    spaceBefore=4,
    spaceAfter=6,
)
style_section_label = ParagraphStyle(
    "SectionLabel",
    fontName="Helvetica-Bold",
    fontSize=8,
    textColor=BRAND_ORANGE,
    leading=10,
    spaceBefore=12,
    spaceAfter=2,
    textTransform="uppercase",
)
style_body = ParagraphStyle(
    "Body",
    fontName="Helvetica",
    fontSize=11,
    textColor=DARK_GREY,
    leading=16,
    spaceAfter=4,
)
style_cat_pill = ParagraphStyle(
    "CatPill",
    fontName="Helvetica-Bold",
    fontSize=9,
    textColor=BRAND_BLUE,
    leading=12,
)
style_footer = ParagraphStyle(
    "Footer",
    fontName="Helvetica",
    fontSize=7,
    textColor=MID_GREY,
    leading=10,
    alignment=1,  # centre
)


def stock_label(level: int) -> tuple[str, colors.Color]:
    """Return a human-readable stock label and colour."""
    if level == 0:
        return "OUT OF STOCK", colors.HexColor("#E53E3E")
    if level <= 10:
        return f"LOW STOCK  ({level} units)", colors.HexColor("#DD6B20")
    if level <= 30:
        return f"LIMITED  ({level} units)", colors.HexColor("#D69E2E")
    return f"IN STOCK  ({level} units)", colors.HexColor("#276749")


def build_pdf(product: dict, output_path: Path) -> None:
    """Render a single product PDF."""
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=0,          # header sits flush at the top
        bottomMargin=1.5 * cm,
    )

    W = A4[0] - 4 * cm   # usable width

    story = []

    # ── Header banner ──────────────────────────────────────────────────────────
    header_data = [
        [
            Paragraph("ZAVA Hardware &amp; Home Improvement", style_brand),
            Paragraph(f"SKU: {product['sku']}", style_sku),
        ]
    ]
    header_table = Table(header_data, colWidths=[W * 0.65, W * 0.35])
    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BRAND_BLUE),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (0, -1), 14),
                ("RIGHTPADDING", (-1, 0), (-1, -1), 14),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 0.5 * cm))

    # ── Product name ───────────────────────────────────────────────────────────
    story.append(Paragraph(product["name"], style_title))

    # ── Horizontal rule ────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=2, color=BRAND_ORANGE, spaceAfter=12))

    # ── Price & stock: two-column summary card ─────────────────────────────────
    stock_text, stock_colour = stock_label(product.get("stock_level", 0))

    price_cell = Table(
        [[Paragraph(f"${product['price']:,.2f}", ParagraphStyle(
            "Price",
            fontName="Helvetica-Bold",
            fontSize=26,
            textColor=BRAND_BLUE,
            leading=30,
        ))]],
        colWidths=[W * 0.45],
    )
    price_cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("BOX", (0, 0), (-1, -1), 1, MID_GREY),
    ]))

    stock_cell = Table(
        [[Paragraph(stock_text, ParagraphStyle(
            "Stock",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=stock_colour,
            leading=18,
        ))]],
        colWidths=[W * 0.50],
    )
    stock_cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("BOX", (0, 0), (-1, -1), 1, MID_GREY),
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    summary_row = Table([[price_cell, stock_cell]], colWidths=[W * 0.48, W * 0.52])
    summary_row.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(summary_row)

    # ── Description ────────────────────────────────────────────────────────────
    story.append(Paragraph("Description", style_section_label))
    story.append(Paragraph(product.get("description", ""), style_body))

    # ── Categories ─────────────────────────────────────────────────────────────
    cats = product.get("categories", [])
    if cats:
        story.append(Paragraph("Categories", style_section_label))
        pill_cells = []
        for cat in cats:
            pill_cells.append(
                Table(
                    [[Paragraph(cat, style_cat_pill)]],
                    colWidths=None,
                )
            )
            # Style each pill
            pill_cells[-1].setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 1, BRAND_BLUE),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))

        # Lay pills in a single row table (they wrap naturally since each is a Table)
        pill_row_data = [pill_cells]
        col_w = W / max(len(cats), 1)
        pill_row = Table(pill_row_data, colWidths=[col_w] * len(cats))
        pill_row.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(pill_row)

    # ── Spec table ─────────────────────────────────────────────────────────────
    story.append(Paragraph("Product Specifications", style_section_label))

    spec_style = ParagraphStyle("Spec", fontName="Helvetica", fontSize=10, textColor=DARK_GREY, leading=14)
    spec_label = ParagraphStyle("SpecLabel", fontName="Helvetica-Bold", fontSize=10, textColor=BRAND_BLUE, leading=14)

    spec_data = [
        [Paragraph("SKU", spec_label), Paragraph(product["sku"], spec_style)],
        [Paragraph("Price (USD)", spec_label), Paragraph(f"${product['price']:,.2f}", spec_style)],
        [Paragraph("Stock Level", spec_label), Paragraph(str(product.get("stock_level", "N/A")), spec_style)],
        [Paragraph("Category Path", spec_label), Paragraph(" › ".join(cats), spec_style)],
    ]

    spec_table = Table(spec_data, colWidths=[W * 0.30, W * 0.70])
    spec_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 1, MID_GREY),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, MID_GREY),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(spec_table)

    story.append(Spacer(1, 0.8 * cm))

    # ── Footer ─────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY, spaceAfter=6))
    story.append(
        Paragraph(
            f"Zava Hardware &amp; Home Improvement · {product['sku']} · "
            "All prices in USD · Subject to change without notice",
            style_footer,
        )
    )

    doc.build(story)


def main() -> None:
    with open(JSON_FILE, encoding="utf-8") as f:
        products = json.load(f)

    total = len(products)
    print(f"Generating {total} PDFs into {PDF_DIR} ...")

    for i, product in enumerate(products, 1):
        sku = product.get("sku", f"product_{i}")
        output_path = PDF_DIR / f"{sku}.pdf"
        build_pdf(product, output_path)
        if i % 50 == 0 or i == total:
            print(f"  [{i}/{total}] {sku}.pdf")

    print(f"\n✓ Done — {total} PDFs written to {PDF_DIR}/")


if __name__ == "__main__":
    main()
