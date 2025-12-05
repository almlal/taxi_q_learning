# Dosya Adı: taxi_env.py

import numpy as np
import random
import matplotlib
# MacOS ve görüntü oluşturma hatalarını önlemek için 'Agg' backend
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class TaxiEnv6x6:
    def __init__(self):
        self.rows = 6
        self.cols = 6
        # Lokasyonlar: (Satır, Sütun)
        self.locs = [(0, 0), (0, 5), (4, 0), (5, 4), (2, 3)]
        self.action_space_n = 6
        # Duvarlar
        self.walls_hor = [(0, 1), (2, 3), (4, 4)]
        self.walls_ver = [(1, 1), (3, 2), (4, 3)]
        self.reset()

    def encode(self, taxi_row, taxi_col, pass_loc, dest_idx):
        i = taxi_row
        i *= 6
        i += taxi_col
        i *= 6
        i += pass_loc
        i *= 5
        i += dest_idx
        return i

    def decode(self, i):
        out = []
        out.append(i % 5)
        i = i // 5
        out.append(i % 6)
        i = i // 6
        out.append(i % 6)
        i = i // 6
        out.append(i)
        return list(reversed(out))

    def reset(self):
        self.taxi_row = random.randint(0, self.rows - 1)
        self.taxi_col = random.randint(0, self.cols - 1)
        self.pass_idx = random.randint(0, 4)
        self.dest_idx = random.randint(0, 4)
        while self.pass_idx == self.dest_idx:
            self.dest_idx = random.randint(0, 4)
        self.pass_loc = self.pass_idx 
        return self.encode(self.taxi_row, self.taxi_col, self.pass_loc, self.dest_idx)

    def step(self, action):
        reward = -1
        done = False
        new_row, new_col = self.taxi_row, self.taxi_col
        
        # Hareketler: 0:South, 1:North, 2:East, 3:West
        if action == 0: # SOUTH
            if new_row < self.rows - 1 and (new_row, new_col) not in self.walls_hor:
                new_row += 1
        elif action == 1: # NORTH
            if new_row > 0 and (new_row - 1, new_col) not in self.walls_hor:
                new_row -= 1
        elif action == 2: # EAST
            if new_col < self.cols - 1 and (new_row, new_col) not in self.walls_ver:
                new_col += 1
        elif action == 3: # WEST
            if new_col > 0 and (new_row, new_col - 1) not in self.walls_ver:
                new_col -= 1
        
        self.taxi_row = new_row
        self.taxi_col = new_col

        # Pickup (4) / Dropoff (5)
        if action == 4: # PICKUP
            if self.pass_loc == 5:
                reward = -10
            elif (self.taxi_row, self.taxi_col) == self.locs[self.pass_loc]:
                self.pass_loc = 5
                reward = 10
            else:
                reward = -10
        elif action == 5: # DROPOFF
            if self.pass_loc == 5 and (self.taxi_row, self.taxi_col) == self.locs[self.dest_idx]:
                reward = 20
                done = True
            elif self.pass_loc == 5:
                reward = -10
            else:
                reward = -10

        state = self.encode(self.taxi_row, self.taxi_col, self.pass_loc, self.dest_idx)
        return state, reward, done

    def render_frame(self, episode_num=1):
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # Grid ayarları
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.set_xticks(np.arange(0, 7, 1))
        ax.set_yticks(np.arange(0, 7, 1))
        ax.set_xticklabels([]) 
        ax.set_yticklabels([])
        ax.grid(True, color='black', linewidth=1)
        ax.invert_yaxis()
        
        # Hedef (Mor)
        dest_r, dest_c = self.locs[self.dest_idx]
        rect_dest = patches.Rectangle((dest_c, dest_r), 1, 1, facecolor='purple', alpha=0.5)
        ax.add_patch(rect_dest)
        
        # Yolcu (Mavi)
        if self.pass_loc != 5:
            pass_r, pass_c = self.locs[self.pass_loc]
            rect_pass = patches.Rectangle((pass_c, pass_r), 1, 1, facecolor='blue')
            ax.add_patch(rect_pass)
            ax.text(pass_c + 0.5, pass_r + 0.5, "Yolcu", ha='center', va='center', color='white', fontsize=10, fontweight='bold')

        # Hedef Yazısı
        ax.text(dest_c + 0.5, dest_r + 0.5, "HEDEF", ha='center', va='center', color='white', fontsize=9, fontweight='bold')

        # Taksi (Sarı/Yeşil)
        taxi_color = 'yellow' 
        taxi_text = "Taksi"
        if self.pass_loc == 5:
            taxi_color = 'green' 
            taxi_text = "Dolu"
            
        rect_taxi = patches.Rectangle((self.taxi_col, self.taxi_row), 1, 1, facecolor=taxi_color)
        ax.add_patch(rect_taxi)
        ax.text(self.taxi_col + 0.5, self.taxi_row + 0.5, taxi_text, ha='center', va='center', color='black', fontsize=10, fontweight='bold')

        # Duvarlar
        for (r, c) in self.walls_hor:
            ax.plot([c, c+1], [r+1, r+1], color='black', linewidth=5)
        for (r, c) in self.walls_ver:
            ax.plot([c+1, c+1], [r, r+1], color='black', linewidth=5)

        plt.title(f"Bölüm: {episode_num} | Durum: {('DOLU' if self.pass_loc==5 else 'BOS')}", fontsize=14)
        
        fig.canvas.draw()
        image = np.array(fig.canvas.buffer_rgba())
        image = image[:, :, :3]
        plt.close(fig)
        return image