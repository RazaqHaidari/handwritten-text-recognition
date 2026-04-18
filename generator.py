from PIL import Image, ImageDraw, ImageFont, ImageColor

def generate_image(text, font_size=28, color="#0000ff", line_spacing=10):

    width, height = 900, 1200
    image = Image.new("RGB", (width, height), "white")

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

  
    fill_color = ImageColor.getrgb(color)

    y = 50

    for line in text.split("\n"):
        draw.text((50, y), line, fill=fill_color, font=font)
        y += font_size + line_spacing

    output_path = "static/output.png"
    image.save(output_path)

    return output_path