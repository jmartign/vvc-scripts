#!/usr/bin/perl -w
use POSIX qw(setsid);

my $pidfile='/tmp/daemon.pid';
my $logfile='/tmp/daemon.log';

my $daemon_continue=1;
daemon();

$0 = "daemon ...";

print "Starting\n";
while($daemon_continue) {
	print "Running...\n";
	sleep(300);
}
unlink($pidfile);
print "Exiting\n";

sub daemon {
  if ( -e $pidfile ) {
    die "$pidfile already exist\n";
  }
  $SIG{'INT' } = \&interrupt;
  $SIG{'HUP' } = \&interrupt;
  $SIG{'QUIT'} = \&interrupt;
  $SIG{'TERM'} = \&interrupt;
  $| = 1;
  chdir '/';
  open STDIN,'/dev/null';
  open STDOUT,">>$logfile" or die "Can't write to $logfile: $!";
  open STDERR,'>&STDOUT' or die "Can't write to $logfile :$!";
  defined(my $pid = fork) or die "Can't fork: $!";
  if ($pid ) {
    open(PID,">$pidfile") or die "Can't write to $pidfile\n";
    print PID "$pid\n";
    close(PID);
    exit;
  }
  setsid or die "Can't start a new session: $!";
  umask 0;
}

sub interrupt {
  my $signame = shift;
  print "Caught a signal SIG$signame\n";
  $daemon_continue=0;
}
