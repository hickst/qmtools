# SIF should already be set, in the environment, to your local repository. For example:
#   export SIF=/contrib/singularity/shared/neuroimaging
#
TOPLVL=${PWD}
FETCHED=${TOPLVL}/fetched
INPUTS=${TOPLVL}/inputs
QRYS=${TOPLVL}/queries
RPTS=${TOPLVL}/reports
TESTDIR=${TOPLVL}/tests

ARGS=
CONFETCHED=/fetched
CONINPUTS=/inputs
CONQRYS=/queries
CONRPTS=/reports
IGNORE=tests/qmtools/qmfetcher/test_fetcher_main.py
IMG=hickst/qmtools
IMGSIF=qmtools_latest.sif
ONLY=
PROG=QMTools
SHELL=/bin/bash
SCOPE=qmtools
TESTS=tests
TSTIMG=qmtools:test
TSTIMGSIF=qmtools_test.sif


.PHONY: help bash bash_hpc cleancache cleanfetch cleanrpts docker dockert sif sift testall test1 tests

help:
	@echo 'Make what? Try: bash, bash_hpc, cleancache, cleanfetch, cleanrpts,'
	@echo '                docker, dockert, sif, sift, testall, test1, tests'
	@echo '  where:'
	@echo '     help       - show this help message'
	@echo "     bash       - run Bash in a ${PROG} Docker container (for debugging)"
	@echo "     bash_hpc   - run Bash in a ${PROG} Apptainer container (for debugging)"
	@echo '     cleancache - REMOVE ALL __pycache__ dirs from the project directory!'
	@echo '     cleanfetch - REMOVE ALL FILES from the fetched directory!!'
	@echo '     cleanrpts  - REMOVE ALL FILES from the reports directory!!'
	@echo '     docker     - build a production Docker image'
	@echo '     dockert    - build a development Docker image (for testing)'
	@echo '     sif        - build a production Apptainer container image'
	@echo '     sift       - build a developement Apptainer image (for testing)'
	@echo '     testall    - run all tests in the tests directory, including slow tests.'
	@echo '     test1      - run tests with a single name prefix (CLI: ONLY=tests_name_prefix)'
	@echo '     tests      - run one or all unit tests in the tests directory (CLI: TESTS=test_module)'

bash:
	docker run -it --rm --name qmtools -v ${FETCHED}:${CONFETCHED} -v ${INPUTS}:${CONINPUTS}:ro -v ${RPTS}:${CONRPTS} -v ${QRYS}:${CONQRYS} --entrypoint ${SHELL} ${TSTIMG} ${ARGS}

bash_hpc:
	apptainer exec --pwd / -B ${PWD}/inputs:/inputs:ro -B ${PWD}/fetched:/fetched -B ${PWD}/reports:/reports -B ${PWD}/queries:/queries ${SIF}/${TSTIMGSIF} ${SHELL} ${ARGS}

cleancache:
	find . -name __pycache__ -print | grep -v .venv | xargs rm -rf
	@rm -rf .pytest_cache

cleanfetch:
	@rm -f ${FETCHED}/*

cleanrpts:
	@rm -rf ${RPTS}/*

docker:
	docker build -t ${IMG} .

dockert:
	docker build -t ${TSTIMG} .

sif:
	apptainer pull ${IMGSIF} docker://${IMG}

sift:
	apptainer build ${TSTIMGSIF} docker-daemon:${TSTIMG}

testall:
	pytest -vv -x ${TESTS} ${ARGS} --cov-report term-missing --cov ${SCOPE}

test1:
	pytest -vv  ${TESTS} -k ${ONLY} --cov-report term-missing --cov ${SCOPE}

tests:
	pytest -vv --ignore ${IGNORE} ${TESTS} ${ARGS} --cov-report term-missing --cov ${SCOPE}
