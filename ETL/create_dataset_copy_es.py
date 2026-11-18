import csv
import unicodedata
from pathlib import Path

base = Path(r"c:\Users\fabia\OneDrive\Desktop\Caso_Semestral\StreamViewAnalytics")
input_dir = base / "DataSet_Original"
output_dir = base / "DataSet_Espanol"
output_dir.mkdir(exist_ok=True)

header_map = {
    "show_id": "id_muestra",
    "type": "tipo",
    "title": "titulo",
    "director": "director",
    "cast": "reparto",
    "country": "pais",
    "date_added": "fecha_agregada",
    "release_year": "anio_estreno",
    "rating": "clasificacion",
    "duration": "duracion",
    "genres": "generos",
    "language": "idioma",
    "description": "descripcion",
    "popularity": "popularidad",
    "vote_count": "votos",
    "vote_average": "promedio_votos",
    "budget": "presupuesto",
    "revenue": "ingresos",
}

tipo_map = {
    "Movie": "Pelicula",
    "TV Show": "Serie",
    "movie": "Pelicula",
    "tv show": "Serie",
}

genre_map = {
    "Action": "Accion",
    "Adventure": "Aventura",
    "Animation": "Animacion",
    "Biography": "Biografia",
    "Comedy": "Comedia",
    "Crime": "Crimen",
    "Documentary": "Documental",
    "Drama": "Drama",
    "Family": "Familia",
    "Fantasy": "Fantasia",
    "History": "Historia",
    "Horror": "Terror",
    "Music": "Musica",
    "Mystery": "Misterio",
    "News": "Noticias",
    "Reality": "Reality",
    "Romance": "Romance",
    "Science Fiction": "Ciencia Ficcion",
    "Science-Fiction": "Ciencia Ficcion",
    "Sci-Fi": "Ciencia Ficcion",
    "Short": "Corto",
    "Sport": "Deporte",
    "Talk": "Charla",
    "Thriller": "Suspenso",
    "War": "Guerra",
    "Western": "Western",
    "Kids": "Infantil",
    "Lifestyle": "Estilo de Vida",
    "Game Show": "Concurso",
    "Cooking": "Cocina",
    "Travel": "Viajes",
}

language_map = {
    "en": "Ingles",
    "es": "Espanol",
    "fr": "Frances",
    "de": "Aleman",
    "it": "Italiano",
    "pt": "Portugues",
    "ja": "Japones",
    "ko": "Coreano",
    "zh": "Chino",
    "hi": "Hindi",
    "ar": "Arabigo",
    "ru": "Ruso",
    "cs": "Checo",
    "el": "Griego",
    "tr": "Turco",
    "nl": "Holandes",
    "sv": "Sueco",
    "pl": "Polaco",
    "da": "Danes",
    "fi": "Finlandes",
    "no": "Noruego",
    "th": "Tailandes",
    "he": "Hebreo",
    "id": "Indonesio",
    "ro": "Rumano",
    "hu": "Hungaro",
    "uk": "Ucraniano",
    "fa": "Persa",
    "sr": "Serbio",
    "sl": "Esloveno",
    "ca": "Catalan",
    "hr": "Croata",
    "bn": "Bangla",
    "te": "Telugu",
    "ta": "Tamil",
    "ml": "Malayalam",
    "mr": "Marathi",
}

country_map = {
    "United States of America": "Estados Unidos",
    "United Kingdom": "Reino Unido",
    "South Korea": "Corea del Sur",
    "Greece": "Grecia",
    "Czech Republic": "Republica Checa",
    "France": "Francia",
    "Spain": "Espana",
    "Argentina": "Argentina",
    "Brazil": "Brasil",
    "Mexico": "Mexico",
    "Chile": "Chile",
    "Colombia": "Colombia",
    "Peru": "Peru",
    "Germany": "Alemania",
    "Italy": "Italia",
    "Japan": "Japon",
    "Canada": "Canada",
    "Australia": "Australia",
    "India": "India",
    "China": "China",
    "Russia": "Rusia",
    "Portugal": "Portugal",
    "Netherlands": "Paises Bajos",
    "Sweden": "Suecia",
    "Norway": "Noruega",
    "Denmark": "Dinamarca",
    "Finland": "Finlandia",
    "Belgium": "Belgica",
    "Ireland": "Irlanda",
    "Switzerland": "Suiza",
    "Austria": "Austria",
    "Turkey": "Turquia",
    "Poland": "Polonia",
    "Romania": "Rumania",
    "Hungary": "Hungria",
    "Thailand": "Tailandia",
    "Israel": "Israel",
    "Egypt": "Egipto",
    "Nigeria": "Nigeria",
    "South Africa": "Sudafrica",
    "New Zealand": "Nueva Zelanda",
    "Philippines": "Filipinas",
    "Indonesia": "Indonesia",
    "Malaysia": "Malasia",
    "Vietnam": "Vietnam",
    "Pakistan": "Pakistan",
}

duration_map = {
    "Seasons": "Temporadas",
    "Season": "Temporada",
}


def normalize_ascii(value):
    if value is None:
        return ""
    text = str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("Ñ", "N").replace("ñ", "n")
    return text


def translate_generos(value):
    if value is None or value == "":
        return ""
    items = [item.strip() for item in str(value).split(",") if item.strip()]
    result = []
    for item in items:
        result.append(genre_map.get(item, item))
    return ", ".join(normalize_ascii(x) for x in result)


def translate_idioma(value):
    if value is None or value == "":
        return ""
    val = str(value).strip()
    translated = language_map.get(val, val)
    return normalize_ascii(translated)


def translate_pais(value):
    if value is None or value == "":
        return ""
    values = [item.strip() for item in str(value).split(",") if item.strip()]
    translated = []
    for item in values:
        translated.append(country_map.get(item, item))
    return ", ".join(normalize_ascii(x) for x in translated)


def translate_tipo(value):
    if value is None or value == "":
        return ""
    val = str(value).strip()
    translated = tipo_map.get(val, val)
    return normalize_ascii(translated)


def translate_duracion(value):
    if value is None or value == "":
        return ""
    text = str(value)
    for key, translated in duration_map.items():
        text = text.replace(key, translated)
    return normalize_ascii(text)


files = [
    ("netflix_movies_detailed_up_to_2025.csv", "netflix_movies_detailed_up_to_2025_es.csv"),
    ("netflix_tv_shows_detailed_up_to_2025.csv", "netflix_tv_shows_detailed_up_to_2025_es.csv"),
]

for src_name, dst_name in files:
    src_path = input_dir / src_name
    out_path = output_dir / dst_name

    with src_path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    output_rows = []
    for row in rows:
        new_row = {}
        for key, value in row.items():
            new_key = header_map.get(key, normalize_ascii(key))
            if key == "type":
                new_row[new_key] = translate_tipo(value)
            elif key == "genres":
                new_row[new_key] = translate_generos(value)
            elif key == "language":
                new_row[new_key] = translate_idioma(value)
            elif key == "country":
                new_row[new_key] = translate_pais(value)
            elif key == "duration":
                new_row[new_key] = translate_duracion(value)
            elif key in {"title", "director", "cast", "description"}:
                new_row[new_key] = normalize_ascii(value or "")
            else:
                new_row[new_key] = value
        output_rows.append(new_row)

    translated_headers = [header_map.get(field, normalize_ascii(field)) for field in fieldnames]

    with out_path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=translated_headers)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Generado: {out_path.name}")

print(f"Carpeta final: {output_dir}")
