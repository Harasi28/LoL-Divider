import tkinter as tk
from tkinter import ttk, messagebox
import random

# ランクとそのウェイト（1が最も低く、11が最も高い）
rank_weights = {
    'チャレンジャー': 11, 'グランドマスター': 10, 'マスター': 9, 'ダイアモンド': 8, 
    'エメラルド': 7, 'プラチナ': 6, 'ゴールド': 5, 'シルバー': 4, 
    'ブロンズ': 3, 'アイアン': 2, 'ランクなし': 3
}

# プレイヤー情報のリスト
players = []

# プレイヤー情報の入力とチーム分割のロジック
def add_player():
    if len(players) < 10:
        # 入力されたプレイヤー情報を取得
        player_info = {'name': name_entry.get(), 'rank': rank_var.get(), 'role': role_var.get()}
        players.append(player_info)

        # 入力フィールドをクリア
        name_entry.delete(0, tk.END)
        rank_var.set('')
        role_var.set('')

        # 現在のプレイヤー数を更新
        player_count_label.config(text=f"現在のプレイヤー数: {len(players)} / 10")
    else:
        messagebox.showinfo("通知", "プレイヤーの数が最大に達しました。")

def create_balanced_teams():
    best_difference = float('inf')  # 最小差分を追跡するための変数を無限大に設定
    best_division = None  # 最適なチーム分けを保持する変数

    # 特定の試行回数（例えば、10000回）または特定の時間経過までループを続ける
    for _ in range(10000):
        random.shuffle(players)  # プレイヤーリストをランダムにシャッフル
        team1 = players[:5]
        team2 = players[5:]

        # 各チームのランクウェイトの合計を計算
        team1_weight = sum(rank_weights[player['rank']] for player in team1)
        team2_weight = sum(rank_weights[player['rank']] for player in team2)

        # 2つのチーム間のウェイト差分を計算
        difference = abs(team1_weight - team2_weight)

        # もし新しい差分がこれまでの最小差分よりも小さければ、この分割を「最適な分割」として記録
        if difference < best_difference:
            best_difference = difference
            best_division = (team1, team2)

            # もし完全に均等な分割が見つかれば、ループを抜ける
            if difference == 0:
                break

    return best_division

# divide_teams関数内でこの関数を呼び出す
def divide_teams():
    if len(players) == 10:
        team1, team2 = create_balanced_teams()

        # 結果の表示
        result_text = "Team 1:\n" + "\n".join([f"{p['name']} ({p['rank']}, {p['role']})" for p in team1]) + \
                      "\n\nTeam 2:\n" + "\n".join([f"{p['name']} ({p['rank']}, {p['role']})" for p in team2])
        messagebox.showinfo("分割結果", result_text)
    else:
        messagebox.showerror("エラー", "プレイヤーが10人揃っていません。")

# GUIのセットアップ
app = tk.Tk()
app.title("League of Legends Team Divider")

# ユーザー名入力
tk.Label(app, text="ユーザーネーム").pack()
name_entry = tk.Entry(app)
name_entry.pack()

# ランク選択
tk.Label(app, text="ランク").pack()
rank_var = tk.StringVar()
rank_choice = ttk.Combobox(app, textvariable=rank_var, values=list(rank_weights.keys()))
rank_choice.pack()

# ロール選択
tk.Label(app, text="ロール").pack()
role_var = tk.StringVar()
role_choice = ttk.Combobox(app, textvariable=role_var, values=['top', 'jg', 'mid', 'adc', 'sup'])
role_choice.pack()

# プレイヤー追加ボタン
add_button = tk.Button(app, text="プレイヤー追加", command=add_player)
add_button.pack()

# 現在のプレイヤー数
player_count_label = tk.Label(app, text="現在のプレイヤー数: 0 / 10")
player_count_label.pack()

# チーム分割ボタン
divide_button = tk.Button(app, text="チーム分割", command=divide_teams)
divide_button.pack()

app.mainloop()
