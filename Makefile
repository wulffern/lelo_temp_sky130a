LIB=LELO_TEST_SKY130A
CELL=LELO_TEST

include tech/make/main.make

#- Extra pages for the Jekyll site. gendoc copies documents/ into
#- docs/, and the DOCS workflow triggers on documents/**, so the page
#- is committed rather than built in CI. LAYOUT_FLOW.md stays the one
#- source; this stamps the front matter onto a copy of it.
docs: documents/layout_flow.md

documents/layout_flow.md: LAYOUT_FLOW.md
	@mkdir -p documents
	@printf -- '---\nlayout: page\ntitle: Layout Flow\n---\n\n' > $@
	@cat $< >> $@
	@echo "regenerated $@ from $<"
