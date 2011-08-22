#!/usr/bin/perl
# $Id: certbasewatch.pl 294 2010-12-24 00:39:33Z vvc $

use Crypt::OpenSSL::X509;
use Date::Parse qw(str2time);
use POSIX qw(strftime floor);
use Net::SMTP;
my $DB='/root/CA/index.txt';
my $CERTS='/root/CA/certs';
my $warndays = 7;
my $smtphost = 'localhost';
my $smtpport = 587;
my $smtpfrom = 'root@chepkov.com';
my $debug = 0;

my $SECINDAY=24*60*60;

open(INDEX,$DB) or die $!;
while(<INDEX>) {
  ($status,$d1,$d2,$serial,$file,$subject) = split('\t');
  if($status eq 'V') {
    my $x509 = Crypt::OpenSSL::X509->new_from_file("$CERTS/".$serial.'.pem');
    if($x509->subject() =~ m/CN=(.*), /) {
      $cn = $1;
    } else {
      $cn = 'Unknown';
    }
    my $endcert = $x509->notAfter();
    my $email = $x509->email();
    print "$cn, $email, $endcert\n" if $debug;
    $email = $smtpfrom unless defined($email); 
    my $endcerttime = str2time($endcert);
    my $now = time();
    if ( $endcerttime > $now and $endcerttime < $now+$warndays*$SECINDAY) {
       $edays = floor (($endcerttime - $now) / $SECINDAY);
       my $str="Certificate for ".$cn." <".$email."> expires ";
       if ($edays > 1 ) {
          $str.="in ".$edays." days";
       } elsif ($edays < 1 ) {
          $str.="today";
       } else {
          $str.="tomorrow";
       }
       my $smtp = Net::SMTP->new(Host => $smtphost, Port => $smtpport ) or die "Can't connect to smtp server\n";

       $smtp->mail("<>");
       $smtp->to($email);
       my $rfc2822 = strftime("%a, %d %b %Y %H:%M:%S %z", localtime());

       $smtp->data();
       $smtp->datasend("From: $smtpfrom\n");
       $smtp->datasend("To: $email\n");
       $smtp->datasend("Date: $rfc2822\n");
       $smtp->datasend("X-Priority: 1 (Highest)\n");
       $smtp->datasend("Importance: High\n");
       $smtp->datasend("Precedence: Bulk\n");
       $smtp->datasend("Subject: Warning: Certificate is about to expire\n");
       $smtp->datasend("\n");
       $smtp->datasend("\n".$str.".\n");
       $smtp->datasend("\n");
       $smtp->datasend("If you want to renew it, you have to send a certificate request to $smtpfrom.\n");
       $smtp->datasend("\n");
       $smtp->datasend("If you already received your new certificate or do not plan to use it anymore,\n");
       $smtp->datasend("please, disregard this message.\n");
       $smtp->datasend("\n");
       $smtp->datasend("Sincerely,\n");
       $smtp->datasend("Certificate Watch Robot\n");
       $smtp->datasend("\n");
       $smtp->dataend();
       $smtp->quit;
    }
  }
}
close(INDEX) or die $!;

