# SPDX-License-Identifier: MIT
# Copyright 2019 Matthew Krupcale <mkrupcale@matthewkrupcale.com>

.PHONY = all

ORIGINAL_IMAGE = bin/orig.bin
MODIFIED_IMAGE = bin/mod.bin

PROCESSING_PROGRAM = scripts/modify_image.py

all: ${MODIFIED_IMAGE}

${MODIFIED_IMAGE}: ${ORIGINAL_IMAGE}     \
                   ${PROCESSING_PROGRAM}
	${PROCESSING_PROGRAM} ${ORIGINAL_IMAGE} ${MODIFIED_IMAGE}
