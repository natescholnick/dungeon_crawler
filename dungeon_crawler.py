from IPython.display import clear_output
from random import randint

class MonsterDungeon():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def showGrid(self, player, monster, door):
        p_coords = player.getCoords()
        m_coords = monster.getCoords()
        d_coords = door.getCoords()

        print(f'Player\'s Coords: {p_coords} \t Lives: {player.lives}')
        print(f'Monster\'s Coords: {m_coords}')
        print(f'Door\'s Coords: {d_coords}')

        for row in range(self.rows):
            print('+---'*self.cols + '+')

            for col in range(self.cols):
                if p_coords == [col, row] and col == self.cols -1:
                    print('| ' + u'\u263A' + ' ', end='|\n')
                elif p_coords == [col, row]:
                    print('| ' + u'\u263A' + ' ', end='')

                elif d_coords == [col, row] and col == self.cols -1:
                    print('| ' + u'\u272D' + ' ', end='|\n')
                elif d_coords == [col, row]:
                    print('| ' + u'\u272D' + ' ', end='')

                elif m_coords == [col, row] and col == self.cols -1:
                    print('| ' + u'\u2620' + ' ', end='|\n')
                elif m_coords == [col, row]:
                    print('| ' + u'\u2620' + ' ', end='')
                elif col == self.cols-1:
                    print('|   ', end='|\n')
                else:
                    print('|   ', end='')
            if row == self.rows-1:
                print('+---'*self.cols + '+')

    def checkCollision(self, ob1, ob2):
        if ob1.getCoords() == ob2.getCoords():
            return True
        else:
            return False

    def handleLoseCondition(self, player):
        if player.getLives() <= 0:
            print('HA! You\'re dead, idiot.')
            return True
        return False



class Character():
    def __init__(self, coords=[0,0]):
        self.coords = coords   # [x, y]

    def getCoords(self):
        return self.coords

    def randCoords(self, rows, cols):
        rand_row = randint(0, rows-1)
        if rand_row == 0:
            rand_col = randint(1, cols-1)
        else:
            rand_col = randint(1, cols-1)
        self.coords = [rand_row, rand_col]

class Player(Character):
    def __init__(self, coords=[0,0], lives=3):
        self.lives = lives
        super().__init__(coords)

    def getLives(self):
        return player.lives

    def loseLife(self):
        self.lives -= 1

    def move(self, rows, cols):
        '''
        Loop to ask player to move. Handle anything but up/down/left/right
        If they type 'quit' return True, else return False
        '''
        moved = False
        while not moved:
            print('Type \'QUIT\' at any time to stop playing. ')
            direction = input('Where would you like to move? ').lower()
            if direction == 'quit':
                return True
            elif direction == 'left':
                self.coords[0] -= 1
                self.coords[0] %= cols
                moved = True
            elif direction == 'right':
                self.coords[0] += 1
                self.coords[0] %= cols
                moved = True
            elif direction == 'up':
                self.coords[1] -= 1
                self.coords[1] %= rows
                moved = True
            elif direction == 'down':
                self.coords[1] += 1
                self.coords[1] %= rows
                moved = True
            else:
                print('Invalid move, try again!')

        return False


class Monster(Character):
    def __init__(self, coords=[0,0]):
        super().__init__(coords)

    def move(self, player, rows, cols):
        p_x, p_y = player.getCoords()[0], player.getCoords()[1]
        m_x, m_y = self.getCoords()[0], self.getCoords()[1]
        if p_x != m_x:
            if p_x - m_x > cols//2 or m_x > p_x:
                self.coords[0] -= 1
                self.coords[0] %= cols
            else:
                self.coords[0] += 1
                self.coords[0] %= cols
        else:
            if p_y - m_y > rows//2:
                self.coords[1] -= 1
                self.coords[1] %= rows
            else:
                self.coords[1] += 1
                self.coords[1] %= rows


# Define gloal game variables
level = 0
lives = 3
rows, cols = 4 + level, 4 + level
done = False

# main game loop that handles object resets
while not done:
    game = MonsterDungeon(rows, cols)
    player = Player()
    monster = Monster()
    monster.randCoords(rows, cols)
    door = Character()
    door.randCoords(rows, cols)
    playing = True
    won = False

    # main gameplay loop
    while playing:
        game.showGrid(player, monster, door)

        # handle user movement
        if player.move(rows, cols) == True:
            playing = False
            done = True

        # handle monster movement
        monster.move(player, rows, cols)

        clear_output()

        # check for collisions
        # winning condition
        if game.checkCollision(player, door) == True:
            print('Congrats! You beat the level!')
            playing = False
            won = True

        # player loses life, maybe lose
        elif game.checkCollision(player, monster)== True:
            player.loseLife()
            print('The monster just took  big bite out of you.')
            if game.handleLoseCondition(player):
                playing = False

    # Ask if they want to continue, increment level if won
    if not done:
        if won and input('Continue to the next level (y/n)?)' ).lower() == 'y':
            level += 1
            rows, cols = rows+level, cols+level
        elif not won and input('Would you like to try again (y/n)? ').lower() == 'y':
            continue
        else:
            done = True

clear_output()
print('Thanks for playing!')
