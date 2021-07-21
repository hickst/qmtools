# environment variables for Docker container run parameters.
TOPLVL=${PWD}
INPUTS=${TOPLVL}/inputs
RPTS=${TOPLVL}/reports
TESTDIR=${TOPLVL}/tests

ARGS=
APP_ROOT=/qmview
CONINPUTS=${APP_ROOT}/inputs
CONRPTS=${APP_ROOT}/reports
ENVLOC=/etc/trhenv
EP=/bin/bash
IMG=qmview:devel
NAME=qmview
PROG=qmview
SHELL=/bin/bash
SCOPE=qmview
TEST=tests
TSTIMG=qmview:test


.PHONY: help bash cleancache cleanrpts docker dockert down exec run runt runt1 runtc runtep stop test up watch

help:
	@echo "Make what? Try: bash, cleancache, cleanrpts, docker, dockert, down, run, runt, runt1, runtc, runtep, stop, test, up, watch"
	@echo '  where:'
	@echo '     help      - show this help message'
	@echo '     bash      - run Bash in a ${PROG} container (for development)'
	@echo '     cleancache - REMOVE ALL __pycache__ dirs from the project directory!'
	@echo '     cleanrpts - REMOVE ALL input and output files from the reports directory!'
	@echo '     docker    - build a production container image'
	@echo '     dockert   - build a container image with tests (for testing)'
	@echo '     exec      - exec into running development server (CLI arg: NAME=containerID)'
	@echo '     run       - start a container (CLI: ARGS=args)'
	@echo '     runt      - run the main program in a test container'
	@echo '     runt1     - run a tests/test-dir in a container (CLI: TEST=testpath)'
	@echo '     runtc     - run all tests and code coverage in a container'
	@echo '     runtep    - run a test container with alternate entrypoint (CLI: EP=entrypoint, ARGS=args)'
	@echo '     stop      - stop a running container'
	@echo '     test      - run one or all tests in the tests directory (CLI: TEST=single_test_file)'
	@echo '     watch     - show logfile for a running container'

bash:
	docker run -it --rm --name ${NAME} -v ${INPUTS}:${CONINPUTS}:ro -v ${RPTS}:/${CONRPTS} --entrypoint ${SHELL} ${TSTIMG} ${ARGS}

cleancache:
	find . -name __pycache__ -print | grep -v .venv | xargs rm -rf

cleanrpts:
	@rm ${RPTS}/*

docker:
	docker build -t ${IMG} .

dockert:
	docker build --build-arg TESTS=tests -t ${TSTIMG} .

exec:
	docker cp .bash_env ${NAME}:${ENVLOC}
	docker exec -it ${NAME} ${EP}

run:
	@docker run -it --rm --name ${NAME} -v ${INPUTS}:${CONINPUTS}:ro -v ${RPTS}:${CONRPTS} ${IMG} ${ARGS}

runt:
	@docker run -it --rm --name ${NAME} -v ${INPUTS}:${CONINPUTS}:ro -v ${RPTS}:${CONRPTS} ${TSTIMG} ${ARGS}

runtep:
	@docker run -it --rm --name ${NAME} -v ${INPUTS}:${CONINPUTS}:ro -v ${RPTS}:${CONRPTS} --entrypoint ${EP} ${TSTIMG} ${ARGS}

runt1:
	docker run -it --rm --name ${NAME} -v ${INPUTS}:${CONINPUTS}:ro  -v ${RPTS}:${CONRPTS} --entrypoint pytest ${TSTIMG} -vv ${TEST}

runtc:
	docker run -it --rm --name ${NAME} -v ${INPUTS}:${CONINPUTS}:ro  -v ${RPTS}:${CONRPTS} --entrypoint pytest ${TSTIMG} -vv --cov-report term-missing --cov ${SCOPE}

stop:
	docker stop ${NAME}

test:
	pytest -vv ${TEST} --cov-report term-missing --cov ${SCOPE}

watch:
	docker logs -f ${NAME}
