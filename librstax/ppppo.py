# origin: https://porezionline.rs/obrasci.php?pID=30216

ppppo_codes = {
    "101000": """
        Zarada i druga primanja koja imaju karakter zarade 
        iz čl. 13, 14, 14a i 14b Zakona o porezu na dohodak građana 
        („Službeni glasnik RS“, br. 24/01, 80/02, 80/02 - dr. zakon, 135/04, 62/06, 65/06 - ispravka, 
        31/09, 44/09, 18/10, 50/11, 91/11 - US, 93/12, 114/12 - US, 47/13, 48/13 - ispravka, 
        108/13, 57/14, 68/14 - dr. zakon, 112/15, 113/17, 95/18, 86/19, 153/20,
        44/21 i 118/21 - u daljem tekstu: Zakon),
        osim lične zarade preduzetnika, uključujući i zaposlenog u privrednom društvu čiji je osnivač,
        odnosno član, bez olakšica i bez staža osiguranja koji se zaposlenom računa sa uvećanim trajanjem.
    """,
    "110000": """
        Naknada dokumentovanih troškova prevoza za dolazak i odlazak sa rada,
        dnevnica za službeno putovanje u zemlji i inostranstvu,
        naknada troškova smeštaja na službenom putovanju,
        naknada prevoza na službenom putovanju, solidarna pomoć,
        jubilarna nagrada i pomoć u slučaju smrti člana porodice zaposlenog - preko neoporezivog iznosa.
    """,
}

ppppo_columns = {
  "3.1": "Šifra vrste prihoda isplaćena fizičkom licu.",
  "3.2": "Ukupna suma bruto prihoda.",
  "3.3": "Normirani troškovi, poreske olakšice i druga umanjenja.",
  "3.4": "Poreska osnovica nakon umanjenja.",
  "3.5": "Iznos obračunatog poreza.",
  "3.6": "Doprinosi za obavezno socijalno osiguranje na teret primaoca prihoda.",
  "3.7": "Doprinosi za obavezno socijalno osiguranje na teret isplatioca prihoda."
}


ppppo_funcs = {
    "101000": {
        "3.2": lambda summary: summary["Total gross salary"],
        "3.3": lambda summary: summary["Tax calculation/Non-taxable amount"],
        "3.4": lambda summary: ppppo_funcs["101000"]["3.2"](summary)-ppppo_funcs["101000"]["3.3"](summary),
        "3.5": lambda summary: round(ppppo_funcs["101000"]["3.4"](summary)/10, 0),
        "3.6": lambda summary: summary["Total employee contributions"],
        "3.7": lambda summary: summary["Total employer contributions"],
    },
    "110000": {
        "3.2": lambda summary: round(summary.get("Total compensation", 0) + summary.get("Tax on transportation (sum)", 0), 0),
        "3.3": lambda _: 0,
        "3.4": lambda summary: ppppo_funcs["110000"]["3.2"](summary)-ppppo_funcs["110000"]["3.3"](summary),
        "3.5": lambda summary: round(summary.get("Tax on transportation (sum)", 0), 0),
        "3.6": lambda _: 0,
        "3.7": lambda _: 0,
    },
}