import base64

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PIL import Image
import numpy as np

webdriver_path = r"C:\Users\biomi\Desktop\chromedriver_win32\chromedriver.exe"

grid_height = 31
grid_width = 28
grid_height_padded = 36
grid_pad_top = 3
grid_pad_bottom = 2


def log(msg: str):
    print(msg)


def save_random_map_png(img_filename: str):
    log("Configuring webdriver...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')

    log("Opening the webdriver in headless mode...")
    chrome = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)

    log("Getting the image...")
    chrome.get("https://shaunlebron.github.io/pacman-mazegen/tetris/many.htm")
    canvas = chrome.find_element_by_id('canvas')

    log("Saving the image...")
    js = "return arguments[0].toDataURL('image/png').substring(21);"
    canvas_b64 = chrome.execute_script(js, canvas)
    canvas_png = base64.b64decode(canvas_b64)
    with open(img_filename, 'wb') as doc:
        doc.write(canvas_png)


def is_empty(pix, x: int, y: int):
    off = 2
    x_coord_start = x*8 + off
    x_coord_end = (x + 1)*8 - off
    y_coord_start = y*8 + off
    y_coord_end = (y + 1)*8 - off

    top = pix[y_coord_start, x_coord_start:x_coord_end]
    bottom = pix[y_coord_end, x_coord_start:x_coord_end]
    left = pix[y_coord_start:y_coord_end, x_coord_start]
    right = pix[y_coord_start:y_coord_end, x_coord_end]
    return all(np.array_equal(px, [0, 0, 0, 255]) for seg in [top, bottom, left, right] for px in seg)


def get_xy(grid_x: int, grid_y: int, x: int, y: int):
    return x + grid_x*grid_width, y + grid_y*grid_height_padded


def print_map(pix, grid_x: int, grid_y: int):
    for y in range(grid_pad_top, grid_height_padded-grid_pad_bottom):
        for x in range(28):
            print(' ' if is_empty(pix, *get_xy(grid_x, grid_y, x, y)) else 'X', end=' ')
        print()


def print_grid(grid):
    for y in range(grid_height):
        for x in range(grid_width):
            print(' ' if not grid[y, x] else 'X', end=' ')
        print()


def save_grid(filename: str, pix, grid_x: int, grid_y: int):
    arr = np.empty((grid_height, grid_width), np.bool)

    for y_arr, y_map in enumerate(range(grid_pad_top, grid_height_padded-grid_pad_bottom)):
        for x_arr, x_map in enumerate(range(grid_width)):
            arr[y_arr, x_arr] = not is_empty(pix, *get_xy(grid_x, grid_y, x_map, y_map))

    xp = np.packbits(arr)

    with open(filename, 'wb') as doc:
        doc.write(xp.tobytes())


def get_grid(filename: str):
    with open(filename, 'rb') as doc:
        xp = np.frombuffer(doc.read(), dtype=np.uint8)

    arr = np.unpackbits(xp)[:-4]
    return np.reshape(arr, (grid_height, grid_width))


def parse_maze_png(img_filename: str, grid_filename: str, grid_x: int, grid_y: int):
    pic = Image.open(img_filename)
    pix = np.array(pic)
    save_grid(grid_filename, pix, grid_x, grid_y)
    return get_grid(grid_filename)


def _main():
    img_filename = 'mazes.png'
    grid_filename = 'grid.pac'
    grid = parse_maze_png(img_filename, grid_filename, 0, 0)
    print_grid(grid)


if __name__ == '__main__':
    _main()
