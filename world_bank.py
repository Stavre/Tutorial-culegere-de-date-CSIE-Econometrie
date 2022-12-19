import pandas as pd
import wbdata


# Acest fișier conține câteva indicații pentru utilizarea librăriei wbdata
# în realizarea proiectului pentru Econometrie

def init():
    """wrapper function around wbdata's get_source(), get_indicator(), and get_country().
    Saves data in three csv files: countries, data_series, and data_sources"""
    data_sources = pd.DataFrame(wbdata.get_source())
    data_sources.to_csv("data_sources.csv", index=False)
    data_series = wbdata.get_indicator()
    data_series = pd.DataFrame(data_series)
    data_series.to_csv("data_series.csv", index=False)
    get_countries().to_csv("countries.csv", index=False)


def get_countries():
    """gets a DataFrame of all countries available in the API"""
    countries = wbdata.get_country()
    countries_df = pd.DataFrame(countries)
    return countries_df



# funcție init salvează o listă cu tările, bazele de date și seriile de timp disponibile în wbdata
# init()

# pentru a vedea seriile de timp disponibile într-o singură bază de date
# se folosește funcția get_indicator(source=<id-ul bazei de date>
# ex
time_series = wbdata.get_indicator(source=3)
print(time_series)

# pentru a căuta țări după nume se folosește funcția wbdata.search_countries(<nume>)
# ex

countries = wbdata.search_countries('united')
print(countries)

# pentru a accesa o serie de timp de folosește funcția
# wbdata.get_dataframe()
# ex

indicators = {"IC.BUS.EASE.XQ": "doing_business", "NY.GDP.PCAP.PP.KD": "gdppc"}
# indicators este un dicționar unde cheile sunt id-ul seriilor de timp
# iar valorile sunt denumirile pe care seriile de timp le vor avea in dataframe


countries = ['ARE', 'USA']
# countries este o listă de țări pentru care accesăm seriile de timp
# daca acest parametru nu este specificat, obținem seriile de date pentru toate țările

# convert_date: dacă este True, va schimba datele calendaristice în obiecte Date
df = wbdata.get_dataframe(indicators, country=countries, convert_date=True)
print(df)

# mai multe detalii pot fi găsite pe site-ul oficial: https://wbdata.readthedocs.io/en/stable/






