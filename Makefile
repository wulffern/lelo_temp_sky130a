LIB=LELO_TEST_SKY130A
CELL=LELO_TEST

include tech/make/main.make

#- Extra pages for the Jekyll site. gendoc copies documents/ into
#- docs/, and the DOCS workflow triggers on documents/**, so the page
#- is committed rather than built in CI.
#-
#- documents/layout_flow.md IS THE SOURCE. It used to be generated from
#- LAYOUT_FLOW.md at the repo root, which is deleted -- so the rule
#- depended on a file that is not there and `make docs` died on it.
#- docs/ is gitignored and documents/ is tracked, so the tracked copy
#- is the one that can be the source.
docs: documents/layout_flow.md
