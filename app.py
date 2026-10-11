from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "autolab-calculator-secret-key"

KONVERSI = {
    "arus": {
        "label": "Arus Listrik",
        "satuan": {
            "µA ke mA": ("µA", "mA", 0.001),
            "mA ke µA": ("mA", "µA", 1000),
            "mA ke A": ("mA", "A", 0.001),
            "A ke mA": ("A", "mA", 1000),
            "A ke kA": ("A", "kA", 0.001),
            "kA ke A": ("kA", "A", 1000),
        },
    },
    "tegangan": {
        "label": "Tegangan",
        "satuan": {
            "µV ke mV": ("µV", "mV", 0.001),
            "mV ke µV": ("mV", "µV", 1000),
            "mV ke V": ("mV", "V", 0.001),
            "V ke mV": ("V", "mV", 1000),
            "V ke kV": ("V", "kV", 0.001),
            "kV ke V": ("kV", "V", 1000),
        },
    },
    "resistansi": {
        "label": "Resistansi",
        "satuan": {
            "mΩ ke Ω": ("mΩ", "Ω", 0.001),
            "Ω ke mΩ": ("Ω", "mΩ", 1000),
            "Ω ke kΩ": ("Ω", "kΩ", 0.001),
            "kΩ ke Ω": ("kΩ", "Ω", 1000),
            "kΩ ke MΩ": ("kΩ", "MΩ", 0.001),
            "MΩ ke kΩ": ("MΩ", "kΩ", 1000),
        },
    },
    "frekuensi": {
        "label": "Frekuensi",
        "satuan": {
            "Hz ke kHz": ("Hz", "kHz", 0.001),
            "kHz ke Hz": ("kHz", "Hz", 1000),
            "kHz ke MHz": ("kHz", "MHz", 0.001),
            "MHz ke kHz": ("MHz", "kHz", 1000),
            "MHz ke GHz": ("MHz", "GHz", 0.001),
            "GHz ke MHz": ("GHz", "MHz", 1000),
        },
    },
    "daya": {
        "label": "Daya Listrik",
        "satuan": {
            "mW ke W": ("mW", "W", 0.001),
            "W ke mW": ("W", "mW", 1000),
            "W ke kW": ("W", "kW", 0.001),
            "kW ke W": ("kW", "W", 1000),
            "kW ke MW": ("kW", "MW", 0.001),
            "MW ke kW": ("MW", "kW", 1000),
        },
    },
    "energi": {
        "label": "Energi",
        "satuan": {
            "J ke kJ": ("J", "kJ", 0.001),
            "kJ ke J": ("kJ", "J", 1000),
            "J ke MJ": ("J", "MJ", 0.000001),
            "MJ ke J": ("MJ", "J", 1000000),
            "Wh ke kWh": ("Wh", "kWh", 0.001),
            "kWh ke Wh": ("kWh", "Wh", 1000),
        },
    },
    "kapasitansi": {
        "label": "Kapasitansi",
        "satuan": {
            "pF ke nF": ("pF", "nF", 0.001),
            "nF ke pF": ("nF", "pF", 1000),
            "nF ke µF": ("nF", "µF", 0.001),
            "µF ke nF": ("µF", "nF", 1000),
            "µF ke mF": ("µF", "mF", 0.001),
            "mF ke µF": ("mF", "µF", 1000),
        },
    },
}

RUMUS_LISTRIK = {
    "ohm": {
        "label": "Hukum Ohm",
        "pilihan": {
            "tegangan": "Tegangan (V)",
            "arus": "Arus (A)",
            "resistansi": "Resistansi (Ω)",
        },
    },
    "daya": {
        "label": "Daya Listrik",
        "pilihan": {
            "daya": "Daya (W)",
            "tegangan": "Tegangan (V)",
            "arus": "Arus (A)",
        },
    },
    "energi": {
        "label": "Energi Listrik",
        "pilihan": {
            "energi": "Energi (J)",
            "daya": "Daya (W)",
            "waktu": "Waktu (s)",
        },
    },
}

PETUNJUK_INPUT = {
    ("ohm", "tegangan"): ("Arus (A)", "Resistansi (Ω)"),
    ("ohm", "arus"): ("Tegangan (V)", "Resistansi (Ω)"),
    ("ohm", "resistansi"): ("Tegangan (V)", "Arus (A)"),
    ("daya", "daya"): ("Tegangan (V)", "Arus (A)"),
    ("daya", "tegangan"): ("Daya (W)", "Arus (A)"),
    ("daya", "arus"): ("Daya (W)", "Tegangan (V)"),
    ("energi", "energi"): ("Daya (W)", "Waktu (s)"),
    ("energi", "daya"): ("Energi (J)", "Waktu (s)"),
    ("energi", "waktu"): ("Energi (J)", "Daya (W)"),
}


def format_angka(angka):
    return f"{angka:.12g}"


def tampilkan_halaman(
    kategori="arus",
    arah=None,
    nilai_input="",
    hasil=None,
    error=None,
    rumus_aktif="ohm",
    besaran_dicari="tegangan",
    nilai1="",
    nilai2="",
    hasil_rumus=None,
    error_rumus=None,
):
    pilihan_arah = list(KONVERSI[kategori]["satuan"].keys())

    if arah not in pilihan_arah:
        arah = pilihan_arah[0]

    if rumus_aktif not in RUMUS_LISTRIK:
        rumus_aktif = "ohm"

    pilihan_rumus = RUMUS_LISTRIK[rumus_aktif]["pilihan"]

    if besaran_dicari not in pilihan_rumus:
        besaran_dicari = next(iter(pilihan_rumus))

    label1, label2 = PETUNJUK_INPUT[
        (rumus_aktif, besaran_dicari)
    ]

    return render_template(
        "index.html",
        konversi=KONVERSI,
        kategori=kategori,
        arah=arah,
        pilihan_arah=pilihan_arah,
        nilai_input=nilai_input,
        hasil=hasil,
        error=error,
        riwayat=session.get("riwayat", []),
        rumus_listrik=RUMUS_LISTRIK,
        rumus_aktif=rumus_aktif,
        besaran_dicari=besaran_dicari,
        nilai1=nilai1,
        nilai2=nilai2,
        label1=label1,
        label2=label2,
        hasil_rumus=hasil_rumus,
        error_rumus=error_rumus,
    )


