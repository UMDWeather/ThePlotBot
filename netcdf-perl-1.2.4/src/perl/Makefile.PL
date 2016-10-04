# Generated automatically from Makefile.PL.in by configure.
use ExtUtils::MakeMaker qw(WriteMakefile);


# The existence of the ./*/Makefile.PL file causes MakeMaker
# to automatically include Makefile code for the targets
#	all, clean, realclean and */Makefile
# which perform the corresponding action in the subdirectory.

$version = "1.2.4";
                           
WriteMakefile(
    'NAME'     => 'NetCDF',
    'DISTNAME' => "netcdf-perl-" + $version,
    'VERSION'  => $version,
    'INC'     => '-I/usr/include',
    'OBJECT' => 'NetCDF.o',
    'LIBS' => "-L/usr/lib -lnetcdf ",
    'clean' => {'FILES' => "*.nc NetCDF.bs"},
    'realclean' => {'FILES' => "*.old Makefile.PL"}
);
