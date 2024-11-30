import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __(Image, colorsys, hueslider, math):
    # From https://rosettacode.org/wiki/Plasma_effect#Python
    def plasma (w, h, hueshift):
        out = Image.new("RGB", (w, h))
        pix = out.load()
        for x in range (w):
            for y in range(h):
                hue = 4.0 + math.sin(x / 19.0) + math.sin(y / 9.0) \
    				+ math.sin((x + y) / 25.0) + math.sin(math.sqrt(x**2.0 + y**2.0) / 8.0)
                hue = (hue+hueshift*8) % 8
                hsv = colorsys.hsv_to_rgb(hue/8.0, 1, 1)
                pix[x, y] = tuple([int(round(c * 255.0)) for c in hsv])
        return out

    w, h = 128, 128
    plasma(w,h, hueslider.value)
    return h, plasma, w


@app.cell(hide_code=True)
def __(mo):
    hueslider = mo.ui.slider(0, 1, 0.01)
    fps = mo.ui.slider(20, 60, 1, show_value=True)
    duration = mo.ui.slider(5, 20, 1, show_value=True)
    mo.md(f"""Hue {hueslider} 
              FPS {fps}
              Duration {duration} seconds
            """
         )
    return duration, fps, hueslider


@app.cell
def __(Image, duration, fps, h, mo, plasma, w):
    n_frames = fps.value * duration.value
    overlay = Image.open("template2.png")
    frames = [plasma(w,h, s/n_frames) for s in range(0,n_frames)]
    [f.paste(overlay, (0,0), overlay) for f in frames]
    im = frames[0]
    im.save("plasma_overlay.gif", save_all=True, append_images=frames[1:], duration=int(1/fps.value), loop=0)
    mo.image("plasma_overlay.gif")
    return frames, im, n_frames, overlay


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""### Scale this up for preview""")
    return


@app.cell
def __(Image, fps, frames, h, mo, w):
    larger_frames = [f.resize((w*2, h*2), Image.NEAREST) for f in frames]
    larger = larger_frames[0]
    larger.save("larger.gif", save_all=True, append_images=larger_frames[1:], duration=int(1/fps.value), loop=0)
    mo.image("larger.gif", width=w*4, height=h*4)
    return larger, larger_frames


@app.cell(hide_code=True)
def __():
    import marimo as mo
    import math
    import colorsys
    from PIL import Image
    return Image, colorsys, math, mo


if __name__ == "__main__":
    app.run()