@app.route("/", methods=["GET", "POST"])
def home():
    kategori = request.values.get("kategori", "arus")

    if kategori not in KONVERSI:
        kategori = "arus"

    pilihan_arah = list(KONVERSI[kategori]["satuan"].keys())
    arah = request.values.get("arah", pilihan_arah[0])

    if arah not in pilihan_arah:
        arah = pilihan_arah[0]

    nilai_input = request.values.get("nilai", "").strip()

    if request.method == "GET":
        return tampilkan_halaman(kategori, arah)

    try:
        if not nilai_input:
            raise ValueError

        nilai = float(nilai_input)

        if not (-1e100 < nilai < 1e100):
            raise ValueError

        awal, akhir, faktor = KONVERSI[kategori]["satuan"][arah]
        angka_hasil = nilai * faktor

        if not (-1e300 < angka_hasil < 1e300):
            raise ValueError

        hasil_format = format_angka(angka_hasil)

        hasil = {
            "nilai": hasil_format,
            "awal": awal,
            "akhir": akhir,
            "rumus": f"{nilai_input} × {faktor:g} = {hasil_format}",
        }

        riwayat = session.get("riwayat", [])
        riwayat.insert(0, {
            "kategori": KONVERSI[kategori]["label"],
            "nilai": nilai_input,
            "awal": awal,
            "hasil": hasil_format,
            "akhir": akhir,
        })
        session["riwayat"] = riwayat[:5]

        return tampilkan_halaman(
            kategori, arah, nilai_input, hasil
        )

    except (ValueError, OverflowError):
        return tampilkan_halaman(
            kategori,
            arah,
            nilai_input,
            error="Masukkan angka yang valid terlebih dahulu.",
        )


@app.route("/hitung-rumus", methods=["POST"])
def hitung_rumus():
    rumus = request.form.get("rumus_aktif", "ohm")
    dicari = request.form.get("besaran_dicari", "tegangan")
    nilai1 = request.form.get("nilai1", "").strip()
    nilai2 = request.form.get("nilai2", "").strip()

    if rumus not in RUMUS_LISTRIK:
        rumus = "ohm"

    if dicari not in RUMUS_LISTRIK[rumus]["pilihan"]:
        dicari = next(iter(RUMUS_LISTRIK[rumus]["pilihan"]))

    hasil_rumus = None
    error_rumus = None

    try:
        if not nilai1 or not nilai2:
            raise ValueError

        a = float(nilai1)
        b = float(nilai2)

        if not all(0 <= n < 1e100 for n in (a, b)):
            raise ValueError

        if rumus == "ohm":
            if dicari == "tegangan":
                hasil = a * b
                persamaan = f"V = {format_angka(a)} × {format_angka(b)}"
                satuan = "V"
            elif dicari == "arus":
                if b == 0:
                    raise ZeroDivisionError
                hasil = a / b
                persamaan = f"I = {format_angka(a)} / {format_angka(b)}"
                satuan = "A"
            else:
                if b == 0:
                    raise ZeroDivisionError
                hasil = a / b
                persamaan = f"R = {format_angka(a)} / {format_angka(b)}"
                satuan = "Ω"

        elif rumus == "daya":
            if dicari == "daya":
                hasil = a * b
                persamaan = f"P = {format_angka(a)} × {format_angka(b)}"
                satuan = "W"
            elif dicari == "tegangan":
                if b == 0:
                    raise ZeroDivisionError
                hasil = a / b
                persamaan = f"V = {format_angka(a)} / {format_angka(b)}"
                satuan = "V"
            else:
                if b == 0:
                    raise ZeroDivisionError
                hasil = a / b
                persamaan = f"I = {format_angka(a)} / {format_angka(b)}"
                satuan = "A"

        else:
            if dicari == "energi":
                hasil = a * b
                persamaan = f"E = {format_angka(a)} × {format_angka(b)}"
                satuan = "J"
            elif dicari == "daya":
                if b == 0:
                    raise ZeroDivisionError
                hasil = a / b
                persamaan = f"P = {format_angka(a)} / {format_angka(b)}"
                satuan = "W"
            else:
                if b == 0:
                    raise ZeroDivisionError
                hasil = a / b
                persamaan = f"t = {format_angka(a)} / {format_angka(b)}"
                satuan = "s"

        if not (-1e300 < hasil < 1e300):
            raise ValueError

        hasil_rumus = {
            "nilai": format_angka(hasil),
            "satuan": satuan,
            "persamaan": persamaan,
        }

    except ZeroDivisionError:
        error_rumus = "Nilai pembagi tidak boleh nol."
    except (ValueError, OverflowError):
        error_rumus = "Masukkan angka valid dan periksa kembali nilainya."

    return tampilkan_halaman(
        rumus_aktif=rumus,
        besaran_dicari=dicari,
        nilai1=nilai1,
        nilai2=nilai2,
        hasil_rumus=hasil_rumus,
        error_rumus=error_rumus,
    )


@app.route("/hapus-riwayat", methods=["POST"])
def hapus_riwayat():
    session.pop("riwayat", None)
    return tampilkan_halaman("arus")


if __name__ == "__main__":
    app.run(debug=True)