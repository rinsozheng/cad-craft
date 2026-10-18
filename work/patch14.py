p=r"D:\code\github\cad-craft\work\design_lib.py"
s=open(p,encoding="utf-8").read()
s=s.replace("'A-KITCHEN': (4, 25, 'Continuous')","'A-KITCHEN': (5, 25, 'Continuous')")
s=s.replace("'A-FIXTURE': (4, 18, 'Continuous')","'A-FIXTURE': (5, 18, 'Continuous')")
s=s.replace("'A-DIM': (2, 13, 'Continuous')","'A-DIM': (1, 13, 'Continuous')")
s=s.replace("'A-AREA': (2, 18, 'Continuous')","'A-AREA': (5, 18, 'Continuous')")
open(p,"w",encoding="utf-8").write(s)
print("colors patched")
