#!/usr/bin/perl -w
#script to help a novice Amanda admin figure out how to set dumpcycle,
#runspercycle, runtapes, and tapecycle
#asks a series of questions, then makes appropriate recommendations
#
#written Feb 13, 2004 by Kurt Yoder
#you can email me at freespirit74@yahoo.com
#
#This script is copyright 2004 by Kurt Yoder and is licensed under the GPL
#See http://fsf.org for more information
#
use strict;
use diagnostics;

my $input_ok = 0;
my ( $dumpcycle, $number_backups, $per_time_period, $time, $time_period, $yn );
my ( $changer, $dc_unit, $runtapes, $total_tapes, $tapecycle, $tapes_per_backup );
my ( $backups, $backups_per_time, $per );

sub get_backups_per_period{
        print( "Now please tell me how often you will be doing a backup\n" );
        print( "I will ask for some number per time period\n" );
        print( "For example, '2 backups every 2 weeks'\n" );
        
        $number_backups = 'false';
        while( $number_backups eq 'false' ){
                print( "Enter number of backups: " );
                $number_backups = <>;
                chomp( $number_backups );
                if( $number_backups !~ /^\d{1,5}$/ ){
                        $number_backups = 'false';
                } elsif( $number_backups < 1 ){
                        $number_backups = 'false';
                }
        }
        $backups = 'backup';
        if( $number_backups > 1 ){
                $backups .= 's';
        }
        
        $time_period = 'false';
        $per_time_period = '';
        while( $time_period eq 'false' ){
                print( "\nTime period can be d for day, w for week, m for month, y for year\n" );
                print( "For multiple days/weeks/months/years type '2d', '5w', etc\n" );
                print( "For single days/weeks/months/years type 'd', 'w', etc\n" );
                print( "Enter time period: " );
                $time_period = <>;
                chomp( $time_period );
        
                if( $time_period =~ /^(\d{0,6})([dwmy])$/ ){
                        $per_time_period = $1;
                        $time_period = $2;
                        $time_period = lc( $time_period );
                        
                        if( $per_time_period ne '' ){
                                $per_time_period = int( $per_time_period );
                                if( $per_time_period == 0 ){
                                        print( "Number cannot be 0\n" );
                                        $time_period = 'false';
                                } else {
                                        &valid_time_period();
                                }
                        } else {
                                $per_time_period = 1;
                                &valid_time_period();
                        }
                        
                } else {
                        $time_period = 'false';
                }
        }
        
        $per = '';
        if( $per_time_period > 1 ){
                $time .= 's';
                $per = $per_time_period . ' ';
        }
        if( $dumpcycle > 1 ){
                $dc_unit .= 's';
        }
}

sub get_runtapes{
        print( "First we will determine the maximum number of tapes you will use per backup\n" );
        
        $yn = '';
        while( $yn !~ /^[yn]$/ ){
                print( "Do you have any kind of automatic/manual tape changer? (y/n): " );
                $yn = <>;
                chomp( $yn );
                $yn = lc( $yn );
        }
        
        if( $yn eq 'n' ){
                $tapes_per_backup = "1 tape maximum per backup";
                $runtapes = 1;
        } else {
        
                print( "Going to use a tape changer\n" );
                print( "What is the maximum number of tapes you want your changer to use every backup\n" );
                $runtapes = '';
                while( $runtapes !~ /^\d{1,3}$/ ){
                        print( "Enter the maximum: " );
                        $runtapes = <>;
                        chomp( $runtapes );
                }
        
                my $tapes = 'tape';
                if( $runtapes > 1 ){
                        $tapes .= 's';
                }
                $tapes_per_backup = "$runtapes $tapes maximum per backup";
        }
        print( "\nYou will use $tapes_per_backup\n\n" );
}

