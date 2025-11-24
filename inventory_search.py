#!/usr/bin/env python3
"""
inventory search
"""

import json
import sys
from difflib import get_close_matches
from typing import List, Optional, TypedDict

class InventoryItem(TypedDict):
    id: str
    name: str
    category: str
    qty: int
    location: str

INVENTORY_FILE = "inventory.json"

# -------------------------
# Data helpers
# -------------------------
def load_inventory(path: str = INVENTORY_FILE) -> List[InventoryItem]:
    import os, json
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_inventory(items: List[InventoryItem], path: str = INVENTORY_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def pretty_print_item(item: InventoryItem) -> None:
    print("-" * 40)
    for k, v in item.items():
        print(f"{k}: {v}")
    print("-" * 40)


# -------------------------
# Search functions
# -------------------------
def find_by_id(items: List[InventoryItem], item_id: str) -> Optional[InventoryItem]:
    for item in items:
        if str(item.get("id")) == str(item_id):
            return item
    return None


def search_by_name(items: List[InventoryItem], name_query: str) -> List[InventoryItem]:
    q = name_query.strip().lower()
    results: List[InventoryItem] = [] 
    for item in items:
        name = str(item.get("name", "")).lower()
        if q in name:
            results.append(item)
    return results


def search_by_category(items: List[InventoryItem], category: str) -> List[InventoryItem]:
    q = category.strip().lower()
    return [it for it in items if q == str(it.get("category", "")).lower()]


def fuzzy_search_name(items: List[InventoryItem], name_query: str, n: int = 5, cutoff: float = 0.6) -> List[InventoryItem]:
    # build name -> item map
    name_to_item = {str(it.get("name", "")): it for it in items}
    names = list(name_to_item.keys())
    matches = get_close_matches(name_query, names, n=n, cutoff=cutoff)
    return [name_to_item[m] for m in matches]


# -------------------------
# CRUD helpers (minimal)
# -------------------------
def add_item(items: List[InventoryItem], item: InventoryItem) -> None:
    items.append(item)


def remove_item_by_id(items: List[InventoryItem], item_id: str) -> bool:
    idx = next((i for i, it in enumerate(items) if str(it.get("id")) == str(item_id)), None)
    if idx is None:
        return False
    items.pop(idx)
    return True


# -------------------------
# CLI
# -------------------------
def print_menu():
    print("""
=== INVENTORY SEARCH ===
1) Tampilkan semua barang
2) Cari barang berdasarkan ID
3) Cari barang berdasarkan nama (partial)
4) Fuzzy search nama (untuk typo)
5) Cari barang berdasarkan kategori
6) Tambah barang baru
7) Hapus barang berdasarkan ID
0) Simpan & keluar
""".strip())


def prompt_new_item() -> InventoryItem:
    _id = input("ID: ").strip()
    name = input("Nama: ").strip()
    category = input("Kategori: ").strip()
    location = input("Lokasi (opsional): ").strip()
    
    while True:
        qty = input("Jumlah (qty): ").strip()
        try:
            qty_val = int(qty)
            break
        except ValueError:
            print("arap masukkan angka yang valid untuk jumlah.")
    
    return {
        "id": _id,
        "name": name,
        "category": category,
        "qty": qty_val,
        "location": location
    }


def main():
    items: List[InventoryItem] = load_inventory()
    print(f"Loaded {len(items)} item(s) from '{INVENTORY_FILE}'.\n")

    while True:
        print_menu()
        choice = input("Pilih nomor: ").strip()
        if choice == "1":
            if not items:
                print("[Inventaris kosong]")
            for it in items:
                pretty_print_item(it)

        elif choice == "2":
            _id = input("Masukkan ID: ").strip()
            found = find_by_id(items, _id)
            if found:
                pretty_print_item(found)
            else:
                print("Tidak ditemukan item dengan ID tersebut.")

        elif choice == "3":
            q = input("Masukkan nama atau sebagian nama: ").strip()
            res = search_by_name(items, q)
            if not res:
                print("Tidak ada hasil (partial search).")
            else:
                for it in res:
                    pretty_print_item(it)

        elif choice == "4":
            q = input("Masukkan nama (fuzzy): ").strip()
            res = fuzzy_search_name(items, q)
            if not res:
                print("Tidak ada hasil fuzzy yang cukup dekat.")
            else:
                print(f"Menemukan {len(res)} hasil terdekat:")
                for it in res:
                    pretty_print_item(it)

        elif choice == "5":
            cat = input("Masukkan kategori: ").strip()
            res = search_by_category(items, cat)
            if not res:
                print("Tidak ada barang pada kategori itu.")
            else:
                for it in res:
                    pretty_print_item(it)

        elif choice == "6":
            new = prompt_new_item()
            if find_by_id(items, new["id"]):
                print("ID sudah ada. Gunakan ID unik.")
            else:
                add_item(items, new)
                print("Barang ditambahkan (belum tersimpan).")

        elif choice == "7":
            _id = input("Masukkan ID untuk dihapus: ").strip()
            ok = remove_item_by_id(items, _id)
            if ok:
                print("Berhasil dihapus (belum tersimpan).")
            else:
                print("ID tidak ditemukan.")

        elif choice == "0":
            save_inventory(items)
            print(f"Inventaris disimpan ke '{INVENTORY_FILE}'. Keluar.")
            break

        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDibatalkan oleh pengguna. Menyimpan sebelum keluar...")
        save_inventory(load_inventory())  
        sys.exit(0)
