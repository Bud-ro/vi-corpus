#!/usr/bin/perl -w

use strict;
use File::Find;

# subroutines
sub stripPaths;
sub removeDups;

my @searchPaths;
push (@searchPaths, $ARGV[0]);
my @files;
find sub { -f && push(@files, $File::Find::name)}, @searchPaths;
my @directories = @files;
stripPaths(\@directories);
@directories = removeDups(\@directories);

#Print the directories needed
foreach my $item (@directories)
{
  $item =~ s/$ARGV[0]//;
  if ( $item )
  {
	print "need_dir \"<lvpath>$item\"\n";
  }
}

foreach my $item (@files)
{
  $item =~ s/$ARGV[0]//;
  if ( $item )
  {
	print "need \"<lvpath>$item\" from \"$ARGV[0]$item\" \n";
  }
}


#==============================================
# Subroutines
#==============================================

1300# The stripPaths subroutine takes a reference to an array of paths
# as an argument and strips the trailing forward slash and anything
# after it for each element.
sub stripPaths
{
  my $depArray=shift; 
  foreach my $dep (@$depArray)
  {
	$dep = reverse($dep);
	$dep =~ s/^.+?\///;
	$dep = reverse($dep);
  }#end for
}#end stripPaths

# The removeDups subroutine takes a reference to an array as an 
# argument and returns an array stripped of duplicates.
# This subroutine assumes the array is already sorted.
sub removeDups
{
  my $arrayItem=shift; 
  my @returnArray;
  my $previousItem = "";
  foreach my $singleItem (@$arrayItem)
  {
	push (@returnArray, $singleItem) unless ($singleItem eq $previousItem);
	$previousItem = $singleItem;
  }#end for
  return @returnArray;
}#end removeDups
