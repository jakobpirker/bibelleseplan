import xlsxwriter
import time
import datetime
from datetime import date
import math

from definitions import BOOKS

def getSectionBorders(section_str):

  section_borders = section_str.split("-")

  for i, abbr in enumerate(section_borders):
    section_borders[i] = abbr.strip()
  
  book_abbr = []
  
  for book in BOOKS:
    book_abbr.append(book.short_name)
  
  return {'s': book_abbr.index(section_borders[0]), 'e': book_abbr.index(section_borders[1])}
 
COLS_PER_DAY = 4

# user definitions
chapters_p_day = 1
num_cols = 3
section_str = "1 Mos - Mal"
s_date = "10.1.2017"

# parse input arguments
start = datetime.datetime.strptime(s_date, "%d.%m.%Y").date()
sections = getSectionBorders(section_str)
  

# prepare excel file
workbook = xlsxwriter.Workbook(start.strftime("%d.%m.%Y") + "_" + BOOKS[sections['s']].short_name.replace(" ", "") + "_" +  BOOKS[sections['e']].short_name.replace(" ", "") + ".xlsx")
worksheet = workbook.add_worksheet()
 
# just use selected books
books = BOOKS[sections['s']:sections['e'] + 1]

# column calculations
sum_chapters = 0
for book in books:
  sum_chapters = sum_chapters + book.length
  
num_lines = int(math.ceil((sum_chapters/chapters_p_day)/num_cols))

current_chapter = chapters_p_day
day = 0

for book in books:
  
  while current_chapter <= book.length:
    col = int(day/num_lines)
    line = day - col*num_lines
    
    worksheet.write(line, COLS_PER_DAY*col + 0, (start + datetime.timedelta(days=day)).strftime("%d.%m.%Y"))
    worksheet.write(line, COLS_PER_DAY*col + 1, book.short_name)
    worksheet.write(line, COLS_PER_DAY*col + 2, current_chapter)
    
    day = day + 1
    current_chapter = current_chapter + chapters_p_day
    
  current_chapter = current_chapter - book.length
    
workbook.close()