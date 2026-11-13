"""Diagnosis penyebab telur ayam gagal menetas pada mesin tetas.

Jalankan: python main.py            (memakai kb_tetas.json)
          python main.py kb_lain.json
"""
import json
import sys


def muat_kb(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def syarat_terpenuhi(aturan, memori):
    """mode 'dan' = semua syarat ada di memori; 'atau' = salah satu cukup."""
    ada = [s in memori for s in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)


def fakta_dasar(kb):
    """Fakta yang tidak pernah menjadi hasil (maka) aturan mana pun -> ditanyakan ke user."""
    hasil = {a["maka"] for a in kb["aturan"]}
    daftar = []
    for a in kb["aturan"]:
        for s in a["jika"]:
            if s not in hasil and s not in daftar:
                daftar.append(s)
    return daftar


def forward_chaining(kb, fakta_awal):
    memori = set(fakta_awal)
    asal = {}   # hasil -> aturan yang menghasilkannya (bahan "alasan")
    log = []    # urutan aturan yang dijalankan
    while True:
        cocok = [a for a in kb["aturan"]
                 if a["maka"] not in memori and syarat_terpenuhi(a, memori)]
        if not cocok:
            break
        r = cocok[0]                 # ambil aturan pertama
        memori.add(r["maka"])
        asal[r["maka"]] = r
        log.append(r)
    return memori, asal, log


def jejak_alasan(hasil, asal, memori, urut):
    """Telusuri mundur: hasil <- aturan <- syarat yang juga hasil aturan lain."""
    if hasil in urut or hasil not in asal:
        return
    urut.append(hasil)
    for s in asal[hasil]["jika"]:
        if s in memori:
            jejak_alasan(s, asal, memori, urut)


def main():
    kb = muat_kb(sys.argv[1] if len(sys.argv) > 1 else "kb_tetas.json")
    print(kb["judul"])
    print("Jawab y/t.")

    fakta = []
    for i, f in enumerate(fakta_dasar(kb), 1):
        while True:
            j = input(f"{i}. {kb['pertanyaan'][f]} (y/t) > ").strip().lower()
            if j in ("y", "t"):
                break
            print("   Ketik y atau t saja.")
        if j == "y":
            fakta.append(f)

    print()
    print("Fakta awal:", ", ".join(fakta) if fakta else "(tidak ada)")
    memori, asal, log = forward_chaining(kb, fakta)

    for n, r in enumerate(log, 1):
        print(f"Siklus {n}: {r['id']} -> {r['maka']}")
    print(f"Siklus {len(log) + 1}: tidak ada aturan baru, berhenti")

    # kesimpulan akhir = hasil yang tidak dipakai sebagai syarat aturan lain
    dipakai = {s for a in kb["aturan"] for s in a["jika"]}
    akhir = [r["maka"] for r in log if r["maka"] not in dipakai]
    antara = [r["maka"] for r in log if r["maka"] in dipakai]

    print()
    if akhir:
        print("Kesimpulan:", "; ".join(akhir))
        urut = []
        for h in akhir:
            jejak_alasan(h, asal, memori, urut)
        print("Alasan:")
        for h in urut:
            r = asal[h]
            syarat = ", ".join(s for s in r["jika"] if s in memori)
            print(f"  {h} <- {r['id']} ({syarat}) [sumber: {', '.join(r['sumber'])}]")
    elif antara:
        print("Kesimpulan: belum ada kesimpulan akhir.")
        print("Temuan antara:", "; ".join(antara))
    else:
        print("Kesimpulan: tidak ada kesimpulan dari fakta yang diberikan.")

    print()
    print("Catatan:", kb["batas"])


if __name__ == "__main__":
    main()