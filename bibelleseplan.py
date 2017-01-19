import xlsxwriter
import time
import datetime
from datetime import date
import math

from definitions import BOOKS
from section import Section
import definitions as DEF

COLS_PER_DAY = 4

# user definitions
chapters_p_day = [1, 3]
num_cols = 3
section_str = "Mt - Offb, 1 Mos - Mal"
s_date = "10.1.2017"

# parse input arguments
start = datetime.datetime.strptime(s_date, "%d.%m.%Y").date()
sections = Section.parseSections(section_str, chapters_p_day)

# prepare excel file
workbook = xlsxwriter.Workbook(start.strftime("%d.%m.%Y") + "_" + section_str.replace(" ", "").replace("-", "_") + ".xlsx")
worksheet = workbook.add_worksheet()

# duration calculation
sum_chapters = 0
sum_chapters_p_day = 0
for section in sections:
  sum_chapters += section.sum_chapters
  sum_chapters_p_day += section.chapters_p_d

num_days = int(sum_chapters/sum_chapters_p_day)    
num_lines = math.ceil((sum_chapters/sum_chapters_p_day)/num_cols)

day = 0
while day <= num_days:

  worksheet.write(day, 0, (start + datetime.timedelta(days=day)).strftime("%d.%m.%Y"))
  for i, section in enumerate(sections):
    [book, chapter, remaining_chapters] = section.iterateDay()
    
    worksheet.write(day, 1 + i*2, book)
    worksheet.write(day, 2 + i*2, chapter)
    
    # section is finished
    if remaining_chapters and len(sections) > 1:
      sections.remove(section)
      
      # add free chapters to section with longest duration (list is sorted!)
      sections[0].addRestFromFinishedSection(remaining_chapters, section.chapters_p_d)
    
  day = day + 1

workbook.close()
