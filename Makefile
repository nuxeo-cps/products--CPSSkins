.PHONY: clean doc perms i18n

all: clean perms 

perms:
	chmod -R go+r *

doc:
	happydoc -d doc/api *.py

clean:
	find . -name '*~' | xargs rm -f
	find . -name '*pyc' | xargs rm -f
	find . -name '.log' | xargs rm -f
	rm -rf doc/api

	rm -f i18n/i18nchart.png

i18n:
	i18ndude sync --pot i18n/cpsskins.pot -s i18n/cpsskins-??.po
	i18ndude sync --pot i18n/cpsskins-default.pot -s i18n/cpsskins-default-??.po
	i18ndude sync --pot i18n/cpsskins-plone.pot -s i18n/cpsskins-plone-??.po

	i18ndude chart -o i18n/i18nchart.png --pot i18n/cpsskins.pot i18n/cpsskins-??.po
