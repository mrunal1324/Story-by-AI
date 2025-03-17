import time
from PIL import Image, ImageDraw, ImageFont
import random
import os
import textwrap

def generate_image(prompt, story_text=None):
    """
    Generate a simple abstract image based on the story prompt.
    This is a lightweight alternative to using Stable Diffusion.
    
    Args:
        prompt (str): The user's story prompt
        story_text (str, optional): The generated story text
        
    Returns:
        Image: A generated abstract image
    """
    start_time = time.time()
    
    # Create a seed from the prompt for consistency
    seed = sum(ord(c) for c in prompt)
    random.seed(seed)
    
    # Create a canvas
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color=(
        random.randint(0, 50),
        random.randint(0, 50),
        random.randint(0, 50)
    ))
    
    draw = ImageDraw.Draw(image)
    
    # Generate abstract shapes based on the prompt
    num_shapes = random.randint(10, 30)
    
    # Extract colors from the prompt
    colors = []
    color_words = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'white', 'black']
    for word in prompt.lower().split():
        if word in color_words:
            if word == 'red':
                colors.append((random.randint(150, 255), random.randint(0, 50), random.randint(0, 50)))
            elif word == 'blue':
                colors.append((random.randint(0, 50), random.randint(0, 50), random.randint(150, 255)))
            elif word == 'green':
                colors.append((random.randint(0, 50), random.randint(150, 255), random.randint(0, 50)))
            elif word == 'yellow':
                colors.append((random.randint(200, 255), random.randint(200, 255), random.randint(0, 50)))
            elif word == 'purple':
                colors.append((random.randint(100, 200), random.randint(0, 50), random.randint(100, 200)))
            elif word == 'orange':
                colors.append((random.randint(200, 255), random.randint(100, 150), random.randint(0, 50)))
            elif word == 'pink':
                colors.append((random.randint(200, 255), random.randint(100, 150), random.randint(150, 200)))
            elif word == 'white':
                colors.append((random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)))
            elif word == 'black':
                colors.append((random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)))
    
    # If no colors were found in the prompt, use random colors
    if not colors:
        for _ in range(5):
            colors.append((
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            ))
    
    # Draw shapes
    for _ in range(num_shapes):
        shape_type = random.choice(['circle', 'rectangle', 'line'])
        color = random.choice(colors)
        
        if shape_type == 'circle':
            center_x = random.randint(0, width)
            center_y = random.randint(0, height)
            radius = random.randint(20, 100)
            draw.ellipse(
                (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                fill=color,
                outline=(255, 255, 255, 128)
            )
        elif shape_type == 'rectangle':
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = x1 + random.randint(50, 200)
            y2 = y1 + random.randint(50, 200)
            draw.rectangle(
                (x1, y1, x2, y2),
                fill=color,
                outline=(255, 255, 255, 128)
            )
        elif shape_type == 'line':
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line(
                (x1, y1, x2, y2),
                fill=color,
                width=random.randint(2, 10)
            )
    
    # Add a title based on the prompt
    try:
        # Try to find a suitable font
        font_path = None
        possible_font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
            '/Library/Fonts/Arial.ttf',  # macOS
            'C:\\Windows\\Fonts\\Arial.ttf',  # Windows
            'arial.ttf'  # Fallback
        ]
        
        for path in possible_font_paths:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            title_font = ImageFont.truetype(font_path, 30)
            # Wrap the title text
            title = prompt if len(prompt) < 50 else prompt[:47] + "..."
            wrapped_title = textwrap.fill(title, width=40)
            
            # Add a semi-transparent background for the title
            title_width, title_height = draw.textbbox((0, 0), wrapped_title, font=title_font)[2:]
            draw.rectangle(
                (20, 20, width - 20, 20 + title_height + 20),
                fill=(0, 0, 0, 128)
            )
            
            # Draw the title
            draw.text(
                (width // 2, 30),
                wrapped_title,
                font=title_font,
                fill=(255, 255, 255),
                anchor="mt"  # Middle top
            )
        else:
            # Fallback if no font is found
            print("No suitable font found for image title")
    except Exception as e:
        print(f"Error adding title to image: {e}")
    
    print(f"Image generation took {time.time() - start_time:.2f} seconds")
    return image