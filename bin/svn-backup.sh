#!/bin/ksh
# $Id: svn-backup.sh 314 2011-04-22 18:04:03Z vvc $

# SOURCEHOST has to be configured in ~/.ssh/config, i.e.
# Host		svndev
# BatchMode	yes
# Hostname	svn.dev.videonext.net
# User		backup
# IdentityFile 	~/.ssh/svndev.key

SOURCEHOST=svndev
SOURCEDIR=/svnroot/repos
BACKUPDIR=/var/backup/videonext-svn
REPOSDIR=$BACKUPDIR/repos

set -e

# Initialize backup structure
if [[ ! -d BACKUPDIR/hooks ]] ; then
  mkdir -p $BACKUPDIR/hooks
  cat > $BACKUPDIR/hooks/pre-revprop-change <<EOF
#!/bin/sh
exit 0
EOF

  chmod +x $BACKUPDIR/hooks/pre-revprop-change
fi

ssh $SOURCEHOST ls -1 $SOURCEDIR | while read repo
do
  if [[ ! -d $REPOSDIR/$repo ]] ; then
     echo "svn repository $repo has been added"
     svnadmin create $REPOSDIR/$repo
     svn info svn+ssh://$SOURCEHOST/$SOURCEDIR/$repo | grep UUID > $REPOSDIR/$repo/backup.uuid
     ln -s $BACKUPDIR/hooks/pre-revprop-change $REPOSDIR/$repo/hooks/
     if ! svnsync init --non-interactive --quiet file://$REPOSDIR/$repo svn+ssh://$SOURCEHOST/$SOURCEDIR/$repo ; then
       echo $repo init has failed >&2
     fi
  fi
# In case URL changed
#   TMP1=/tmp/svnsync.$$
#   echo -n "svn+ssh://$SOURCEHOST/$SOURCEDIR/$repo" > $TMP1
#   svnadmin setrevprop $REPOSDIR/$repo -r0 svn:sync-from-url $TMP1
#   rm -f $TMP1
  if ! svnsync sync --non-interactive --quiet file://$REPOSDIR/$repo  ; then
   echo $repo sync has failed >&2
  fi
  if [[ "$1" = "props" ]] ; then
    if ! svnsync copy-revprops --non-interactive --quiet file://$REPOSDIR/$repo  ; then
       echo $repo sync has failed >&2
    fi
  fi 
done
