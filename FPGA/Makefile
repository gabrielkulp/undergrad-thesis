# spellchecker: disable
PROJ := co-proc

PROJ_BASEDIR := rtl
PROJ_RTL_SRCS := $(addprefix $(PROJ_BASEDIR)/, \
	spi/spi_fast.v \
	spi/spi_fast_core.v \
	aes/aes.v \
	aes/tables.v \
	aes/key_schedule.v \
	sysmgr.v \
	seven_seg.v \
	label_array.v \
	label_ctl.v \
	spi_decoder.v \
)

PROJ_TOP_SRC := $(PROJ_BASEDIR)/top.v
PROJ_TOP_MOD := top

# Target config
BOARD ?= icebreaker
DEVICE = up5k
PACKAGE = sg48
FREQUENCY = 30

#NEXTPNR_ARGS = --pre-pack data/clocks.py

# Include default rules
include ./rules.mk
