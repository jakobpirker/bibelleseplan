import xlsxwriter
import time
import datetime
from datetime import date
import math

from definitions import BOOKS
import definitions as DEF

def getSectionBorders(section_str):

  # create a list with all abbreviations for the books
  abbr = []  
  for book in BOOKS:
    abbr.append(book.short_name)

  sec_ind = []
  for section in section_str.split(","):
    section_borders = section.strip().split("-")

    # section must have one book to start and one to end
    if len(section_borders) != 2:
      raise ValueError("getSectionBorders: Choosen sections are invalid")

    # 0 ... start index, 1 ... end index
    sec_ind.append([abbr.index(section_borders[0].strip()), abbr.index(section_borders[1].strip())])

  return sec_ind
 
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
workbook = xlsxwriter.Workbook(start.strftime("%d.%m.%Y") + "_" + section_str.replace(" ", "") + ".xlsx")
worksheet = workbook.add_worksheet()
 
# just use selected books
books = BOOKS[sections[0][0]:sections[0][1] + 1]

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