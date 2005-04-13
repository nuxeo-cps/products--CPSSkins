.PHONY: clean doc perms i18n

all: check
	
check:
	pychecker2 *.py

perms:
	chmod -R go+r *

doc:
	happydoc -d doc/api *.py

clean:
	find . -name '*~' | xargs rm -f
	find . -name '*.pyc' | xargs rm -f
	find . -name '*.swp' | xargs rm -f
	find . -name '*.cln' | xargs rm -f
	find . -name '.log' | xargs rm -f
	rm -rf doc/api

	rm -f i18n/i18nchart.png

i18n:
# sync po files with pot
	i18ndude sync --pot i18n/cpsskins.pot -s \
           i18n/cpsskins-[a-z][a-z].po \
           i18n/cpsskins-[a-z][a-z]_[A-Z][A-Z].po
	i18ndude sync --pot i18n/cpsskins-default.pot -s \
           i18n/cpsskins-default-[a-z][a-z].po \
           i18n/cpsskins-default-[a-z][a-z]_[A-Z][A-Z].po
	i18ndude sync --pot i18n/cpsskins-plone.pot -s \
           i18n/cpsskins-plone-[a-z][a-z].po \
           i18n/cpsskins-plone-[a-z][a-z]_[A-Z][A-Z].po

i18n-en:
# add untranslated msgstrs from the English translations
	for pofile in i18n/*.po; do \
           i18ndude admix $$pofile i18n/cpsskins-en.po > i18n/temp-po; \
           mv -f i18n/temp-po $$pofile; \
        done

i18nchart:
# draw a chart
	i18ndude chart -o i18n/i18nchart.png --pot i18n/cpsskins.pot \
           i18n/cpsskins-[a-z][a-z].po \
           i18n/cpsskins-[a-z][a-z]_[A-Z][A-Z].po
