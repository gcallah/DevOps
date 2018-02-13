# Need to export as ENV var
export TEMPLATE_DIR = ../templates
export QUIZ_DIR = ../quizzes
PTML_DIR = html_src   
INCS = $(TEMPLATE_DIR)/menu.txt 

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///') 

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 ../utils/html_checker.py $<   # added ../utils/html_checker.py
	../utils/html_include.awk <$< >$@

local: $(HTMLFILES)

