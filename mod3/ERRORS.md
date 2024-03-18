## 1.

Ошибка:

    self.yob - now.year
Исправлено:
    
    now.year - self.yob 

## 2.
Ошибка:
   
    self.name = self.name
Исправлено:
    
    self.name = name 

## 3.
Ошибка:
   
    self.address == address
Исправлено:
    
    self.address = address

## 4.
Ошибка:
   
    return address is None
Исправлено:
    
    return self.address is None