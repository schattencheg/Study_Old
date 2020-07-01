from tqdm import tqdm
l = []
ch = [1, 2, 4, 5, 10, 20, 101, 202, 404, 505, 1010, 2020]
r = 100
for a in tqdm(ch):
    for b in ch:
        for c in ch:
            for d in ch:
                for e in ch:
                    if (a * b * c * d * e == 2020):
                        print(a * b * c * d * e)
                        l.append([a,b,c,d,e])
print(l)