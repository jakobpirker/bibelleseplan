import xlsxwriter
import time
import datetime
import argparse
from datetime import date
import math

from definitions import BOOKS
from section import Section
import definitions as DEF

# parse command-line-arguments
parser = argparse.ArgumentParser(description="Create a bible reading plan, based on" 
  " reading a certain amount of chapters a day, and creates an according excel file")
parser.add_argument('-sec', nargs=1, type=str,
  help = "list of the sections that should be used, e.g. '1 Mos - Mal, Mt - Offb' for book names see definitions.py")
parser.add_argument('-ch', nargs=1, type=str,
  help = "list of the numbers of chapters a day for a specific, according to the order given in -s, e.g. '1 3'")
parser.add_argument('-d', nargs=1, type=str, help = "starting date, e.g. '17.1.2017'")
parser.add_argument('-col', nargs=1, type=int, help = "number of columns the excel file should have")

args = parser.parse_args()
  
# user definitions
chapters_p_day = [int(ch) for ch in args.ch[0].split()]
num_cols = args.col[0]
section_str = args.sec[0]
s_date = args.d[0]

# parse input arguments
start = datetime.datetime.strptime(s_date, DEF.DATE_FORMAT).date()
sections = Section.parseSections(section_str, chapters_p_day)

# duration calculation
sum_chapters = 0
sum_chapters_p_day = 0
for section in sections:
  sum_chapters += section.sum_chapters
  sum_chapters_p_day += section.chapters_p_d

num_days = int(sum_chapters/sum_chapters_p_day)    
num_lines = math.ceil((sum_chapters/sum_chapters_p_day)/num_cols)

# prepare excel file
wb_name = "reading_plan_" + start.strftime(DEF.DATE_FORMAT) + ".xlsx"
workbook = xlsxwriter.Workbook(wb_name)
worksheet = workbook.add_worksheet()

day = 0
s_col = 0 # "start (leftest)" column of a new seperated column-area
line = 0
removed_elements = 0
while day <= num_days:

  worksheet.write(line, s_col, (start + datetime.timedelta(days=day)).strftime(DEF.DATE_FORMAT))
  for i, section in enumerate(sections):
    [book, chapter, remaining_chapters] = section.iterateDay()
    
    worksheet.write(line, s_col + 1 + i*DEF.COLS_PER_SEC, book)
    worksheet.write(line, s_col + 2 + i*DEF.COLS_PER_SEC, chapter)
    
    # section is finished
    if remaining_chapters and len(sections) > 1:
      sections.remove(section)
      removed_elements += 1
      # add free chapters to section with longest duration (list is sorted!)
      sections[0].addRestFromFinishedSection(remaining_chapters, section.chapters_p_d)
    
  day = day + 1
  
  line = day % num_lines  
  if(not line):
    # + 2 for date and free column
    s_col += (len(sections) + removed_elements)*DEF.COLS_PER_SEC + 2
    removed_elements = 0

workbook.close()
