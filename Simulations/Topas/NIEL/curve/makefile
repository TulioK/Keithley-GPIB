particles = 10000
energy = 200
start = 1
stop = 6
interval = 1
repeats = 10

default :
	@echo "Call something specific, like 'make files particles=50000 energy=200'"

files :
	cp -f nieltemplate.txt niel.topas
	cp -f lindhardtemplate.txt lindhard.topas
	python3 writer.py $(particles) $(energy) >> log.txt

run :
	make files
	topas niel.topas >> log.txt
	topas lindhard.topas >> log.txt
	python3 script.py $(particles)  $(energy) >> log.txt
	make clean

curve :
	rm -f nielresults.csv
	touch nielresults.csv
	rm -f lindhardresults.csv
	touch lindhardresults.csv
	rm -f log.txt
	touch log.txt
	
	for E in $(shell seq $(start) 1 $(stop)) ; do \
		for N in $(shell seq 1 $(interval) 9) ; do \
			for e in e ; do \
				echo -n "$$N$$e$$E, $(particles)" >> nielresults.csv ; \
				echo -n "$$N$$e$$E, $(particles)" >> lindhardresults.csv ; \
				for i in $(shell seq 1 $(repeats)) ; do \
					echo "Energy: $$N$$e$$E MeV, particle= $(particles), measurement $$i / $(repeats), goes to 9e$(stop) MeV." ; \
					make -s run energy=$$N$$e$$E ; \
				done ; \
				echo -n "\n" >> nielresults.csv ; \
				echo -n "\n" >> lindhardresults.csv ; \
			done ; \
		done ; \
	done
	python3 analyzer.py >> log.txt

clean :
	rm -f niel.topas
	rm -f lindhard.topas
	rm -f Score.csv
	rm -f Lindhard.csv
