import xlsxwriter
import time
import datetime
from datetime import date

# constant definitions
book_names = ["1 Mos", "2 Mos", "3 Mos", "4 Mos", "5 Mos", "Jos", "Ri", "Rut", "1 Sam", "2 Sam", "1 Koe", "2 Koe", "1 Chr", "2 Chr", "Esra", "Neh", "Est", "Hi", "Ps", "Spr", "Pred", "Hld", "Jes", "Jer", "Klgl", "Hes", "Dan", "Hos", "Joel", "Am", "Obd", "Jona", "Mi", "Nah", "Hab", "Zef", "Hag", "Sach", "Mal", "Mt", "Mk", "Lk", "Joh", "Apg", "Roem", "1 Kor", "2 Kor", "Gal", "Eph", "Phil", "Kol", "1 Thess", "2 Thess", "1 Tim", "2 Tim", "Tit", "Phlm", "Hebr", "Jak", "1 Petr", "2 Petr", "1 Joh", "2 Joh", "3 Joh", "Jud", "Offb"]           
book_lengths = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 4, 9, 1, 4, 7, 3, 3, 3, 2, 14, 3, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]

# user definitions
chapters_p_day = 4
max_lines = 49
input = "10.1.2017"
start = datetime.datetime.strptime(input, "%d.%m.%Y").date()

# prepare excel file
workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()
 
current_chapter = chapters_p_day
day = 0
 
for i, book in enumerate(book_names):
  
  while current_chapter <= book_lengths[i]:
    col = int(day/max_lines)
    line = day - col*max_lines
    
    worksheet.write(line, 4*col + 0, (start + datetime.timedelta(days=day)).strftime("%d.%m.%Y"))
    worksheet.write(line, 4*col + 1, book)
    worksheet.write(line, 4*col + 2, current_chapter)
    
    day = day + 1
    current_chapter = current_chapter + chapters_p_day
    
  current_chapter = current_chapter - book_lengths[i]
    
workbook.close()