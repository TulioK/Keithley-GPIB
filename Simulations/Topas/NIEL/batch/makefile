


particles = 1000000
energy = 200
start = 1
stop = 4
interval = 2

default :
	@echo "Call something specific, like 'make pka particles=1000000 energy=200'"

pka :
	make files
	make run
	python3 ../script.py >> log.txt
	make clean

nielcurve :
	rm -f batchresults.csv
	touch batchresults.csv
	rm -f log.txt
	touch log.txt
	for E in $(shell seq $(start) 1 $(stop)) ; do \
		for N in $(shell seq 1 $(interval) 9) ; do \
			for e in e ; do \
				echo "$$N$$e$$E MeV, $(particles) Particles " ; \
				echo "$$N$$e$$E, $(particles), " >> batchresults.csv ; \
				make pka energy=$$N$$e$$E ; \
			done ; \
		done ; \
	done
	python3 batchplotter.py

files :
	cp -f topaswritertemplate.topas nuclear.topas
	cp -f topaswritertemplate.topas coulomb.topas
	python3 topaswriter.py $(particles) $(energy) >> log.txt

clean :
	rm -f nuclear.topas
	rm -f coulomb.topas
	rm -f CoulombKnock.header
	rm -f CoulombKnock.phsp
	rm -f Knock.header
	rm -f Knock.phsp
	rm -f log.txt
run :
	topas nuclear.topas >> log.txt
	topas coulomb.topas >> log.txt
