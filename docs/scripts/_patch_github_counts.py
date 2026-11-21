from pathlib import Path

p = Path(__file__).with_name("informe_techasset.py")
s = p.read_text(encoding="utf-8")

s = s.replace("39 capturas", "40 capturas")
s = s.replace('("39", "CAPTURAS")', '("40", "CAPTURAS")')
s = s.replace('"39", "capturas"', '"40", "capturas"')
s = s.replace("44 figuras", "45 figuras")
s = s.replace("49 tablas", "50 tablas")
p.write_text(s, encoding="utf-8")
print("conteos de capturas/figuras actualizados")
