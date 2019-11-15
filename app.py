from tkinter import Tk, Frame, Button, TOP, BOTTOM, LEFT, RIGHT, Toplevel, IntVar, Entry
from numpy import random
import time

START_COLOR = 'yellow'
TARGET_COLOR = 'grey'
RANDOM_COLOR = 'orange'
WALKABLE_COLOR = 'white'
WALL_COLOR = 'black'


# NEIGHBORS_DIAG = [(1,1),(1,-1),(-1,1),(-1,-1)]
NEIGHBORS_DIRS = [(1,0), (-1,0), (0,1), (0,-1)]
# NEIGHBORS_DIRS = [(1,0), (-1,0), (0,1), (0,-1), (1,1),(1,-1),(-1,1),(-1,-1)]

def prim_maze_generator(r, c):
    # 0 is wall, 1 is walkable
    grid = [list(range(c)) for i in range(r)]
    for i in range(r):
        for j in range(c):
            grid[i][j] = 0
    walls = []
    starting_pos = (random.randint(0,r),random.randint(0,c))
    grid[starting_pos[0]][starting_pos[1]] = 1
    walls = get_neighbors(grid,starting_pos[0],starting_pos[1])

    while walls:
        index = random.randint(0,len(walls))
        w = walls[index]
        walls.remove(w)
        neighbors = get_neighbors(grid,w[0],w[1])
        neighbors = [x for x in neighbors if grid[x[0]][x[1]] != 0]
        if len(neighbors) == 1:
            t = neighbors[0]
            grid[w[0]][w[1]] = 1
            to_add = get_neighbors(grid,w[0],w[1])
            to_add = [x for x in to_add if grid[x[0]][x[1]] == 0]
            walls.extend(to_add)

    return grid


def remove_some_walls(grid, r, c):
    CHANCE = 0.05
    for i in range(r):
        for j in range(c):
            if random.uniform(0,1) <= CHANCE:
                grid[i][j] = 1

    return grid




def get_button_coords(button):
    gi = button.grid_info()
    # print(str(gi['row']) + " " + str(gi['column']))
    return (gi['row'], gi['column'])


def get_neighbors(a, r, c):
    neighbors = []
    for d in NEIGHBORS_DIRS:
        if 0 <= r + d[0] <= len(a)-1 and 0 <= c + d[1] <= len(a[0]) - 1:
            neighbors.append( (r + d[0], c + d[1]) )

    return neighbors




