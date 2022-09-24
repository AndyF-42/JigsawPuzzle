from PIL import Image
import numpy as np
import math
import random

def random_img(output, width, height):
    #array = np.random.randint(0,256, (height,width,3)) 
    array = np.array([[[i, 125, 125] for i in range(50, (width*5)-50, 5)]] * height, dtype=np.uint8)
    # print(array)
    img = Image.fromarray(array)
    img.save(output)
    # print(img.width, img.height)
    return array

def simple_jigsaw(w, h):
    # # CHOOSING A SIZE
    MIN_PIXELS = 30
    
    gcd = math.gcd(w, h)
    a = int(w / gcd)
    b = int(h / gcd)
    
    max_amp = int(w / MIN_PIXELS / a)
    for i in range(1, max_amp + 1):
        if w / (i * a) == w // (i * a):
            print(str(i) + ": " + str(i * i * a * b))
    amp = 5  # later get user input
    
    # fill with zeros
    array = np.zeros((h, w), dtype=int)

    # add the puzzle pieces
    piece_width = int(w / amp / a)
    for row in range(amp * b):
        for col in range(amp * a):
            # initial square piece
            array[(row * piece_width):((row+1) * piece_width),
                    (col * piece_width):((col+1) * piece_width)] = row * (a * amp) + col
            
            # adding a bump left or right
            if col != 0:
                in_out = random.randint(0, 1)
                if in_out == 1:
                    array[(row * piece_width + 30):(row * piece_width + 50),
                            (col * piece_width):(col * piece_width + 20)] = row * (a * amp) + (col-1)
                else:
                    array[(row * piece_width + 30):(row * piece_width + 50),
                            (col * piece_width - 20):(col * piece_width)] = row * (a * amp) + col
            
            # adding a bump up or down
            if row != 0:
                in_out = random.randint(0, 1)
                if in_out == 1:
                    array[(row * piece_width):(row * piece_width + 20),
                            (col * piece_width + 30):(col * piece_width + 50)] = (row-1) * (a * amp) + col
                else:
                    array[(row * piece_width - 20):(row * piece_width),
                            (col * piece_width + 30):(col * piece_width + 50)] = row * (a * amp) + col

    # # convert to jigsaw image to check
    # random_colors = np.random.randint(0, 256, (amp * amp * a * b, 3))
    # jigsaw_array = np.zeros((h, w, 3), dtype=np.uint8)
    # for row in range(len(array)):
    #     for col in range(len(array[0])):
    #         jigsaw_array[row, col] = random_colors[array[row, col]]
    # img = Image.fromarray(jigsaw_array)
    # img.save("new_jigsaw.png")

    return array

def cut_pieces(original, jigsaw, num_pieces, piece_width, bump_width, num_cols, output):

    print(original.shape)
    print(jigsaw.shape)

    piece_images = []

    for i in range(num_pieces):
        piece_images.append(Image.new(mode="RGBA",
            size=(piece_width + 2 * bump_width, piece_width + 2 * bump_width), color=(0,0,0,0)))

    for row in range(len(jigsaw)):
        for col in range(len(jigsaw[0])):
            piece_row = int(jigsaw[row, col] / num_cols)
            piece_col = jigsaw[row, col] % num_cols
            piece_images[jigsaw[row, col]].putpixel(
                (col - (piece_col * piece_width) + bump_width, row - (piece_row * piece_width) + bump_width), tuple(original[row, col]))
    
    for i, img in enumerate(piece_images):
        img.save(output + "/piece_" + str(i) + ".png")

def main():
    jigsaw_array = simple_jigsaw(1600, 1200)
    cut_pieces(np.asarray(Image.open("better_test.jpg")), jigsaw_array, 300, 80, 20, 20, 'pieces')
    
    
    # original_array = random_img('original.png', 50, 25)
    # jigsaw_array = simple_jigsaw('jigsaw.png')
    # cut_pieces(original_array, jigsaw_array, 'pieces')


if __name__ == "__main__":
    main()