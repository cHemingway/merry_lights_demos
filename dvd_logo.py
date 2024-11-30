from PIL import Image, ImageDraw

# Open the images
overlay = Image.open("template2.png").convert("RGBA")
dvd_logo = Image.open("DVD_32x14.png").convert("RGBA")


def draw_dvd_logo(x, y, color):
    # Create a new image for the result
    result = Image.new("RGBA", overlay.size, color=(0, 0, 0, 255))

    # Paste the overlay onto the result
    result.paste(overlay.copy(), (0, 0))

    # Recolor the DVD logo by replacing black pixels with the specified color
    dvd_logo_recolored = dvd_logo.copy()
    draw = ImageDraw.Draw(dvd_logo_recolored)
    width, height = dvd_logo_recolored.size
    for i in range(width):
        for j in range(height):
            if dvd_logo_recolored.getpixel((i, j)) == (0, 0, 0, 255):
                draw.point((i, j), fill=color)

    # Paste the recolored logo onto the result with alpha blending
    result.paste(dvd_logo_recolored, (x, y), dvd_logo_recolored)

    # Save or show the result
    return result



# Define the boundaries of the overlay for the DVD logo to bounce off
xmin, xmax = 16, 111
ymin, ymax = 52, 98
# Calculate the initial position to place the logo in the center of the overlay
position = (xmax-xmin)//2 + xmin, (ymax-ymin)//2 + ymin

logo_width, logo_height = dvd_logo.size

# Define the initial position and velocity of the DVD logo
x, y = position
vx, vy = 3, 1

# Define the different colors to cycle through
colors = [
          (210, 3, 5, 255),
          (207, 169, 0, 255),
          (40, 153, 83, 255),
          (0, 170, 211, 255),
          (139, 44, 160, 255),
          (211, 86, 3, 255),
          (255, 255, 0, 255)]

# Loop to animate the bouncing DVD logo
n_frames = 1000
frames = []
color_index = 0
for i in range(n_frames):
    # Update the position based on the velocity
    x += vx
    y += vy

    # Check for collision with the boundaries and update the velocity and color
    if x <= xmin or x + logo_width >= xmax:
        vx *= -1
        color_index = (color_index + 1) % len(colors)
    if y <= ymin or y + logo_height >= ymax:
        vy *= -1
        color_index = (color_index + 1) % len(colors)

    # Draw the DVD logo at the updated position with the current color
    result_image = draw_dvd_logo(x, y, colors[color_index])

    # Append the frame to the list
    frames.append(result_image)

# Save the frames as an animated GIF
# Disposal=2 is needed to avoid smear, see https://legacy.imagemagick.org/Usage/anim_basics/#background
frames[0].save("dvd_logo.gif", save_all=True, append_images=frames[1:], 
               loop=0, duration=100, disposal=2,
               transparency=0, optimize=True)