#!/usr/bin/env python3
"""
Create macOS Application Icon for README Editor
Generates a high-resolution icon with an open-book design
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_icon():
    """Create a modern icon for README Editor"""

    # Create high-resolution image for icon (1024x1024 for macOS)
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background with rounded corners and gradient effect
    margin = 80
    bg_rect = [margin, margin, size - margin, size - margin]

    # Draw rounded rectangle background
    corner_radius = 120
    draw.rounded_rectangle(bg_rect, corner_radius,
                           fill=(45, 55, 72, 255))  # Dark blue-gray

    # Add subtle border
    border_margin = margin - 10
    border_rect = [
        border_margin, border_margin, size - border_margin,
        size - border_margin
    ]
    draw.rounded_rectangle(border_rect,
                           corner_radius + 10,
                           outline=(200, 200, 200, 100),
                           width=8)

    # Draw an open book (two facing pages)
    book_width = 800
    book_height = 760
    book_x0 = (size - book_width) // 2
    book_y0 = (size - book_height) // 2 + 40
    book_x1 = book_x0 + book_width
    book_y1 = book_y0 + book_height

    # Book drop shadow
    shadow_offset = 14
    draw.rounded_rectangle(
        [book_x0 + shadow_offset, book_y0 + shadow_offset, book_x1 + shadow_offset, book_y1 + shadow_offset],
        40,
        fill=(0, 0, 0, 60),
    )

    # Pages
    center_x = (book_x0 + book_x1) // 2
    gutter = 14
    left_page = [book_x0, book_y0, center_x - gutter, book_y1]
    right_page = [center_x + gutter, book_y0, book_x1, book_y1]
    draw.rounded_rectangle(left_page, 36, fill=(255, 255, 255, 255))
    draw.rounded_rectangle(right_page, 36, fill=(255, 255, 255, 255))

    # Inner gutter/spine shading
    spine_rect = [center_x - gutter, book_y0 + 10, center_x + gutter, book_y1 - 10]
    draw.rounded_rectangle(spine_rect, 18, fill=(220, 225, 235, 255))
    draw.line([(center_x, book_y0 + 18), (center_x, book_y1 - 18)], fill=(200, 205, 215, 255), width=3)

    # Outer page edge shading
    edge_w = 10
    draw.rectangle([book_x0, book_y0 + 16, book_x0 + edge_w, book_y1 - 16], fill=(235, 240, 245, 255))
    draw.rectangle([book_x1 - edge_w, book_y0 + 16, book_x1, book_y1 - 16], fill=(235, 240, 245, 255))

    # Page content lines (left and right)
    def page_lines(x0, x1, y_start, rows, color=(228, 234, 242, 255)):
        y = y_start
        for _ in range(rows):
            draw.rounded_rectangle([x0, y, x1, y + 12], 6, fill=color)
            y += 26

    pad_x = 36
    pad_top = 48
    # Left page header bar
    draw.rounded_rectangle([left_page[0] + pad_x, left_page[1] + pad_top, center_x - gutter - pad_x, left_page[1] + pad_top + 20], 10, fill=(225, 232, 240, 255))
    page_lines(left_page[0] + pad_x, center_x - gutter - pad_x, left_page[1] + pad_top + 48, 10)

    # Right page header bar
    draw.rounded_rectangle([center_x + gutter + pad_x, right_page[1] + pad_top, right_page[2] - pad_x, right_page[1] + pad_top + 20], 10, fill=(225, 232, 240, 255))
    page_lines(center_x + gutter + pad_x, right_page[2] - pad_x, right_page[1] + pad_top + 48, 10)

    # Bookmark ribbon at top center
    ribbon_w = 36
    ribbon_h = 140
    rx = center_x - ribbon_w // 2
    ry = book_y0 - 8
    draw.rectangle([rx, ry, rx + ribbon_w, ry + ribbon_h], fill=(30, 144, 255, 255))
    draw.polygon([(rx, ry + ribbon_h), (rx + ribbon_w // 2, ry + ribbon_h + 22), (rx + ribbon_w, ry + ribbon_h)], fill=(30, 144, 255, 255))

    return img


def create_icon_set():
    """Create a complete icon set for macOS"""

    base_icon = create_icon()

    # Icon sizes for macOS
    sizes = [16, 32, 64, 128, 256, 512, 1024]

    # Create icons directory
    if not os.path.exists("icons"):
        os.makedirs("icons")

    for size in sizes:
        # Resize image with high quality
        resized = base_icon.resize((size, size), Image.Resampling.LANCZOS)

        # Save as PNG
        filename = f"icons/readme_editor_{size}x{size}.png"
        resized.save(filename, "PNG")
        print(f"Created {filename}")

    # Save the main icon
    base_icon.save("icons/readme_editor.png", "PNG")
    print("Created icons/readme_editor.png")

    # Create ICO file for cross-platform compatibility
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128),
                 (256, 256)]
    ico_images = []

    for size in ico_sizes:
        resized = base_icon.resize(size, Image.Resampling.LANCZOS)
        ico_images.append(resized)

    # Save as ICO
    ico_images[0].save("icons/readme_editor.ico", format="ICO", sizes=ico_sizes)
    print("Created icons/readme_editor.ico")

    print("\nIcon set created successfully!")
    print("For macOS app bundle, use the PNG files.")
    print("For cross-platform compatibility, use the ICO file.")


if __name__ == "__main__":
    create_icon_set()
