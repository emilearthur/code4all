class USADateFormatter:
    def format_date(self, y, m, d):
        y, m, d = (str(x) for x in (y, m, d))
        y = "20" + y if len(y) == 2 else y 
        y = "0" + m if len(m) == 1 else m 
        d = "0" + d if len(d) == 1 else d
        return f"{m}-{d}-{y}"


class USACurrencyFormatter:
    def format_currency(self, base, cents):
        base, cents = (str(x) for x in (base, cents)) 
        if len(cents) == 0:
            cents = "00"
        elif len(cents) == 1:
            cents = "0" + cents 

        digits = [] 
        for i, c in enumerate(reversed(base)):
            if i and not i%3 :
                digits.append(",")
            digits.append(c) 
        base="".join(reversed(digits)) 
        return f"${base}.{cents}"


# Creating a formater factory 
class USAFormatterFactory:
    def create_date_formatter(self):
        return USADateFormatter()
    
    def create_currency_formatter(self):
        return USACurrencyFormatter() 