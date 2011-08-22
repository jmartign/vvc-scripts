#!/usr/bin/perl
# $Id: mqcomm.pl 55 2009-06-02 22:07:27Z vvc $

use strict;
use MQClient::MQSeries;
use MQSeries::QueueManager;
use MQSeries::Command;

my $qm1='SOA1P';
my $conname1='soamq.vzbi.com(5050)';
my $qm2='SOA2S';
my $conname2='pdcsoai02.vzbi.com(2055)';

sub QM_Connect($$) {
   my $qm = shift;
   my $conname = shift;

   my $qmgr = MQSeries::QueueManager->new
        (
                QueueManager    => $qm,
                AutoConnect     => 0,
                AutoCommit      => 1,
                ConnectTimeout  => 120,
                RetryCount      => 5,
                RetrySleep      => 2,
                ClientConn => { 'ChannelName'    => 'SYSTEM.ADMIN.SVRCONN',
                                'TransportType'  => 'TCP',
                                'ConnectionName' => $conname
                              }
        ) or die "Unable to instantiate MQSeries::QueueManager object\n";

    $qmgr->Connect() or die("Unable to connect to queue manager $qm\n" .
                "CompCode => " . $qmgr->CompCode() . "\n" .
                "Reason => " . $qmgr->Reason() .
                " (", MQReasonToText($qmgr->Reason()) . ")\n");
   return $qmgr;
}

sub QLocal($) {
  my $qmgr = shift;
  my $command = MQSeries::Command->new
    (
     QueueManager => $qmgr
    ) or die("Unable to instantiate command object\n");

  my %qlocals = ();

  my @queues = $command->InquireQueue
        (
         QType          => 'Local'
        ) or die "InquireQueue: " . MQReasonToText($command->Reason()) . "\n";
  foreach my $queue (@queues) {
      if ($queue->{'DefinitionType'} ne 'Temporary') {
         $qlocals{$queue->{'QName'}}=1;
      }
  }
  return %qlocals;
}

sub QRemote($) {
  my $qmgr = shift;
  my $command = MQSeries::Command->new
    (
     QueueManager => $qmgr
    ) or die("Unable to instantiate command object\n");

  my %qremote = ();

  my @queues = $command->InquireQueue
        (
         QType          => 'Remote'
        ) or die "InquireQueue: " . MQReasonToText($command->Reason()) . "\n";
  foreach my $queue (@queues) {
    $qremote{$queue->{'QName'}}=1;
  }
  return %qremote;
}


my $qmgr1 = QM_Connect($qm1,$conname1);
my $qmgr2 = QM_Connect($qm2,$conname2);

my %qlocal1 = QLocal($qmgr1);
my %qlocal2 = QLocal($qmgr2);

print "Local queues defined in $qm2 and not in $qm1:\n";

foreach my $queue (sort keys %qlocal2) {
  if(!defined($qlocal1{$queue})) {
    print "$queue\n";
  }
}

my %qremote1 = QRemote($qmgr1);
my %qremote2 = QRemote($qmgr2);

print "Remote queues defined in $qm2 and not in $qm1:\n";

foreach my $queue (sort keys %qremote2) {
  if(!defined($qremote1{$queue})) {
    print "$queue\n";
  }
}
