import re

def siivoa_kirja_tarkasti(input_tiedosto, output_tiedosto):
    print(f"Luetaan tiedostoa '{input_tiedosto}'...")
    with open(input_tiedosto, "r", encoding="utf-8") as f:
        sisalto = f.read()

    # 1. Poistetaan chevron_left ja more_vert -roinat sekä niiden välinen sisältö
    sisalto = re.sub(r'chevron_left.*?more_vert', '', sisalto, flags=re.DOTALL)
    sisalto = sisalto.replace('chevron_left', '').replace('more_vert', '')

    # 2. Käsitellään teksti rivi riviltä säilyttäen alkuperäiset rivinvaihdot
    rivit = sisalto.splitlines()
    uudet_rivit = []

    for rivi in rivit:
        # Ohitetaan pelkät sivuerotinviivat, jos niitä jäi roikkumaan
        if rivi.strip() == "---":
            continue

        puhdas_rivi = rivi.strip()
        
        # Jos rivi on tyhjä, säilytetään se (kappalejako säilyy)
        if not puhdas_rivi:
            uudet_rivit.append("")
            continue

        # Etsitään rivin ensimmäinen kirjain
        eka_kirjain = None
        for char in puhdas_rivi:
            if char.isalpha():
                eka_kirjain = char
                break

        # Heuristiikka: jos rivi alkaa pienellä kirjaimella, liitetään se edelliseen riviin
        if eka_kirjain and eka_kirjain.islower() and uudet_rivit:
            # Etsitään uutesta listasta viimeisin ei-tyhjä rivi, johon pätkä yhdistetään
            viimeisin_idx = len(uudet_rivit) - 1
            while viimeisin_idx >= 0 and not uudet_rivit[viimeisin_idx].strip():
                viimeisin_idx -= 1
            
            if viimeisin_idx >= 0:
                uudet_rivit[viimeisin_idx] = uudet_rivit[viimeisin_idx].rstrip() + " " + puhdas_rivi
            else:
                uudet_rivit.append(rivi)
        else:
            # Muussa tapauksessa säilytetään rivi sellaisenaan omalla rivillään
            uudet_rivit.append(rivi)

    # 3. Kirjoitetaan tulos uuteen tiedostoon
    with open(output_tiedosto, "w", encoding="utf-8") as f:
        f.write("\n".join(uudet_rivit))

    print(f"Valmista! Alkuperäinen rivitys säilytetty ja pienellä alkavat liitetty. Tallennettu: {output_tiedosto}")

if __name__ == "__main__":
    siivoa_kirja_tarkasti("kirja_vihrea.txt", "kirja_puhdas.txt")
