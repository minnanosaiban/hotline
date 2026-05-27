import sys
sys.path.insert(0, r"C:\stock_analysis")
from pathlib import Path

exec(open(r"C:\stock_analysis\scripts\blog\01_PEG_ROE_make_images.py", encoding="utf-8").read().split("if __name__")[0])

df = load_universe()
OUT = Path(r"C:/minnanosaiban/hotline/docs/blog/posts/img/01_PEG_ROE")
make_majors_table(df, OUT / "02_majors_table.png")
print("done: 02_majors_table.png")
