# -----------------------------------------------------------
# class representing a section of the reading plan
# section ... a range of consecutive books
#
# section_str   string containing section description e.g. "Mt - Offb"        
# chapters_p_d  number of chapters to read per day

from definitions import BOOKS

class Section:

  # static member, contains all short names of the bible-books in a list
  book_names = [book.short_name for book in BOOKS]

  def __init__(self, section_str, chapters_p_d):
    
    border_names = section_str.strip().split("-")
    
    # section must have one book to start and one to end
    if len(border_names) != 2:
      raise ValueError("getSectionBorders: Choosen sections are invalid")
    
    # extract the indices of the books
    inds = sorted([Section.book_names.index(border.strip()) for border in border_names])
    
    self.ind_s = inds[0]
    self.ind_e = inds[1]
    
    self.name_s = Section.book_names[self.ind_s]
    self.name_e = Section.book_names[self.ind_e]
    self.chapters_p_d = chapters_p_d

  def __str__(self):
    return self.name_s + "_" + self.name_e
