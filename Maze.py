
def make_maze_list(all_spacings: list[list])->list[list]:
    ret_list = list()
    for i, x_spacings in enumerate(all_spacings):
        ret_list.append(list())
        for value in x_spacings:
            if i % 2 == 0:
                ret_list[-1].extend([0 for _ in range((value - 1) * 2 + 1)])
                ret_list[-1].append(1)
            else:
                ret_list[-1].extend([1 for _ in range((value) * 2)])
                ret_list[-1].extend([0,1])
        if i % 2 == 1:
            ret_list[-1].pop(-1)
            ret_list[-1].pop(-1)
    return ret_list


maze_list = make_maze_list([
    [7,5,5,3],
    [3,2,2,1,4,0,0,1],
    [4,2,2,2,1,3,3,1,2],
    [0,4,1,0,1,2,0,2,1,0],
    [3,4,2,5,5,1],
    [2,1,4,3,5,0],
    [2,2,5,1,3,7],
    [0,0,1,4,0,0,1,4,2],
    [1,3,2,2,1,1,1,2,2,3,2],
    [0,3,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [1,3,1,2,1,2,1,1,2,1,2,2,1],
    [0,0,1,0,2,2,0,2,2,1,0],
    [1,2,2,6,3,4,2],


])

class Maze:
    _maze_array: list[list]
    WIDTH: int
    HEIGHT: int
    _GOAL: tuple[int, int]
    START: tuple[int, int]

    def __init__(self, array: list[list], goal: tuple[int, int], start: tuple[int, int] = (0, 0)):
        self._maze_array = list()
        self.WIDTH = len(array[0])
        self.HEIGHT = len(array)
        self._GOAL = goal
        self.START = start
        for row in array:
            self._maze_array.append(row[:])
            if len(row) != self.WIDTH:
                raise ValueError("All rows must be equal in length")
        self._maze_array[goal[1]][goal[0]] = 2
    def is_wall(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return True
        return True if self._maze_array[y][x] == 1 else False

    def is_goal(self, x, y):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return False
        if self._maze_array[y][x] == 2:
            return True
        return False

    def print_array(self):
        for row, value in enumerate(self._maze_array):
            for col, value in enumerate(value):
                if col == self._GOAL[0] and row == self._GOAL[1]:
                    print(9, end=" ")
                else:
                    print(value, end=" ")
            print()

    def get_array(self) -> list[list[int]]:
        return [row[:] for row in self._maze_array]


