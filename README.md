# Konwerter-xml.json.yml-

File Converter to narzędzie umożliwiające konwersję plików między formatami XML, JSON oraz YAML. Program posiada zarówno interfejs wiersza poleceń, jak i prosty UI użytkownika oparty na PyQt5.

## Funkcje

- Konwersja plików XML, JSON i YAML
- Intuicyjny graficzny interfejs użytkownika
- Obsługa wiersza poleceń do szybkiej konwersji

## Wymagania

- Python 3.x
- PyQt5
- PyYAML

## Instalacja

Aby zainstalować wymagane pakiety, uruchom skrypt `installResources.ps1`:

##lub ręcznie zainstaluj wymagane pakiety:

```pip install PyQt5 pyyaml```

## Sposób użycia

Aby uruchomić program z interfejsem graficznym, po prostu uruchom skrypt project.py bez dodatkowych argumentów:

```python konwerter.py```

## Wiersz poleceń

```python konwerter.py input_file output_file```

## Przykład

```python konwerter.py data/input.xml data/output.json```

## Kompilacja do pliku .exe

Aby skompilować program do pliku wykonywalnego (.exe) użyj PyInstaller:

```pyinstaller --onefile --noconsole konwerter.py```

## Autor

- Maksymilian Haas 52686











