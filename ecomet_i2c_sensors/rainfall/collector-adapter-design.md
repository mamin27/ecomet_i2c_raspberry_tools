# Zberač dažďa: návrh redukčného lievika

## Cieľ a rozsah

Navrhnúť otvorený, obrátene skosený ihlan, ktorý sa nasadí na existujúci
zberač s horným rozhraním `50 × 110 mm` a rozšíri vstupnú plochu na zvolenú
referenčnú zbernú plochu `200 cm²`. Táto plocha je návrhový cieľ; sama osebe
neznamená zhodu s konkrétnou normou ani úplnú meteorologickú certifikáciu.

## Odporúčaná geometria

| Parameter | Hodnota |
|---|---:|
| Dolná základňa, rozhranie s existujúcim zberačom | `50 × 110 mm` |
| Horný otvor | štvorec `141,4 × 141,4 mm` |
| Plocha horného otvoru | `20 000 mm² = 200 cm²` |
| Výška nástavca | `45,7 mm` |
| Poloha otvoru | vycentrovaný nad dolnou základňou |

Štvorec je zvolený namiesto obdĺžnika pre jednoduchšiu výrobu a symetrický
vstup. Jeho strana vychádza z odmocniny plochy:

```text
strana = √20 000 mm² = 141,42 mm
```

Výška `45,7 mm` je praktický kompromis pre kompaktný nástavec. Zodpovedá
polovici rozšírenia kratšej strany (`(141,42 − 50) / 2`), teda približne
45° sklonu tejto steny od zvislice. Steny v smere dlhšej strany majú menší
sklon, približne 19° od zvislice. Rozmery priečnych rezov sa predpokladajú
meniť lineárne po celej výške.

## Plocha a meranie

Existujúca plocha `50 × 110 mm` je `5 500 mm² = 55 cm²`. Nový horný otvor má
3,636-násobnú plochu. Pri rovnakom úhrne zrážok preto zachytí približne
3,636-násobný objem vody oproti vstupu s plochou `55 cm²`. Ak sa zozbieraný
objem prevádza na výšku zrážok, prevod treba kalibrovať podľa novej plochy
otvoru (`200 cm²`): pri tejto ploche zodpovedá `1 mm` zrážok objemu `20 ml`
(pri pôvodných `55 cm²` by to bolo `5,5 ml`).

## Nastavenie Python ovládača

Voľba zbernej plochy sa nastavuje v `~/.comet/config.yaml` pod samostatným
vrchným kľúčom `rainfall` (na rovnakej úrovni ako `i2c`):

```yaml
rainfall:
  collector: original # original alebo attachment
```

- `original` — pôvodná plocha `50 × 110 mm = 55 cm²`; predvolená voľba.
- `attachment` — plocha horného otvoru `200 cm²`; Python ovládač násobí
  kumulatívne a hodinové zrážky faktorom `55/200 = 0,275`. Zapisovanie
  akumulovanej základnej hodnoty prepočítava opačným faktorom.

Ak kľúč `rainfall` alebo `collector` chýba, použije sa `original`. Iná
hodnota `collector` vyvolá chybu konfigurácie. Surový počet preklopení
zostáva bez úpravy.

## Objemový odhad

Pri lineárne sa meniacich stranách obdĺžnikového prierezu je objem nástavca:

```text
V = h/6 × (2a₀b₀ + a₀b₁ + a₁b₀ + 2a₁b₁)
```

Pre `a₀ = 50 mm`, `b₀ = 110 mm`, `a₁ = b₁ = 141,42 mm` a `h = 45,7 mm`
vychádza približne `560 927 mm³`, teda **560,9 ml**. Ak nástavec tvorí
spojitú dutinu s pôvodným priestorom s odhadovaným objemom `107,54 ml`,
celkový objem po horný okraj je približne **668,5 ml**. Výpočet nezahŕňa
zaoblenia, hrúbku stien, spoje ani zvyškovú vodu.

Existujúci priechodný otvor s priemerom `3 mm` sa ponechá ako výpust.
Priemer otvoru nemení teoretický objem dutiny; ovplyvňuje odtok a prípadnú
zvyškovú vodu.

## Predpoklady a obmedzenia

- Dolná plocha nástavca presne nadväzuje na existujúci obdĺžnik `50 × 110 mm`.
- Horný štvorec je vodorovný a vycentrovaný; steny sa nemenia skokovo.
- Rozmer `200 cm²` je referenčná plocha zvolená pre tento návrh, nie tvrdenie
  o zhode s normou. Na posúdenie zhody treba určiť konkrétnu normu a overiť
  aj jej požiadavky na tvar, okraj, umiestnenie a konštrukciu zberača.
- Pred výrobou treba overiť dostupný priestor, hrúbku stien, spôsob uchytenia
  a to, či otvor dokáže odvádzať vodu dostatočne rýchlo.