sub valid_time_period{
        $dc_unit = 'day';
        if( $time_period eq 'd' ){
                $dumpcycle = $per_time_period;
                $time = 'day';
                #print( 
                #       "\nWarning: do not do your dumps more than " . 
                #       ( $dumpcycle - 1 ) . 
                #       " days apart\nIf you do, you will get unexpected results\n");
        } elsif( $time_period eq 'w' ){
                $dumpcycle = $per_time_period;
                $time = 'week';
                $dc_unit = 'week';
        } elsif( $time_period eq 'm' ){
                #try to account for variable-length months
                $dumpcycle = int ( $per_time_period * 365 / 12 );
                $time = 'month';
        } elsif( $time_period eq 'y' ){
                #lets try to take leap years into account
                $dumpcycle = int ( $per_time_period * 1461 / 4 );
                $time = 'year';
        }

        $tapecycle = ( $number_backups + 1 ) * $runtapes;

        print( "\nIf you know how many tapes you will be using, please enter this now\n" );
        print( "Or to 'scale' this up by a certain number, enter x then the number\n" );
        print( "Or to let me calculate the minimum number of tapes, leave this blank\n" );

        my $cycles;
        $total_tapes = 'false';
        while( $total_tapes eq 'false' ){
                print( "Enter number, x then number,  or Enter: " );
                $total_tapes = <>;
                chomp( $total_tapes );
                
                if( $total_tapes =~ /^(\d){1,4}$/ ){
                        if( $total_tapes < $tapecycle ){
                                print( "You should have a minimum of $tapecycle tapes for the configuration you want\n\n" );
                                print( "If you really only have $total_tapes tapes, hit Enter then restart this script\n" );
                                print( "and reduce your backups per $time or your number of tapes per backup\n" );
                                $total_tapes = 'false';
                        } else {
                                #because I am not a good mathematician, I am going to brute-force
                                #with an inefficient while loop
                                my $tapes_req = $tapecycle;
                                $cycles = 1;
                                while( $tapes_req <= $total_tapes ){
                                        $cycles++;
                                        $tapes_req += $tapecycle - $runtapes;
                                }
                                $cycles--;
                                print( 
                                        "You have $total_tapes tapes which means you can support " .
                                        $cycles .
                                        " $time" . "'s worth of backups\n"
                                );
                                print( "Multiplying backups and tapes by $cycles\n" );
                        }

                } elsif( !$total_tapes ){
                        print( "Skipped; I will calculate the number of tapes needed\n" );
                        $cycles = 1;

                } elsif( 
                        $total_tapes =~ /^x(\d){1,3}$/ || 
                        $total_tapes =~ /^(\d){1,3}x$/ 
                ){
                        if( $1 > 1 ){
                                print( "'Scaling' up to $1 $time" . "'s worth of backups\n" );
                                $cycles = $1;
                        } else {
                                print( "$1 doesn't make sense here\n" );
                                $total_tapes = 'false';
                        }

                } else {
                        $total_tapes = 'false';
                }
        }

        $dumpcycle *= $cycles;
        $number_backups *= $cycles;
        $per_time_period *= $cycles;

        $tapecycle -= $runtapes;
        $tapecycle *= $cycles;
        $tapecycle += $runtapes;
}

my $mainloop = 'go';
while( $mainloop eq 'go' ){
        &get_runtapes();
        &get_backups_per_period();

        $backups_per_time =  "$number_backups $backups every $per$time";
        print( "\nYou can do $backups_per_time\n\n" );
        $yn = '';
        while( $yn !~ /^[yn]$/ ){
                print( "Is this the configuration you want? (y/n) " );
                $yn = <>;
                chomp( $yn );
                $yn = lc( $yn );

                if( $yn eq 'n' ){
                        print( "OK, we'll go through the questions again\n\n" );
                } elsif( $yn eq 'y' ) {
                        $mainloop = '';
                }
        }
}

print( "To do $backups_per_time using $tapes_per_backup\n" );
print( "You should use minimum $tapecycle tapes and set the following Amanda configuration:\n\n" );
print( "dumpcycle $dumpcycle $dc_unit\n" );
print( "runspercycle $number_backups\n" );
print( "runtapes $runtapes\n" );
print( "tapecycle $tapecycle tapes\n\n" );
