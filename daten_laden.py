"""Lädt Tagesschlusskurse von Bitcoin und Gold ab 2017 und speichert sie als CSV.

Goldpreis (siehe Methodik, Entscheidung E5):
- GLD:  SPDR Gold Shares, ETF mit physischem Gold, bildet den LBMA Gold Price PM ab
        (Hauptreihe, kein Rollover).
- GC=F: Gold-Future COMEX, nächste Fälligkeit (Kontrollreihe, hat Rollover-Sprünge).
"""
from pathlib import Path

import yfinance as yf

START = "2017-01-01"
TICKER = {
    "bitcoin": "BTC-USD",  # Bitcoin in USD, wird 7 Tage pro Woche gehandelt
    "gold_gld": "GLD",     # Gold-ETF in USD, nur an Börsentagen (NYSE)
    "gold_gcf": "GC=F",    # Gold-Future in USD, nur an Börsentagen (COMEX)
}
DATEN_ORDNER = Path(__file__).parent / "daten"


def lade_kurse(ticker: str):
    """Lädt die Schlusskurse eines Tickers ab START und gibt eine Tabelle zurück."""
    df = yf.download(ticker, start=START, auto_adjust=True,
                     progress=False, multi_level_index=False)
    if df.empty:
        raise RuntimeError(f"Keine Daten für {ticker} erhalten.")
    df = df[["Close"]].rename(columns={"Close": "schlusskurs"})
    df.index.name = "datum"
    return df


def main():
    DATEN_ORDNER.mkdir(exist_ok=True)
    for name, ticker in TICKER.items():
        df = lade_kurse(ticker)
        df.to_csv(DATEN_ORDNER / f"{name}.csv")
        print(f"{name:9} ({ticker:7}): {len(df):5} Tage, "
              f"{df.index.min().date()} bis {df.index.max().date()}, "
              f"fehlende Werte: {df['schlusskurs'].isna().sum()}")


if __name__ == "__main__":
    main()
