# -----------------------------------------------------------
# class representing a section of the reading plan
# section ... a range of consecutive books
#
# section_str   string containing section description e.g. "Mt - Offb"        
# chapters_p_d  number of chapters to read per day

import math

from definitions import BOOKS

class Section:

  # static member, contains all short names of the bible-books in a list
  book_names = [book.short_name for book in BOOKS]
  
  # creates a list of Section-objects from a string
  @staticmethod
  def parseSections(section_str, chapters_p_day):

    sections = []
    for i, section in enumerate(section_str.split(",")):
      sections.append(Section(section, chapters_p_day[i]))
    
    # sort sections with biggest duration first
    sections.sort(key=lambda section: section.num_days_, reverse = True)
        
    return sections

  def __init__(self, section_str, chapters_p_d):
    
    border_names = section_str.strip().split("-")
    
    # section must have one book to start and one to end
    if len(border_names) != 2:
      raise ValueError("getSectionBorders: Choosen sections are invalid")
    
    # extract the indices of the books
    inds = sorted([Section.book_names.index(border.strip()) for border in border_names])    
    self.ind_s_ = inds[0]
    self.ind_e_ = inds[1]
    
    self.chapters_p_d = chapters_p_d
    
    # start at first day with first book
    self.cur_chapter_ = self.chapters_p_d
    self.cur_book_ind = self.ind_s_
    self.cur_book_ = BOOKS[self.ind_s_]
    
    # sum of chapters for this section
    self.sum_chapters = 0    
    for i in range(self.ind_s_, self.ind_e_ + 1):
      self.sum_chapters += BOOKS[i].length
      
    self.num_days_ = self.sum_chapters/self.chapters_p_d

  def __str__(self):
    return Section.book_names[self.ind_s_] + "_" + Section.book_names[self.ind_e_]

  # returns the current book and chapter of the day, and increases the day
  def iterateDay(self):
    
    if self.cur_chapter_ <= self.cur_book_.length:
      # book is not finished yet
      ret_chapter = self.cur_chapter_
      self.cur_chapter_ += self.chapters_p_d
      # None ... remaining chapters -> section not finished
      return [self.cur_book_.short_name, ret_chapter, None]
    else:
      # book is finished -> select next if possible
      if self.cur_book_ind < self.ind_e_:
        # next book available (section not finished)
        self.cur_chapter_ -= self.cur_book_.length
        self.cur_book_ind = self.cur_book_ind + 1
        self.cur_book_ = BOOKS[self.cur_book_ind]
        return self.iterateDay()
      else:
        # next book not available (section finished)
        remaining_chapters = self.cur_chapter_ - self.cur_book_.length
        return [self.cur_book_.short_name, self.cur_book_.length, remaining_chapters]      
    return

  # adds the remaining chapters and chapters per day from a finished
  # section to the current section
  def addRestFromFinishedSection(self, remaining_chapters, add_chapters_p_d):
    self.cur_chapter_ += remaining_chapters
    self.chapters_p_d += add_chapters_p_d