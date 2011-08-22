include(`/usr/share/sendmail-cf/m4/cf.m4')dnl
VERSIONID(`setup for linux')dnl
OSTYPE(`linux')dnl
define(`SMART_HOST', `mail.server')dnl
define(`confTO_CONNECT', `1m')dnl
define(`confDONT_PROBE_INTERFACES', `True')dnl
define(`ALIAS_FILE', `/etc/aliases')dnl
define(`confPRIVACY_FLAGS', `authwarnings,novrfy,noexpn,nobodyreturn')dnl
FEATURE(authinfo, `hash -o /etc/mail/authinfo')dnl
dnl Install cyrus-sasl-plain for plain auth to work
define(`confAUTH_MECHANISMS', `PLAIN LOGIN')dnl
define(`confCACERT_PATH', `/etc/pki/tls/certs')dnl
define(`confCACERT', `/etc/pki/tls/certs/CA.pem')dnl
define(`confTO_IDENT', `0')dnl
FEATURE(`no_default_msa', `dnl')dnl
DAEMON_OPTIONS(`Port=smtp,Addr=127.0.0.1, Name=MTA')dnl
MAILER(smtp)dnl
LOCAL_RULESETS
SHdrFromSMTP
R$*			$@ backup@chepkov.com

SEnvFromSMTP
R$*			$@ backup@chepkov.com
