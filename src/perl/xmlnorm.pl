#!/usr/bin/perl
# $Id: xmlnorm.pl 72 2009-10-16 21:35:52Z vvc $

use strict;
use XML::Twig;

if ($#ARGV != 0 ) {
 print "Usage: $0 xmlfile\n";
 exit(1);
}

my $twig = XML::Twig->new (comments => 'drop', pretty_print => 'indented');

$twig->safe_parsefile($ARGV[0]); 
die "Ill-formed xml: $ARGV[0]: $@\n" if $@;

open(NORMAL, ">$ARGV[0]");
binmode NORMAL, ":utf8";
select NORMAL;
$twig->print;
close(NORMAL);