class MainScreen(Frame):
    def __init__(self, root, r, c):
        # Frame.__init__(self, root)
        # self.grid()
        #

        self.r = r
        self.c = c
        self.root = root
        self.tile = None
        self.btn_list = []
        self.start_tile = None
        self.target_tile = None

        top_frame = Frame(root)
        top_frame.pack(side=TOP)

        bottom_frame = Frame(root)
        bottom_frame.pack(side=BOTTOM)

        self.tf = top_frame

        # for row in range(r):
        #     for col in range(c):
        #         b = Button(top_frame, bg=WALKABLE_COLOR, width=2, height=1)
        #         b.configure(command=(lambda button=b: self.maze_tile_click(button)))
        #         b.grid(row=row, column=col)
        #         self.btn_list[row][col] = b

        self.build_maze(r, c)

        Button(bottom_frame, text='Set Source', bg=START_COLOR,
               command=(lambda: (self.set_tile_to_set(START_COLOR)))).pack(side=LEFT)
        Button(bottom_frame, text='Set Target', bg=TARGET_COLOR,
               command=(lambda: (self.set_tile_to_set(TARGET_COLOR)))).pack(side=LEFT)
        Button(bottom_frame, text='Resize Grid', bg='teal',
               command=(lambda: (self.resize_grid()))).pack(side=LEFT)

        Button(bottom_frame, text='Randomize Maze', bg=RANDOM_COLOR, command=(lambda: (self.randomize()))).pack(
            side=LEFT)
        Button(bottom_frame, text='Clear Maze', command=(lambda: (self.clear()))).pack(side=LEFT)

        Button(bottom_frame, text='BFS', command=(lambda: (self.bfs()))).pack(side=LEFT)

        Button(bottom_frame, text='Quit', width=6, command=lambda root=root: root.destroy()).pack(side=BOTTOM)


    def maze_tile_click(self, button):
        if self.tile is not None:

            # TODO: Find a better way to write this
            if self.tile == START_COLOR:
                if self.start_tile is not None:
                    self.start_tile.configure(bg=WALKABLE_COLOR)
                self.start_tile = button
            else:
                if self.target_tile is not None:
                    self.target_tile.configure(bg=WALKABLE_COLOR)
                self.target_tile = button

            button.configure(bg=self.tile)
            self.tile = None
        else:
            if button.cget("background") == WALL_COLOR:
                button.configure(bg=WALKABLE_COLOR)
            else:
                button.configure(bg=WALL_COLOR)

        # coords = get_button_coords(button)
        # for n in get_neighbors(self.btn_list,coords[0],coords[1]):
        #     gi = n.grid_info()
        #     print(str(gi['row']) + " " + str(gi['column']))


    def set_tile_to_set(self, new_tile):
        self.tile = new_tile

    def resize_grid(self):
        class Request(object):
            def __init__(self,parent):
                self.top_level = Toplevel(parent)

                self.var_r = IntVar()
                self.var_c = IntVar()

                self.entry_r = Entry(self.top_level, textvariable = self.var_r, width = 3)
                self.entry_c = Entry(self.top_level, textvariable = self.var_c, width = 3)

                Button(self.top_level, text = "Submit", command = self.on_ok).pack(side="bottom")

                self.entry_r.pack(side="top")
                self.entry_c.pack(side="top")
                self.entry_r.bind("<Return>", self.on_ok)
                self.entry_c.bind("<Return>", self.on_ok)

            def show(self):

                self.top_level.wm_deiconify()
                self.top_level.wait_window()

                val = (self.var_r.get(),self.var_c.get())
                return val

            def on_ok(self, event = None):
                try:
                    r = self.var_r.get()
                    c = self.var_c.get()

                    if not (1 <= r <= 30 and 1 <= c <= 50):
                        raise Exception()

                    self.top_level.destroy()
                except:
                    pass


        r = Request(self.root).show()
        # print(r)
        self.build_maze(r[0],r[1])

    def build_maze(self, r, c):
        for lst in self.btn_list:
            for btn in lst:
                btn.destroy()


        self.r = r
        self.c = c
        self.btn_list = [list(range(c)) for i in range(r)]
        for row in range(r):
            for col in range(c):
                b = Button(self.tf, bg=WALKABLE_COLOR, width=2, height=1)
                b.configure(command=(lambda button=b: self.maze_tile_click(button)))
                b.grid(row=row, column=col)
                self.btn_list[row][col] = b


    def randomize(self):
        self.clear()
        g = prim_maze_generator(self.r, self.c)
        g = remove_some_walls(g,self.r,self.c)
        for i in range(self.r):
            for j in range(self.c):
                # if random.randint(0, 2) == 1:
                if g[i][j] == 1:
                    res = WALKABLE_COLOR
                else:
                    res = WALL_COLOR
                self.btn_list[i][j].configure(bg=res)


    def clear(self):
        self.start_tile = None
        self.target_tile = None
        for i in range(self.r):
            for j in range(self.c):
                self.btn_list[i][j].configure(text='', bg=WALKABLE_COLOR)

    def clear_search(self):
        for i in range(self.r):
            for j in range(self.c):
                color = self.btn_list[i][j].cget("background")
                if  color != WALL_COLOR and color != TARGET_COLOR and color != START_COLOR:
                    self.btn_list[i][j].configure(text='', bg=WALKABLE_COLOR)


    def bfs(self):
        BFS_TO_SEARCH = 'red'
        BFS_SEARCHED_TILE = 'orange'
        BFS_PATH_TILE = '#40E0D0'

        BFS_DELAY = 0.05
        PATH_DELAY = 0.01

        self.clear_search()


        if self.start_tile is None or self.target_tile is None:
            return


        arr_map = [list(range(self.c)) for i in range(self.r)]
        for i in range(self.r):
            for j in range(self.c):
                if self.btn_list[i][j].cget("background") == WALL_COLOR:
                    arr_map[i][j] = -1
                else:
                    arr_map[i][j] = 0

        s_coords = get_button_coords(self.start_tile)
        t_coords = get_button_coords(self.target_tile)

        arr_map[s_coords[0]][s_coords[1]] = -1

        layer = 1
        queued = get_neighbors(arr_map,s_coords[0],s_coords[1])
        queued = [x for x in queued if arr_map[x[0]][x[1]] == 0]
        while queued != [] and arr_map[t_coords[0]][t_coords[1]] == 0:
            neighbors = []
            for q in queued:
                arr_map[q[0]][q[1]] = layer
                temp = get_neighbors(arr_map,q[0],q[1])
                temp = [c for c in temp if arr_map[c[0]][c[1]] == 0]    # we ignore the ones we visited, values being >0
                neighbors.extend(temp)

                if q != t_coords:
                    self.btn_list[q[0]][q[1]].configure(text=layer, bg=BFS_SEARCHED_TILE)

            layer = layer + 1

            queued = list(set(neighbors))
            for n in neighbors:
                if n != s_coords and n != t_coords:
                    self.btn_list[n[0]][n[1]].configure(text=layer, bg=BFS_TO_SEARCH)



            # Wait a couple of seconds to simulate the "breadth" search.
            self.tf.update_idletasks()
            time.sleep(BFS_DELAY)


        # now we paint with blue tiles the shortest path from target to start
        current_coords = t_coords
        curr_layer = arr_map[t_coords[0]][t_coords[1]]
        arr_map[s_coords[0]][s_coords[1]] = 0
        if curr_layer == 0:
            return

        while curr_layer > 1:
            temp2 = get_neighbors(arr_map, current_coords[0], current_coords[1])
            temp2 = [c for c in temp2 if arr_map[c[0]][c[1]] == curr_layer - 1]
            current_coords = temp2[0]    # TODO: we could choose a random one
            self.btn_list[current_coords[0]][current_coords[1]].configure(bg = BFS_PATH_TILE)
            curr_layer = curr_layer - 1

            self.tf.update_idletasks()
            time.sleep(PATH_DELAY)

        # self.btn_list[current_coords[0]][current_coords[1]].configure(bg=START_COLOR)   # we assume curr_coords eventually lead to the start tile


s = Tk()
sheet = MainScreen(s, 25, 50)
# s = Canvas(s,width = 500, height = 500)

s.mainloop()
