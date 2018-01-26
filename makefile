# Need to export as ENV var
export TEMPLATE_DIR = templates
export QUIZ_DIR = quizzes
PTML_DIR = html_src
DJANGO_DIR = TheDevOpsCourse/devops/templates

INCS = $(TEMPLATE_DIR)/menu.txt 

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 utils/html_checker.py $<
	utils/html_include.awk <$< >$@
	python3 utils/html2django.py $< >$(DJANGO_DIR)/$@
	git add $@
# at the moment the git stuff below is not working:
#	cd $(DJANGO_DIR) ; git add $(DJANGO_DIR)/$@
#	cd $(DJANGO_DIR) ; git commit $(DJANGO_DIR)/$@ -m "Rebuilt from DevOps site."
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
