#!/usr/bin/env bash

if [[ ! $@ ]]; then
	python3 -m fm -h
else
	python3 -m fm $@
fi
