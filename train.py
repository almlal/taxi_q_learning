# Dosya Adı: train.py

import numpy as np
import random
import imageio
from taxi_env import TaxiEnv6x6  # Ortamımızı buradan çağırıyoruz

def train_agent():
    env = TaxiEnv6x6()
    
    # Q-Table Başlatma
    q_table = np.zeros([1080, env.action_space_n])

    # Hiperparametreler
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1
    episodes = 5000

    print("Eğitim başladı...")
    for i in range(episodes):
        state = env.reset()
        done = False
        while not done:
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 5)
            else:
                action = np.argmax(q_table[state])
            
            next_state, reward, done = env.step(action)
            
            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])
            
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state, action] = new_value
            
            state = next_state
            
    print("Eğitim tamamlandı.")
    return q_table, env

def create_animation(q_table, env, output_file='taxi_simulation.gif'):
    print("Test ve Animasyon oluşturuluyor (4 Farklı Tur)...")
    frames = []
    total_test_episodes = 4

    for ep in range(1, total_test_episodes + 1):
        state = env.reset()
        done = False
        steps = 0
        max_steps = 30 

        while not done and steps < max_steps:
            frames.append(env.render_frame(episode_num=ep))
            action = np.argmax(q_table[state])
            state, reward, done = env.step(action)
            steps += 1
        
        # Bölüm sonu karesini ekle
        frames.append(env.render_frame(episode_num=ep))
        
        # Geçiş duraksaması
        last_frame = env.render_frame(episode_num=ep)
        for _ in range(4):
            frames.append(last_frame)

    imageio.mimsave(output_file, frames, fps=6)
    print(f"Animasyon '{output_file}' olarak kaydedildi.")

if __name__ == "__main__":
    # Önce eğit
    q_table, env = train_agent()
    # Sonra GIF yap
    create_animation(q_table, env, output_file='taxi_final.gif')