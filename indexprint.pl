#!/usr/bin/perl

use Crypt::OpenSSL::X509;
use Date::Parse qw(str2time);
my $DB='/root/CA/index.txt';
my $CERTS='/root/CA/certs';
my $HTML='/var/www/html/restricted/vpn/index.html';

open(HTML,">$HTML") or die $!;
open(INDEX,"/bin/sort -k1 $DB|") or die $!;
print HTML <<"HR";
<HTML>
<HEAD>
<TITLE>
videoNEXT Network Operation Center
</TITLE>
<style type="text/css">
TD {font-family:monospace; font-size: 10pt;}
body {background-color: silver; }
</style>
</HEAD>
<BODY>
<CENTER>
<H1>videoNEXT VPN Client Certificates</H1>
<TABLE border=1>
<TR>
<TD>Common Name</TD><TD>Serial</TD><TD>E-Mail</TD><TD>Valid until</TD>
</TR>
HR

while(<INDEX>) {
  ($status,$d1,$d2,$serial,$file,$subject) = split('\t');
  if($status eq 'V') {
    open(SSL,"openssl x509 -noout -in $CERTS/$serial.pem -purpose|") or die "Can't run openssl\n";
    my $client=1;
    while(my $purpose = <SSL>) {
      if ($purpose =~ m/SSL client : No/) {
        $client = 0;
        last;
      }
    }
    close(SSL) or die "Couldn't run openssl\n";
    next unless $client;
    my $x509 = Crypt::OpenSSL::X509->new_from_file("$CERTS/".$serial.'.pem');
    if($x509->subject() =~ m/CN=(.*), /) {
      $cn = $1;
    } else {
      $cn = 'Unknown';
    }
    my $endcert = $x509->notAfter();
    my $endcerttime = str2time($endcert);
    if ( $endcerttime > time() ) {
       printf HTML "<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>\n",$cn,$serial,$x509->email(),$endcert;
    }
  }
}
close(INDEX) or die $!;
print HTML <<"TR";
</TABLE>
</CENTER>
</BODY>
</HTML>
TR
close(HTML) or die $!;
