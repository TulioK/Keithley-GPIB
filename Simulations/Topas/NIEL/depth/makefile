particles = 10000
energy = 200
repeats = 10

default :
	@echo "Call something specific, like 'make files particles=50000 energy=200'"

files :
	cp -f depthtemplate.txt depth.topas
	python3 writer.py $(particles) $(energy) >> log.txt

run :
	make files
	topas depth.topas >> log.txt
	python3 script.py $(particles)  $(energy) >> log.txt
	make clean

depth :
	rm -f depthresults.csv
	touch depthresults.csv
	rm -f log.txt
	touch log.txt
	
	#echo -n "$$N$$e$$E, $(particles)" >> depthresults.csv
	for i in $(shell seq 1 $(repeats)) ; do \
		echo "Energy: $(energy) MeV, particles: $(particles), measurement $$i / $(repeats)." ; \
		make -s run; \
	done ; \
	echo -n "\n" >> depthresults.csv
	
	python3 analyzer.py >> log.txt

clean :
	rm -f depth.topas
	rm -f Displacement.csv
