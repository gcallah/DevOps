# Need to export the next two as ENV vars
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
	./test_html.sh $< $(UTILS_DIR)
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

website: $(INCS) $(HTMLFILES)
	-git commit -a 
	git pull origin master
	git push origin master

local: $(HTMLFILES)

all:
	make local
	cd build; make local; cd ..
	cd cloud; make local; cd ..
	cd coding; make local; cd ..
	cd deployment; make local; cd ..
	cd journals; make local; cd ..
	cd monitoring; make local; cd ..
	cd reviews; make local; cd ..
	cd security; make local; cd ..
	cd testing; make local; cd ..
	cd workflow; make local; cd ..
	cd UX; make local; cd ..

clean:
	touch $(PTML_DIR)/*.ptml; make local
	cd build; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd cloud; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd coding; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd deployment; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd journals; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd monitoring; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd reviews; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd security; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd testing; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd workflow; touch $(PTML_DIR)/*.ptml; make local; cd ..
	cd UX; touch $(PTML_DIR)/*.ptml; make local; cd ..
