#!/usr/bin/perl -w

use strict;
use Net::LDAP;

my $SKEL='/etc/skel';
my $SERVER="ldap.videonext.net";
my $BASE="ou=People,dc=videonext,dc=net";

my $ldap = Net::LDAP->new($SERVER);
$ldap->bind;
my $mesg = $ldap->search(filter=>"(objectClass=posixAccount)",
			base=>$BASE,
			attrs=>['uid','gidNumber','homeDirectory','mail'] );

my @entries = $mesg->entries;
foreach my $entry (@entries) {
  my $uid = $entry->get_value('uid');
  my $gidNumber = $entry->get_value('gidNumber');
  my $homeDirectory = $entry->get_value('homeDirectory');
  my $mail = $entry->get_value('mail');
  if(! -e $homeDirectory) {
    print "Creating $homeDirectory for user $uid\n";
    system("cp -rp $SKEL $homeDirectory");
    if(!defined($mail)) {
      print "No e-mail addres found for user $uid\n";
    } elsif ($mail =~ '@videonext.net$') {
      print "No mail forwarding for $uid\n";
    } else {
      open(PROCMAILRC,">$homeDirectory/.procmailrc");
      print PROCMAILRC <<"EOF";
:0
! $mail
EOF
      close(PROCMAILRC);
    }
    system("chown -R $uid:$gidNumber $homeDirectory");
    system("restorecon -R $homeDirectory");
    system("chmod 700 $homeDirectory");
  }	
}
