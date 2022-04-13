#
# Copyright 2017 The Openstack-Helm Authors.
#
# Copyright (c) 2021 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# It's necessary to set this because some environments don't link sh -> bash.
SHELL := /bin/bash
TASK  := build

EXCLUDES := helm-toolkit doc tests tools logs tmp .build
CHARTS := helm-toolkit $(filter-out $(EXCLUDES), $(patsubst %/.,%,$(wildcard */.)))
VARIANTS := centos debian

.PHONY: $(EXCLUDES) $(CHARTS)

# Usage: $(call helm-package,VARIANT,CHART_SRC_DIR)
# Build the specified variant of a chart by replacing
# "variant = ..." with VARIANT
define helm-package
	{ \
		rm -rf .build/$(1)/$(2) && \
		mkdir -p .build/$(1) && \
		cp -ar $(2) .build/$(1)/$(2) && \
		sed -i 's#^\(\s*variant\s*:\s*\).*#\1'"$(1)"'#' .build/$(1)/$(2)/values.yaml && \
		helm package -d .build/$(1) .build/$(1)/$(2) ; \
	}
endef

all: $(CHARTS)

$(CHARTS):
	@if [ -d $@ ]; then \
		echo; \
		echo "===== Processing [$@] chart ====="; \
		make $(TASK)-$@; \
	fi

init-%:
	if [ -f $*/Makefile ]; then make -C $*; fi
	if [ -f $*/requirements.yaml ]; then helm dep up $*; fi

lint-%: init-%
	if [ -d $* ]; then helm lint $*; fi

build-%:
	if [ -d $* ]; then \
		for variant in $(VARIANTS) ; do \
			$(call helm-package,$$variant,$*) || exit 1 ; \
		done ; \
	fi

clean:
	@echo "Clean all build artifacts"
	rm -f */templates/_partials.tpl */templates/_globals.tpl
	rm -f *tgz */charts/*tgz */requirements.lock
	rm -rf */charts */tmpcharts
	rm -rf .build

%:
	@:
