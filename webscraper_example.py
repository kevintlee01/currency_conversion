from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import requests

class currencyExchange:
    def __init__(self, window, font):
        self.window = window
        self.font = font
        self.country_dict = dict()
        self.getCurrencies()
        self.setWidget()

    def setWidget(self):
        self.window.title("Currency Converter")

        self.amount1_text = tk.Label(self.window, text="Amount", font=self.font)
        self.amount2_text = tk.Label(self.window, text="Amount", font=self.font)
        self.from_currency_text = tk.Label(self.window, text="From Currency", font=self.font)
        self.to_currency_text = tk.Label(self.window, text="To Currency", font=self.font)

        self.textbox_amount1 = tk.Text(height="1", width="30", font=self.font)
        self.textbox_amount2 = tk.Text(height="1", width="30", font=self.font)
        self.textbox_amount2.config(state=tk.DISABLED)

        country_values = list(self.country_dict.keys())
        #print(country_values)

        self.from_box = ttk.Combobox(values=country_values, state="readonly", takefocus=0, font=self.font)
        self.to_box = ttk.Combobox(values=country_values, state="readonly", takefocus=0, font=self.font)
        self.from_box.current(0)
        self.to_box.current(0)

        self.button_swap = tk.Button(self.window, text="<->", command=self.swapCurrencies)
        self.button_convert = tk.Button(self.window, text="Convert", font=self.font, command=self.getExchangeRates)

        self.from_currency_text.grid(row=0, column=1, sticky=tk.W, padx=(10,10), pady=(10,0))
        self.to_currency_text.grid(row=0, column=3, sticky=tk.W, padx=(10,10), pady=(10,0))

        self.from_box.grid(row=1, column=1, sticky=tk.W, padx=(10,10), pady=(0,10))
        self.button_swap.grid(row=1, column=2, sticky=tk.S, pady=(0, 10))
        self.to_box.grid(row=1, column=3, sticky=tk.W, padx=(10,10), pady=(0,10))

        self.amount1_text.grid(row=2, column=1, sticky=tk.W, padx=(10,10), pady=(10,0))
        self.amount2_text.grid(row=2, column=3, sticky=tk.W, padx=(10,10), pady=(10,0))

        self.textbox_amount1.grid(row=3, column=1, sticky=tk.W, padx=(10,10), pady=(0,10))
        self.textbox_amount2.grid(row=3, column=3, sticky=tk.W, padx=(10,10), pady=(0,10))

        self.button_convert.grid(row=4, column=2, sticky=tk.N, pady=(10,10))

    def getCurrencies(self):
        source = requests.get("https://www.x-rates.com/table/?from=USD&amount=1").text
        soup = BeautifulSoup(source, "lxml")

        country_list = soup.find_all("option")
        for country in country_list:
            if "-" in country.text:
                code, name = country.text.split(" - ")
                self.country_dict[name] = code
        #print(self.country_dict)

    def getExchangeRates(self):
        #print(self.from_box.get())
        #print(self.to_box.get())
        source = requests.get("https://www.x-rates.com/table/?from=" + self.country_dict[self.from_box.get()] + "&amount=1").text
        soup = BeautifulSoup(source, "lxml")

        table = soup.find("table", class_="tablesorter ratesTable")
        rows = table.find_all("tr")
        conversion_hash = dict()
        conversion_hash[self.from_box.get()] = 1.0
        for row in rows:
            columns = row.find_all('td')
            columns = [element.text.strip() for element in columns]
            if len(columns) > 0:
                conversion_hash[columns[0]] = float(columns[1])

        #print(conversion_hash)
        self.setTextBoxValues(conversion_hash)

    def setTextBoxValues(self, conversion_hash):
        try:
            input = float(self.textbox_amount1.get("1.0", tk.END).strip())
            output = conversion_hash[self.to_box.get()]*input
        except ValueError:
            input = "VALUE ERROR"
            output = "VALUE ERROR"

        self.textbox_amount1.delete("1.0", tk.END)
        self.textbox_amount1.insert(tk.END, input)
        self.textbox_amount2.config(state=tk.NORMAL)
        self.textbox_amount2.delete("1.0", tk.END)
        self.textbox_amount2.insert(tk.END, output)
        self.textbox_amount2.config(state=tk.DISABLED)

    def swapCurrencies(self):
        from_currency = self.from_box.get()
        to_currency = self.to_box.get()

        self.from_box.set(to_currency)
        self.to_box.set(from_currency)

if __name__ == "__main__":
    window = tk.Tk()
    currencyExchange(window, ('arial', 11))
    window.mainloop()
