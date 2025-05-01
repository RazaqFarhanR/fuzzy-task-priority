import pandas as pd
from datetime import datetime
from fuzzy_system import hitung_prioritas

def main():
    data = pd.read_csv('data/sample_tasks.csv')

    today = datetime.now().date()
    hasil = []

    for index, row in data.iterrows():
        deadline_date = datetime.strptime(row['deadline_date'], '%Y-%m-%d').date()
        days_left = (deadline_date - today).days
        if days_left < 0:
            days_left = 0

        difficulty_scaled = min(row['difficulty'] * 2, 10)
        urgency_scaled = row['urgency']

        prioritas = hitung_prioritas(days_left, difficulty_scaled, urgency_scaled)

        hasil.append({
            'task': row['task'],
            'prioritas': prioritas,
            'days_left': days_left
        })

    df_hasil = pd.DataFrame(hasil)
    df_urut = df_hasil.sort_values(by='prioritas', ascending=False).reset_index(drop=True)

    print(df_urut)

if __name__ == "__main__":
    main()
