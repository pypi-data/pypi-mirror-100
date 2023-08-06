# Bddk Data

This package helps you to collect your desired data from Bddk via selenium. 
Since this package automates browser, you do not need to use the interface of Bddk. 
Thus, ultimate aim is that one should able to get whatever data needed from Bddk without leaving python environment and visiting the 
site over and over again. 

### Prerequisites

OS - Windows, Linux or Mac

Browser - Chrome or Ubuntu

### Installing

Importing package should install all necessary files and programs for you.

In case of a problem;

[ChromeDriver](https://chromedriver.chromium.org/) for Chrome

[geckodriver](https://github.com/mozilla/geckodriver/releases) for Firefox

## Important Note

Both ChromeDriver and geckodriver are open source programs. They will be automatically installed on you computer and used accordingly.
However, Linux and Mac do not give permission to ChromeDriver for using Chrome. This package forces to run ChromeDriver program if that happens.

## Patch Notes v1.1

- **Support for weekly data is added**
- New functions are been created for weekly data and information
- Function names are been simplified
- Drivers are been updated in order to match latest versions of browsers
- New "dev" argument is been added for all current functions
- Several bugfixes and optimization 

# How to Use

### Getting the Data

Returns dataframe

```
bddk.aylik_rapor(kalem, basyil, basay, bityil, bitay, per, para="TL", taraf=None, zaman=120, browser="firefox", dev=False)

Paremeters:
    kalem : list, use get_kalem for suitable elements
        Kalemler
    basyil, bityil : str or int, year
        Baslangıç Yılı, Bitiş Yılı
    basay, bitay : str, months
        Baslangıç Ayı, Bitiş Ayı
    per : "3 Aylık", "6 Aylık", "Yıllık"
        Periyot
    para : "TL" (default), "USD" 
        Para Birimi
    taraf: list, use aylik_taraf for suitable elements
        Taraflar, "Sektör" her zaman seçilidir, bunun dışında istediklerinizi liste olarak ekleyin.
    zaman : int, 120 (default)
        Sitenin veya internetinizin durumuna göre paket zaman aşımına uğrayabilir. Yoğunluk durumunda arttırmanız tavsiye edilir.
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı
    dev: boolean; True, False (default)
        Arkaplanda çalışan browser'ı görmenizi sağlar. Karşılaştığınız hataları düzeltmek ya da pakedi geliştirmek isterseniz için bu modu kullanın.

#######################################################

bddk.haftalik_rapor(kalem, bastarih, bittarih, para=None, sutun=None, taraf=None, zaman=30, browser="chrome",dev=False)

Paremeters:
    kalem: list, use get_kalem for suitable elements
        Kalemler
    bastarih, bittarih: str
        Fonksiyon için spesifik düzende tarih string'leri gereklidir. bkz. bddk.haftalik_tarih()
    para: str, "USD", None
        "TL" her zaman seçilidir.
    sutun: str, "TP", "YP", None
        "Toplam" her zaman seçilidir.
    taraf: list, use haftalik_taraf for suitable elements
        Taraflar, "Sektör" her zaman seçilidir, bunun dışında istediklerinizi liste olarak ekleyin.
    zaman : int, 30 (default)
        Sitenin veya internetinizin durumuna göre paket zaman aşımına uğrayabilir. Yoğunluk durumunda arttırmanız tavsiye edilir.
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı
    dev: boolean; True, False (default)
        Arkaplanda çalışan browser'ı görmenizi sağlar. Karşılaştığınız hataları düzeltmek ya da pakedi geliştirmek isterseniz için bu modu kullanın.
```
#### Example
```
rapor = bddk.aylik_rapor(
    kalem=["Menkul Kıymetler-Finansman Bonoları", "Menkul Kıymetler-Hazine Bonoları"],
    basyil=2014,
    basay="Ocak",
    bityil=2020,
    bitay="Mart",
    per="1 Aylık",
    taraf=["Mevduat"],
    zaman=60,
    browser="chrome"
)
print(rapor.head())

#######################################################

rapor2 = bddk.haftalik_rapor(
    kalem=["Krediler", "Mevduat"],
    bastarih="08.01.2021 (02.Hafta)",
    bittarih="19.3.2021 (12.Hafta)",
    para="USD",
    sutun="TP",
    taraf=["Mevduat","Kamu"],
    zaman=30,
    browser="firefox",
    dev=True
)
print(rapor2.head())
```
### Getting Kalem, Taraf and Tarih

All functions print available strings and do not return any object. 
```
bddk.aylik_kalem(kalems=None, browser="firefox", dev=False)

Parameters:
    kalems : str, returns full names of available kalem that consists of this string
        Kalem arama
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı
    dev: boolean; True, False (default)
        Arkaplanda çalışan browser'ı görmenizi sağlar. Karşılaştığınız hataları düzeltmek ya da pakedi geliştirmek isterseniz için bu modu kullanın.   

#######################################################

bddk.aylik_taraf(browser="firefox", dev=False)
    
Parameters:
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı
    dev: boolean; True, False (default)
        Arkaplanda çalışan browser'ı görmenizi sağlar. Karşılaştığınız hataları düzeltmek ya da pakedi geliştirmek isterseniz için bu modu kullanın. 
    
#######################################################

bddk.haftalik_kalem(browser="chrome", dev=False)
    
Parameters:
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı
    dev: boolean; True, False (default)
        Arkaplanda çalışan browser'ı görmenizi sağlar. Karşılaştığınız hataları düzeltmek ya da pakedi geliştirmek isterseniz için bu modu kullanın. 

#######################################################

bddk.haftalik_taraf(browser="chrome", dev=False)
    
Parameters:
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı
    dev: boolean; True, False (default)
        Arkaplanda çalışan browser'ı görmenizi sağlar. Karşılaştığınız hataları düzeltmek ya da pakedi geliştirmek isterseniz için bu modu kullanın. 

#######################################################

bddk.haftalik_tarih(tarih="baslangic", browser="chrome", dev=False)

Parameters:
    tarih: str, "baslangic" (default), "bitis"
        Baslangic veya bitis tarihleri. Duzenleri birbirinden farklıdır!
    browser: "chrome" or "firefox"
        Kullandığınız web tarayıcı
    dev: boolean; True, False (default)
        Arkaplanda çalışan browser'ı görmenizi sağlar. Karşılaştığınız hataları düzeltmek ya da pakedi geliştirmek isterseniz için bu modu kullanın. 
```
#### Example
```
bddk.aylik_kalem("bono",browser="firefox")

bddk.aylik_taraf(browser="firefox")

bddk.haftalik_kalem()

bddk.haftalik_taraf(dev=True)

bddk.haftalk_tarih(tarih="bitis")
```

## Authors

* **İlyas Burak Hızarcı** - [barbasan](https://github.com/barbasan)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

