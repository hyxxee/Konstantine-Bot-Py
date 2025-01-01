# Konstantine Bot Py

sebuah bot discord anime.

## Daftar Isi

- [Tentang](#tentang)
- [Fitur](#fitur)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Kontak](#kontak)

## Tentang

bot discord untuk cek anime/manga.

## Fitur

- ?anime <nama anime> untuk cek anime
- ?manga <nama manga> untuk cek manga 

## Instalasi

Instruksi untuk menginstal proyek ini di lingkungan lokal Anda.

```bash
# Clone repositori ini
https://github.com/hyxxee/Konstantine-Bot-Py.git

# Masuk ke direktori proyek
cd Konstantine-Bot-Py

# Instal dependensi

# upload graphql anilist
curl -X POST https://graphql.anilist.co \
-H "Content-Type: application/json" \
-d @<(cat <<EOF
{
    "query": "$(sed ':a;N;$!ba;s/\n/\\n/g' anime_query.graphql)",
    "variables": $(cat variables.json)
}
EOF
)
