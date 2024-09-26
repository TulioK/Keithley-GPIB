particles = 10000
energy = 200
start = 0
stop = 0
interval = 3
repeats = 5
size = 1

default :
	@echo "Call something specific, like 'make files particles=50000 energy=200'"

files :
	cp -f nieltemplate.txt niel.topas
	python3 writer.py $(particles) $(energy) $(size) >> log.txt

run :
	make files
	topas niel.topas >> log.txt
	python3 script.py $(particles)  $(energy) $(size) >> log.txt
	make clean

size :
	rm -f results.csv
	touch results.csv
	rm -f Lindhardresults.csv
	touch Lindhardresults.csv
	rm -f log.txt
	touch log.txt
	for E in $(shell seq $(start) 1 $(stop)) ; do \
		for N in $(shell seq 1 $(interval) 9) ; do \
			for e in e ; do \
				echo -n "$(energy), $(particles), $$N$$e$$E" >> results.csv ; \
				echo -n "$(energy), $(particles), $$N$$e$$E" >> Lindhardresults.csv ; \
				for i in $(shell seq 1 $(repeats)) ; do \
					echo "Particles: $(particles), Energy: $(energy) MeV, size $$N$$e$$E, goes to 9e$$stop, measurement $$i/$(repeats) " ; \
					make -s run size=$$N$$e$$E ; \
				done ; \
				echo -n "\n" >> results.csv ; \
				echo -n "\n" >> Lindhardresults.csv ; \
			done ; \
		done ; \
	done
	python3 analyzer.py >> log.txt

clean :
	rm -f niel.topas
	rm -f Score.csv
