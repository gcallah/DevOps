# Need to export as ENV var
export TEMPLATE_DIR = templates
export QUIZ_DIR = quizzes
PTML_DIR = html_src
DJANGO_DIR = TheDevOpsCourse
DTEMPL_PATH = devops/templates
DTEMPL_DIR = $(DJANGO_DIR)/$(DTEMPL_PATH)
UTILS_DIR = utils

INCS = $(TEMPLATE_DIR)/navbar.txt $(TEMPLATE_DIR)/head.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $< -u
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@
#	python3 $(UTILS_DIR)/html2django.py $< >$(DTEMPL_DIR)/$@
#	cd $(DJANGO_DIR) ; git add $(DTEMPL_PATH)/$@
#	cd $(DJANGO_DIR) ; git commit $(DTEMPL_PATH)/$@ -m "Rebuilt from DevOps site."
#	cd $(DJANGO_DIR) ; git push origin master; cd -

website: $(INCS) $(HTMLFILES)
	-git commit -a 
	git pull origin master
	git push origin master

local: $(HTMLFILES)

clean:
	touch $(PTML_DIR)/*.ptml
	cd build; $(PTML_DIR)/*.ptml; make local; cd ..
	cd cloud; $(PTML_DIR)/*.ptml; make local; cd ..
	cd coding; $(PTML_DIR)/*.ptml; make local; cd ..
	cd deployment; $(PTML_DIR)/*.ptml; make local; cd ..
	cd monitoring; $(PTML_DIR)/*.ptml; make local; cd ..
	cd security; $(PTML_DIR)/*.ptml; make local; cd ..
	cd testing; $(PTML_DIR)/*.ptml; make local; cd ..
	cd workflow; $(PTML_DIR)/*.ptml; make local; cd ..
	cd UX; $(PTML_DIR)/*.ptml; make local; cd ..
