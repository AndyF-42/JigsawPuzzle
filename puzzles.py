import pygame

class Piece:
    SNAPPING_DISTANCE = 50

    def __init__(self, id, image, x, y, dragging):
        self.id = id
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.bump_size = 20
        self.x = x
        self.y = y
        self.dragging = dragging

    def in_piece(self, x, y):
        return (x > self.x and x < (self.x + self.width) and
                y > self.y and y < (self.y + self.height))

    def move_to_mouse(self, click_x, click_y):
        x, y = pygame.mouse.get_pos()
        self.x += (x - click_x)
        self.y += (y - click_y)

    def true_x(self):
        return self.x + self.bump_size
    
    def true_y(self):
        return self.y + self.bump_size

    def true_width(self):
        return self.width - 2 * self.bump_size

    def true_height(self):
        return self.height - 2 * self.bump_size

    def check_snap(self, other_piece, puzzle_width):
        # other_piece to the left
        if self.id - other_piece.id == 1 and self.id % puzzle_width != 0: 
            if (abs(self.true_x() - (other_piece.true_x() + other_piece.true_width())) + 
                    abs(self.true_y() - other_piece.true_y())) < self.SNAPPING_DISTANCE:
                self.x = other_piece.true_x() + other_piece.true_width()
                self.y = other_piece.y
                return True

        # other_piece to the right
        elif self.id - other_piece.id == -1 and self.id % puzzle_width != (puzzle_width - 1): 
            if (abs((self.true_x() + self.true_width()) - other_piece.true_x()) + 
                    abs(self.true_y() - other_piece.true_y())) < self.SNAPPING_DISTANCE:
                self.x = other_piece.true_x() - self.true_width() - 2 * self.bump_size
                self.y = other_piece.y
                return True

        # other_piece above
        elif self.id - other_piece.id == puzzle_width:
            if (abs(self.true_x() - other_piece.true_x()) + 
                    abs(self.true_y() - (other_piece.true_y() + other_piece.true_height()))) < self.SNAPPING_DISTANCE:
                self.x = other_piece.x
                self.y = other_piece.true_y() + other_piece.true_height()
                return True

        # other_piece below
        elif self.id - other_piece.id == -puzzle_width:
            if (abs(self.true_x() - other_piece.true_x()) + 
                    abs((self.true_y() + self.true_height()) - other_piece.true_y())) < self.SNAPPING_DISTANCE:
                self.x = other_piece.x
                self.y = other_piece.true_y() - self.true_height() - 2 * self.bump_size
                return True

        return False
    

# class Chain:
#     pieces = set()

#     def __init__(self, pieces):
#         self.pieces.update(pieces)

def main():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PUZZLE_WIDTH = 20
    PUZZLE_HEIGHT = 15

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Puzzles!")
    clock = pygame.time.Clock()

    click_x = -1
    click_y = -1

    chains = []
    for i in range(PUZZLE_WIDTH * PUZZLE_HEIGHT):
        image = pygame.image.load("pieces/piece_" + str(i) + ".png")
        image = pygame.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))
        chains.append([Piece(i, image, 25 + i * 20, 100, False)]) # randomize

    running = True
    while running:
        clock.tick(60)

        # PYGAME EVENTS
        for event in pygame.event.get():
            
            # quit
            if event.type == pygame.QUIT:
                running = False
                break

            # mouse down, check if in piece for dragging
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                click_x = x
                click_y = y
                
                for chain in chains:
                    for piece in chain:
                        if piece.in_piece(x, y):
                            piece.dragging = True
                            break
                    else:
                        continue
                    break

            # mouse up, no longer dragging
            if event.type == pygame.MOUSEBUTTONUP:
                click_x = -1
                click_y = -1
                for chain in chains: # can optimize
                    for piece in chain:
                        if not piece.dragging:
                            continue

                        piece.dragging = False

                        for other_chain in chains:
                            if other_chain == chain:
                                continue
                                
                            for other_piece in other_chain:
                                if not piece.check_snap(other_piece, PUZZLE_WIDTH):
                                    continue
                                chain.extend(other_chain)
                                chains.remove(other_chain)
                                if len(chains) == 1:
                                    print("Yay you did it!")


        screen.fill((255, 255, 255))

        for chain in chains: # can optimize
            if all([not piece.dragging for piece in chain]):
                for piece in chain:
                    screen.blit(piece.image, (piece.x, piece.y))
                continue

            for piece in chain:
                piece.move_to_mouse(click_x, click_y)
                screen.blit(piece.image, (piece.x, piece.y))
            click_x, click_y = pygame.mouse.get_pos()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()