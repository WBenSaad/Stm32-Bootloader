##########################################################################################################################
# File automatically-generated by tool: [projectgenerator] version: [3.13.0-B3] date: [Tue Sep 07 20:05:32 CEST 2021]
##########################################################################################################################

# ------------------------------------------------
# Generic Makefile (based on gcc)
#
# ChangeLog :
#	2017-02-10 - Several enhancements + project update mode
#   2015-07-22 - first version
# ------------------------------------------------
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))
BUILD_DIR = build
SUBDIRS  := $(wildcard */.)
App_Dir  := $(mkfile_dir)MainApp/build
App		  = $(App_Dir)/Main_App.bin
Boot_Dir := $(mkfile_dir)Bootloader/build
Boot	  = $(Boot_Dir)/Bootloader.bin
PROJECT	  = STM32




.PHONY: all $(SUBDIRS)
.PHONY: flash $(SUBDIRS)

all: build

build: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ 


#flash: $(SUBDIRS)
#$(SUBDIRS):
#	$(MAKE) -C $@ flash

#flash:
#	%.bin: $(Boot_Dir)/Bootloader.bin $(App_Dir)/Main_App.bin
#		cat $^ > $@







# *** EOF ***