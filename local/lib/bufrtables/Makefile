#
#                                 Makefile for bufrtables
#
R64 = 
ARCH = linux
CNAME = _gfortran
LIB = bufr
A64 = A64
#
LIBRARY  = ../lib$(LIB)$(R64).a
#
include ../config/config.$(ARCH)$(CNAME)$(R64)$(A64)
#
include ../options/options_$(ARCH)
#
TARGETS      = all clean
#
SOURCES.F=



#
OBJECTS.F    = $(SOURCES.F:.F=.o) 
OBJECTS.c    = $(SOURCES.c:.c=.o)
OBJECTS      = $(OBJECTS.F) $(OBJECTS.c) 
#
#
all:  links 

links: 
	./clean.sh
	./links.sh
bufr2txt_tables: bufr2txt_tables.f
	$(FC) $(FFLAGS) -o bufr2txt_tables bufr2txt_tables.f $(LIBRARY)
bufr_split_tables: bufr_split_tables.f
	$(FC) $(FFLAGS) -o bufr_split_tables bufr_split_tables.f $(LIBRARY)
txt2bufr_tables: txt2bufr_tables.f
	$(FC) $(FFLAGS) -o txt2bufr_tables txt2bufr_tables.f $(LIBRARY)

clean:
	./clean.sh
	\rm -f bufr2txt_tables; \rm -f bufr_split_tables; \rm -f txt2bufr_tables
