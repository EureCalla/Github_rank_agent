import sqlite3

conn = sqlite3.connect('database/research_github.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('''
    SELECT rank, repo_full_name, description, repo_url, total_stars, language, weekly_growth, created_date
    FROM research_github 
    ORDER BY rank ASC 
    LIMIT 19
''')

rows = cursor.fetchall()
print('\n【本周 GitHub 熱門排行 Top 19】\n')
for row in rows:
    stars = row['total_stars'] if row['total_stars'] else 'N/A'
    stars_display = f"{stars//1000}k" if isinstance(stars, int) and stars > 0 else str(stars)
    print(f"{row['rank']:<3} ⭐ {stars_display:<8} | {row['repo_full_name']}")
    if row['description']:
        desc = row['description'][:70]
        print(f"     📝 {desc}")
    growth = row['weekly_growth'] if row['weekly_growth'] else 0
    if growth:
        print(f"     📈 本周增長: +{growth} ⭐")
    if row['language']:
        print(f"     💻 {row['language']}")
    print()

conn.close()
