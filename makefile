# Need to export as ENV var
export TEMPLATE_DIR = templates
export QUIZ_DIR = quizzes
PTML_DIR = html_src
DJANGO_DIR = TheDevOpsCourse
TEMPL_PATH = devops/templates
TEMPL_DIR = $(DJANGO_DIR)/$(TEMPL_PATH)
UTILS_DIR = utils

INCS = $(TEMPLATE_DIR)/menu.txt 

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $<
	$(UTILS_DIR)/html_include.awk <$< >$@
#	python3 $(UTILS_DIR)/html2django.py $< >$(TEMPL_DIR)/$@
#	git add $@
#	cd $(DJANGO_DIR) ; git add $(TEMPL_PATH)/$@
#	cd $(DJANGO_DIR) ; git commit $(TEMPL_PATH)/$@ -m "Rebuilt from DevOps site."
#	cd $(DJANGO_DIR) ; git push origin master; cd -

website: $(INCS) $(HTMLFILES)
	-git commit -a -m "Website rebuild."
	git push origin master

tests: $(QUIZ_DIR)
	cd $(QUIZ_DIR) ; make all

local: $(HTMLFILES)

template: $(TEMPLATE_DIR)
	cd $(TEMPLATE_DIR) ; make all

clean:
	rm $(HTMLFILES)
	cd $(TEMPLATE_DIR) ; make clean
